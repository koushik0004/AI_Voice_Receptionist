# Repository Summary — `AI_Voice_Receptionist`

## Purpose

This repository hosts a lean MVP foundation for an **India-first AI Voice Receptionist** focused on validating real SME workflows before investing in heavy platform work (RAG ingestion, dashboards, fine-tuning, multi-tenant infra, GPU autoscaling).

The implemented MVP scope centers on:

1. Missed call recovery
2. Appointment / table booking
3. Structured FAQ answering
4. Human transfer
5. WhatsApp follow-up trail for the owner

## Architecture

The MVP is designed as a **workflow orchestrator** (not an autonomous agent system), using a ports-and-adapters approach:

- **FastAPI** exposes webhook endpoints and a built-in “Call Simulator” web UI.
- A single orchestrator, `ReceptionistWorkflow`, drives call state transitions and decisions.
- External systems (telephony, WhatsApp, booking, persistence) are abstracted behind ports (protocols) so providers can be swapped in later.
- Current integrations are simulated using in-memory/local adapters.

## Tech stack

- Python `>=3.11`
- FastAPI (HTTP API + webhook surface)
- Pydantic v2 (domain/request/response models)
- Uvicorn (ASGI server)
- pytest + FastAPI TestClient (tests)

## Modules (upstream structure)

Upstream code is organized under `ai-voice-receptionist-mvp/`:

- `app/core/models.py`: domain objects (`CallSession`, `BusinessProfile`, `WorkflowResult`, enums)
- `app/core/ports.py`: integration contracts (`TelephonyClient`, `WhatsAppClient`, `BookingAdapter`, `SessionStore`, `BusinessRepository`)
- `app/core/bootstrap.py`: demo container wiring (`build_demo_container`)
- `app/adapters/memory.py`: in-memory/local implementations of the ports
- `app/workflows/receptionist.py`: deterministic workflow orchestration (intent, FAQ routing, booking collection, transfer)
- `app/api/routes.py`: HTTP routes, embedded simulator UI, and debug outbox endpoint
- `tests/`: workflow and API surface tests

## Workflow (behavior)

- **Inbound call start**
  - `POST /webhooks/telephony/inbound-call` creates a `CallSession` and returns a greeting.
- **Caller turn**
  - `POST /calls/{call_id}/turn` updates transcript and routes the turn:
    - transfer intent (or unknown FAQ) → WhatsApp summary → telephony transfer
    - known FAQ → answer from `BusinessProfile.faqs` → WhatsApp summary
    - booking intent or booking-in-progress → collect slot then name → availability check → booking creation → WhatsApp confirmation
- **Missed call recovery**
  - `POST /webhooks/telephony/missed-call` triggers outbound callback and sends an owner WhatsApp notification.

## Integrations

**Current (demo mode)**:

- Telephony, WhatsApp, booking, and session storage are implemented as local/in-memory adapters for simulation and tests.

**Planned (behind ports)**:

- Telephony: Exotel or Plivo
- Session store: Redis
- Durable storage: Postgres (business profiles, bookings, call records)
- WhatsApp: WhatsApp Business provider adapter
- Later: real-time audio streaming + STT/TTS/LLM providers, kept behind ports with bounded outputs feeding the workflow.

## Deployment flow (intended)

The MVP is intended to run as a simple HTTP service that receives provider webhooks. As it moves beyond demo mode, the expected production shape becomes:

- FastAPI service
- Redis for active call session state (TTL + cleanup)
- Postgres for durable records
- Telephony provider webhooks + outbound callback/transfer APIs
- WhatsApp provider for owner notifications

