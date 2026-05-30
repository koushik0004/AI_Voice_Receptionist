# API & Flow

## HTTP surface (upstream)

The MVP exposes:

- `GET /health` — health check
- `GET /` — built-in “Call Simulator” UI
- `POST /webhooks/telephony/inbound-call` — start an inbound call session
- `POST /webhooks/telephony/missed-call` — trigger missed-call recovery callback flow
- `POST /calls/{call_id}/turn` — submit a caller “turn” (utterance text) and receive workflow response
- `GET /debug/whatsapp-outbox` — inspect simulated WhatsApp outbox (demo mode)

## Sequence: inbound call start

```mermaid
sequenceDiagram
  participant Tel as Telephony Provider
  participant API as FastAPI
  participant WF as ReceptionistWorkflow
  participant Store as SessionStore

  Tel->>API: POST /webhooks/telephony/inbound-call
  API->>WF: handle_call_started(CallEvent)
  WF->>Store: save(CallSession)
  WF-->>API: WorkflowResult(say=greeting, actions=[call_started])
  API-->>Tel: 200 JSON
```

## Sequence: missed-call recovery

```mermaid
sequenceDiagram
  participant Tel as Telephony Provider
  participant API as FastAPI
  participant WF as ReceptionistWorkflow
  participant TC as TelephonyClient
  participant WA as WhatsAppClient
  participant Store as SessionStore

  Tel->>API: POST /webhooks/telephony/missed-call
  API->>WF: handle_missed_call(CallEvent)
  WF->>TC: call_back(caller_number, business)
  WF->>Store: save(CallSession)
  WF->>WA: send(missed_call_recovery summary)
  WF-->>API: WorkflowResult(actions=[callback_queued, owner_whatsapp_sent])
  API-->>Tel: 200 JSON
```

## Sequence: caller turn (booking / FAQ / transfer)

```mermaid
sequenceDiagram
  participant Caller
  participant API as FastAPI
  participant WF as ReceptionistWorkflow
  participant Store as SessionStore
  participant Book as BookingAdapter
  participant WA as WhatsAppClient
  participant Tel as TelephonyClient

  Caller->>API: POST /calls/{call_id}/turn (text)
  API->>WF: handle_caller_turn(call_id, text)
  WF->>Store: get(call_id)
  alt Transfer intent OR unknown FAQ
    WF->>WA: send(transfer_summary)
    WF->>Tel: transfer(session, transfer_number, summary)
    WF->>Store: save(session)
    WF-->>API: WorkflowResult(stage=TRANSFERRED)
  else FAQ resolved
    WF->>WA: send(call_summary)
    WF->>Store: save(session)
    WF-->>API: WorkflowResult(stage=ANSWERED)
  else Booking flow
    WF->>Book: is_available(...)
    WF->>Book: create_booking(session)
    WF->>WA: send(booking_confirmation)
    WF->>Store: save(session)
    WF-->>API: WorkflowResult(stage=BOOKED)
  end
  API-->>Caller: 200 JSON (say + actions)
```

## Notes on “AI”

In the MVP, intent detection and extraction are deterministic (keywords + regex) and produce bounded outputs that the workflow uses to decide the next step.

