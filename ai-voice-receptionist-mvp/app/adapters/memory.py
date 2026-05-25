from app.core.models import BusinessProfile, CallSession, WhatsAppMessage


class InMemoryBusinessRepository:
    def __init__(self, businesses: dict[str, BusinessProfile]) -> None:
        self._businesses = businesses

    @classmethod
    def demo(cls) -> "InMemoryBusinessRepository":
        return cls(
            {
                "demo-salon": BusinessProfile(
                    business_id="demo-salon",
                    name="Namma Glow Salon",
                    owner_number="+919900000001",
                    transfer_number="+919900000002",
                    industry="salon",
                    default_service="salon appointment",
                    faqs={
                        "timings": "We are open from 10 AM to 8 PM, Monday to Sunday.",
                        "parking": "Two-wheeler parking is available outside, and car parking is available in the basement.",
                        "pricing": "Haircuts start at Rs 500, facials start at Rs 1,200, and bridal packages are shared by staff.",
                        "location": "We are near Indiranagar Metro Station, Bengaluru.",
                        "services": "We offer haircuts, hair spa, facials, waxing, threading, and bridal packages.",
                        "staff_availability": "Stylist availability changes by day. I can connect you to the team or help book a slot.",
                    },
                ),
                "demo-restaurant": BusinessProfile(
                    business_id="demo-restaurant",
                    name="Masala Table",
                    owner_number="+919900000011",
                    transfer_number="+919900000012",
                    industry="restaurant",
                    default_service="table booking",
                    faqs={
                        "timings": "We are open from noon to 11 PM every day.",
                        "parking": "Valet parking is available from 7 PM onwards.",
                        "pricing": "Most main course dishes are between Rs 280 and Rs 550.",
                        "menu": "We serve North Indian, coastal, and vegetarian options. Jain food is available on request.",
                        "location": "We are on 12th Main, Indiranagar, close to the metro station.",
                        "services": "We handle table bookings, takeaway queries, private dining requests, and menu questions.",
                    },
                ),
            }
        )

    def get(self, business_id: str) -> BusinessProfile:
        return self._businesses[business_id]


class InMemorySessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, CallSession] = {}

    def save(self, session: CallSession) -> None:
        self._sessions[session.call_id] = session

    def get(self, call_id: str) -> CallSession:
        return self._sessions[call_id]


class LocalTelephonyClient:
    def __init__(self) -> None:
        self.callbacks: list[tuple[str, str]] = []
        self.transfers: list[tuple[str, str, str]] = []

    def call_back(self, to_number: str, from_business: BusinessProfile) -> str:
        ref = f"local-callback-{len(self.callbacks) + 1}"
        self.callbacks.append((to_number, from_business.business_id))
        return ref

    def transfer(self, session: CallSession, to_number: str, summary: str) -> str:
        ref = f"local-transfer-{len(self.transfers) + 1}"
        self.transfers.append((session.call_id, to_number, summary))
        return ref


class LocalWhatsAppClient:
    def __init__(self) -> None:
        self.messages: list[WhatsAppMessage] = []

    def send(self, message: WhatsAppMessage) -> None:
        self.messages.append(message)


class InMemoryBookingAdapter:
    def __init__(self) -> None:
        self.bookings: dict[str, CallSession] = {}

    def is_available(self, business: BusinessProfile, requested_slot: str) -> bool:
        normalized = requested_slot.lower()
        return "unavailable" not in normalized and "closed" not in normalized

    def create_booking(self, session: CallSession) -> str:
        ref = f"bk-{len(self.bookings) + 1:04d}"
        self.bookings[ref] = session
        return ref
