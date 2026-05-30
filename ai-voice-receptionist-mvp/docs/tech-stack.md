# Tech Stack

## Current stack (MVP)

- **Language**: Python `>=3.11`
- **Web framework**: FastAPI
- **Data models**: Pydantic v2
- **ASGI server**: Uvicorn
- **Testing**: pytest + FastAPI TestClient

From upstream `pyproject.toml`:

- runtime deps: `fastapi`, `pydantic`, `uvicorn[standard]`
- dev deps: `pytest`, `httpx`

## Architecture patterns

- Ports-and-adapters (clean boundaries around integrations)
- Deterministic workflow orchestration
- In-memory adapters used as a “simulation environment”

## Planned integrations (behind ports)

The upstream docs recommend implementing providers behind `app/core/ports.py`:

- **Telephony**: Exotel first, Plivo fallback
- **WhatsApp**: WhatsApp Business provider adapter
- **Session store**: Redis-backed `SessionStore`
- **Durable storage**: Postgres-backed business profiles + bookings + call records
- **Bookings**: calendar/CRM adapter (per industry)

## AI/voice roadmap (future)

Once live call streaming begins:

- **STT** (English): Deepgram or Google
- **STT** (Hindi/Kannada): Sarvam AI
- **TTS** (Hindi): Sarvam AI
- **TTS** (English premium): ElevenLabs
- **LLM**: small/fast model for routing + constrained extraction

The MVP should keep the workflow deterministic, using AI components primarily for:

- intent classification (bounded labels)
- entity extraction (bounded schema)
- summarization for owner notifications (bounded length)

