# AI Voice Receptionist MVP

Lean foundation for an India-first AI voice receptionist focused on the first five workflows:

1. Missed call recovery
2. Appointment or table booking
3. Structured FAQ answering
4. Human transfer
5. WhatsApp follow-up

The goal is not a full voice platform yet. This codebase starts with deterministic workflow orchestration, provider ports, and local adapters so we can validate real SME workflows before adding complex RAG, custom dashboards, fine-tuning, or GPU infrastructure.

## Stack Direction

- Backend: Python FastAPI
- Active call state: Redis later, in-memory adapter now
- Durable records: Postgres later, in-memory adapter now
- Telephony: Exotel or Plivo port, local adapter now
- STT/TTS: provider ports for Deepgram/Google/Sarvam/ElevenLabs
- LLM: small fast model port, deterministic local router now
- Follow-up: WhatsApp provider port, local adapter now

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Simulate an inbound call:

```bash
curl -X POST http://127.0.0.1:8000/webhooks/telephony/inbound-call \
  -H "Content-Type: application/json" \
  -d '{"business_id":"demo-salon","call_id":"call-1","caller_number":"+919900001111"}'
```

Send a caller utterance:

```bash
curl -X POST http://127.0.0.1:8000/calls/call-1/turn \
  -H "Content-Type: application/json" \
  -d '{"text":"Can I book a haircut tomorrow at 5 pm? My name is Sneha."}'
```

Simulate missed-call recovery:

```bash
curl -X POST http://127.0.0.1:8000/webhooks/telephony/missed-call \
  -H "Content-Type: application/json" \
  -d '{"business_id":"demo-salon","call_id":"missed-1","caller_number":"+919900001111"}'
```

## What Is Intentionally Deferred

- Analytics dashboard
- PDF/menu ingestion and full RAG
- Fine-tuned LLM
- Voice cloning
- Heavy multi-tenant platform work
- Advanced CRM integrations
- GPU autoscaling

