from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field


class CallSource(StrEnum):
    INBOUND = "inbound"
    MISSED_CALLBACK = "missed_callback"


class Intent(StrEnum):
    BOOKING = "booking"
    FAQ = "faq"
    TRANSFER = "transfer"
    UNKNOWN = "unknown"


class CallStage(StrEnum):
    STARTED = "started"
    COLLECTING = "collecting"
    BOOKED = "booked"
    ANSWERED = "answered"
    TRANSFERRED = "transferred"
    CLOSED = "closed"


class CallEvent(BaseModel):
    business_id: str
    call_id: str
    caller_number: str
    source: CallSource = CallSource.INBOUND
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BookingDetails(BaseModel):
    caller_name: str | None = None
    service: str | None = None
    requested_slot: str | None = None
    party_size: int | None = None

    @property
    def is_complete(self) -> bool:
        return bool(self.caller_name and self.requested_slot)


class BusinessProfile(BaseModel):
    business_id: str
    name: str
    owner_number: str
    transfer_number: str
    industry: str
    faqs: dict[str, str]
    default_service: str


class CallSession(BaseModel):
    call_id: str
    business: BusinessProfile
    caller_number: str
    source: CallSource
    stage: CallStage = CallStage.STARTED
    intent: Intent = Intent.UNKNOWN
    booking: BookingDetails = Field(default_factory=BookingDetails)
    transcript: list[str] = Field(default_factory=list)
    summary: str = ""


class WorkflowResult(BaseModel):
    call_id: str
    intent: Intent
    stage: CallStage
    say: str
    actions: list[str] = Field(default_factory=list)
    summary: str = ""


class WhatsAppMessage(BaseModel):
    to_number: str
    template: str
    body: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

