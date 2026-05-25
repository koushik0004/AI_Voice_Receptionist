from dataclasses import dataclass

from app.adapters.memory import (
    InMemoryBookingAdapter,
    InMemoryBusinessRepository,
    InMemorySessionStore,
    LocalTelephonyClient,
    LocalWhatsAppClient,
)
from app.workflows.receptionist import ReceptionistWorkflow


@dataclass
class Container:
    workflow: ReceptionistWorkflow
    whatsapp: LocalWhatsAppClient


def build_demo_container() -> Container:
    businesses = InMemoryBusinessRepository.demo()
    sessions = InMemorySessionStore()
    telephony = LocalTelephonyClient()
    whatsapp = LocalWhatsAppClient()
    booking = InMemoryBookingAdapter()
    workflow = ReceptionistWorkflow(
        businesses=businesses,
        sessions=sessions,
        telephony=telephony,
        whatsapp=whatsapp,
        booking=booking,
    )
    return Container(workflow=workflow, whatsapp=whatsapp)

