# Project Overview — AI Voice Receptionist (MVP)

## Purpose

This repository contains a **Lean MVP foundation** for an *India-first AI Voice Receptionist* focused on validating real SME workflows before investing in heavy platform work (RAG ingestion, dashboards, fine-tuning, multi-tenant infra, etc.).

The MVP is intentionally **workflow-first**: deterministic orchestration + clean provider “ports”, with **local/in-memory adapters** to simulate integrations while the team locks in real vendors.

## MVP workflows (today)

1. **Missed call recovery**: trigger outbound callback quickly and notify the owner on WhatsApp.
2. **Appointment / table booking**: collect slot + name, check availability, create booking, notify owner.
3. **Structured FAQ answering**: answer from a configured per-business FAQ map (no RAG yet).
4. **Human transfer**: fast “escape hatch” to staff; send owner summary before transfer.
5. **WhatsApp follow-up trail**: key events produce owner-facing WhatsApp messages.

## What this MVP is (and is not)

- This is a **workflow orchestrator**, not an autonomous multi-agent system.
- “AI” is currently mostly **routing + structured responses**; provider ports exist for future STT/TTS/LLM integrations.
- Durable storage and streaming audio are **deferred**; the current implementation uses in-memory stores and a web UI to simulate call flows.

## Repository layout (upstream)

The upstream code lives under `ai-voice-receptionist-mvp/`.

```text
AI_Voice_Receptionist/
└─ ai-voice-receptionist-mvp/
   ├─ app/
   │  ├─ api/                 # FastAPI routes + webhook surface + test console UI
   │  ├─ core/                # Domain models + ports + bootstrap wiring
   │  ├─ adapters/            # In-memory/local adapters (telephony, WhatsApp, bookings, session store)
   │  └─ workflows/           # Deterministic receptionist workflow orchestration
   ├─ docs/                   # Upstream docs (architecture + MVP scope)
   ├─ tests/                  # Workflow + API surface tests
   └─ pyproject.toml          # Python deps (FastAPI, Pydantic, Uvicorn) + pytest extras
```

## Local development (from upstream README)

The MVP is a FastAPI app with a test console UI at `/`.

Typical local run steps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

## Key concepts

- **BusinessProfile**: per-business configuration including transfer numbers + structured FAQs.
- **CallSession**: mutable call state stored in `SessionStore`.
- **Ports**: interfaces for Telephony, WhatsApp, Bookings, and repositories.
- **ReceptionistWorkflow**: deterministic policy that updates session state and emits a `WorkflowResult` (`say` + `actions` + `summary`).

