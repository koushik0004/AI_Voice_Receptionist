import re

from app.core.models import (
    BookingDetails,
    CallEvent,
    CallSession,
    CallStage,
    Intent,
    WhatsAppMessage,
    WorkflowResult,
)
from app.core.ports import (
    BookingAdapter,
    BusinessRepository,
    SessionStore,
    TelephonyClient,
    WhatsAppClient,
)


class ReceptionistWorkflow:
    def __init__(
        self,
        businesses: BusinessRepository,
        sessions: SessionStore,
        telephony: TelephonyClient,
        whatsapp: WhatsAppClient,
        booking: BookingAdapter,
    ) -> None:
        self.businesses = businesses
        self.sessions = sessions
        self.telephony = telephony
        self.whatsapp = whatsapp
        self.booking = booking

    def handle_call_started(self, event: CallEvent) -> WorkflowResult:
        business = self.businesses.get(event.business_id)
        session = CallSession(
            call_id=event.call_id,
            business=business,
            caller_number=event.caller_number,
            source=event.source,
        )
        self.sessions.save(session)
        greeting = (
            f"Thank you for calling {business.name}. This call may be recorded for quality purposes. "
            "How can I help you today?"
        )
        return self._result(session, greeting, ["call_started"])

    def handle_missed_call(self, event: CallEvent) -> WorkflowResult:
        business = self.businesses.get(event.business_id)
        provider_ref = self.telephony.call_back(event.caller_number, business)
        session = CallSession(
            call_id=event.call_id,
            business=business,
            caller_number=event.caller_number,
            source=event.source,
        )
        session.summary = f"Missed call callback started for {event.caller_number}."
        self.sessions.save(session)
        self._notify_owner(
            session,
            "missed_call_recovery",
            f"Missed call recovery started for {event.caller_number}. Callback ref: {provider_ref}.",
        )
        return self._result(
            session,
            f"Calling the customer back now for {business.name}.",
            ["callback_queued", "owner_whatsapp_sent"],
        )

    def handle_caller_turn(self, call_id: str, caller_text: str) -> WorkflowResult:
        session = self.sessions.get(call_id)
        session.transcript.append(f"Caller: {caller_text}")
        intent = self._classify_intent(caller_text)
        faq_key = self._faq_key(caller_text)

        if intent == Intent.TRANSFER:
            return self._handle_transfer(session, caller_text)
        if faq_key:
            return self._handle_faq(session, caller_text)
        if intent == Intent.BOOKING or session.intent == Intent.BOOKING:
            return self._handle_booking(session, caller_text)

        session.summary = f"Unclear caller request: {caller_text}"
        self.sessions.save(session)
        return self._result(
            session,
            "I can help with bookings, timings, pricing, services, parking, location, or connect you to the team. What would you like?",
            ["clarification_requested"],
        )

    def _handle_booking(self, session: CallSession, caller_text: str) -> WorkflowResult:
        session.intent = Intent.BOOKING
        session.stage = CallStage.COLLECTING
        session.booking = self._merge_booking(session.booking, caller_text, session.business.default_service)

        if not session.booking.requested_slot:
            self.sessions.save(session)
            return self._result(session, "Sure, what date and time would you like?", ["booking_slot_requested"])

        if not session.booking.caller_name:
            self.sessions.save(session)
            return self._result(session, "Got it. May I have your name for the booking?", ["booking_name_requested"])

        if not self.booking.is_available(session.business, session.booking.requested_slot):
            session.summary = f"No availability for {session.booking.requested_slot}."
            self.sessions.save(session)
            return self._result(
                session,
                "I am sorry, that slot is not available. Would you like another time?",
                ["booking_unavailable"],
            )

        booking_ref = self.booking.create_booking(session)
        session.stage = CallStage.BOOKED
        session.summary = (
            f"Booking {booking_ref}: {session.booking.service} for {session.booking.caller_name} "
            f"at {session.booking.requested_slot}. Caller: {session.caller_number}."
        )
        self.sessions.save(session)
        self._notify_owner(session, "booking_confirmation", session.summary)
        return self._result(
            session,
            (
                f"Perfect. I have booked {session.booking.service} for {session.booking.caller_name} "
                f"at {session.booking.requested_slot}. You will receive a WhatsApp confirmation shortly."
            ),
            ["booking_created", "owner_whatsapp_sent"],
        )

    def _handle_faq(self, session: CallSession, caller_text: str) -> WorkflowResult:
        session.intent = Intent.FAQ
        session.stage = CallStage.ANSWERED
        key = self._faq_key(caller_text)
        answer = session.business.faqs.get(key)
        if not answer:
            return self._handle_transfer(session, caller_text)

        session.summary = f"Answered FAQ about {key} for {session.caller_number}."
        self.sessions.save(session)
        self._notify_owner(session, "call_summary", session.summary)
        return self._result(session, answer, ["faq_answered", "owner_whatsapp_sent"])

    def _handle_transfer(self, session: CallSession, caller_text: str) -> WorkflowResult:
        session.intent = Intent.TRANSFER
        session.stage = CallStage.TRANSFERRED
        session.summary = f"Transfer requested or needed. Latest caller message: {caller_text}"
        self._notify_owner(session, "transfer_summary", session.summary)
        transfer_ref = self.telephony.transfer(session, session.business.transfer_number, session.summary)
        self.sessions.save(session)
        return self._result(
            session,
            "Let me connect you with the team. Please hold for a moment.",
            ["owner_whatsapp_sent", f"transfer_started:{transfer_ref}"],
        )

    def _notify_owner(self, session: CallSession, template: str, body: str) -> None:
        self.whatsapp.send(
            WhatsAppMessage(
                to_number=session.business.owner_number,
                template=template,
                body=body,
            )
        )

    def _result(self, session: CallSession, say: str, actions: list[str]) -> WorkflowResult:
        return WorkflowResult(
            call_id=session.call_id,
            intent=session.intent,
            stage=session.stage,
            say=say,
            actions=actions,
            summary=session.summary,
        )

    def _classify_intent(self, text: str) -> Intent:
        normalized = text.lower()
        transfer_terms = ["human", "staff", "owner", "manager", "angry", "complaint", "confused", "vip"]
        booking_terms = ["book", "appointment", "reservation", "table", "slot", "schedule"]
        faq_terms = [
            "timing",
            "hour",
            "open",
            "close",
            "parking",
            "price",
            "cost",
            "charge",
            "menu",
            "service",
            "offer",
            "available",
            "location",
            "address",
            "where",
            "landmark",
            "direction",
            "doctor",
            "stylist",
        ]

        if any(term in normalized for term in transfer_terms):
            return Intent.TRANSFER
        if any(term in normalized for term in booking_terms):
            return Intent.BOOKING
        if any(term in normalized for term in faq_terms):
            return Intent.FAQ
        return Intent.UNKNOWN

    def _merge_booking(self, booking: BookingDetails, text: str, default_service: str) -> BookingDetails:
        name_match = re.search(r"(?:my name is|under|name is)\s+([A-Za-z][A-Za-z ]{1,40})", text, re.IGNORECASE)
        time_match = re.search(
            r"((?:(?:today|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\s+"
            r"(?:at\s*)?\d{1,2}(?::\d{2})?\s*(?:am|pm)?)|"
            r"(?:at\s*\d{1,2}(?::\d{2})?\s*(?:am|pm)?))",
            text,
            re.IGNORECASE,
        )
        party_match = re.search(r"(?:for|party of)\s+(\d{1,2})", text, re.IGNORECASE)

        return BookingDetails(
            caller_name=(name_match.group(1).strip() if name_match else booking.caller_name),
            service=booking.service or default_service,
            requested_slot=(time_match.group(1).strip() if time_match else booking.requested_slot),
            party_size=(int(party_match.group(1)) if party_match else booking.party_size),
        )

    def _faq_key(self, text: str) -> str | None:
        normalized = text.lower()
        if any(term in normalized for term in ["timing", "hour", "open", "close"]):
            return "timings"
        if "parking" in normalized:
            return "parking"
        if any(term in normalized for term in ["price", "cost", "charge"]):
            return "pricing"
        if any(term in normalized for term in ["menu", "dish", "food", "vegan", "jain"]):
            return "menu"
        if any(term in normalized for term in ["service", "offer", "haircut", "facial", "spa"]):
            return "services"
        if any(term in normalized for term in ["doctor", "stylist"]):
            return "staff_availability"
        if any(term in normalized for term in ["location", "where", "address", "landmark", "direction"]):
            return "location"
        return None
