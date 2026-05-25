from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="AI Voice Receptionist MVP",
    version="0.1.0",
    description="Lean workflow foundation for missed calls, bookings, FAQ, transfer, and WhatsApp follow-up.",
)

app.include_router(router)

