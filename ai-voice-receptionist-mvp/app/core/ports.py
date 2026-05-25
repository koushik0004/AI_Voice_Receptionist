from typing import Protocol

from app.core.models import BusinessProfile, CallSession, WhatsAppMessage


class BusinessRepository(Protocol):
    def get(self, business_id: str) -> BusinessProfile:
        """Return a business profile or raise KeyError."""


class SessionStore(Protocol):
    def save(self, session: CallSession) -> None:
        """Persist active call session state."""

    def get(self, call_id: str) -> CallSession:
        """Return active call session state or raise KeyError."""


class TelephonyClient(Protocol):
    def call_back(self, to_number: str, from_business: BusinessProfile) -> str:
        """Place outbound callback and return provider call reference."""

    def transfer(self, session: CallSession, to_number: str, summary: str) -> str:
        """Transfer the active call and return provider transfer reference."""


class WhatsAppClient(Protocol):
    def send(self, message: WhatsAppMessage) -> None:
        """Send a WhatsApp message."""


class BookingAdapter(Protocol):
    def is_available(self, business: BusinessProfile, requested_slot: str) -> bool:
        """Check whether the requested slot is available."""

    def create_booking(self, session: CallSession) -> str:
        """Create a booking and return booking reference."""

