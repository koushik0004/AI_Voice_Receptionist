# Real MVP Scope

## The Five Workflows

### 1. Missed Call Recovery

When a customer call is missed, the system should trigger an outbound callback within 10-20 seconds, start the same voice workflow, and notify the owner on WhatsApp.

MVP behavior in code:

- `POST /webhooks/telephony/missed-call`
- queues callback through `TelephonyClient`
- sends owner WhatsApp summary through `WhatsAppClient`

### 2. Appointment / Table Booking

For salons, clinics, and restaurants, the first version only needs slot collection, availability check, booking creation, and WhatsApp notification.

MVP behavior in code:

- deterministic slot collection
- in-memory booking adapter
- owner WhatsApp confirmation

### 3. FAQ Answering

Use structured FAQs per business. Avoid full RAG until customer onboarding proves the need.

MVP behavior in code:

- FAQ keys such as `timings`, `parking`, `pricing`, `menu`, `location`
- answer only from configured structured data
- transfer when answer is unknown

### 4. Human Transfer

Trust depends on quick escape hatches.

MVP behavior in code:

- transfer when caller asks for staff, manager, owner, or human
- transfer on unknown FAQ
- WhatsApp summary is sent before transfer

### 5. WhatsApp Follow-up

Every meaningful call event should leave a WhatsApp trail for the SME owner.

MVP behavior in code:

- missed call recovery summary
- booking confirmation
- FAQ call summary
- transfer summary

## V1 Non-Goals

- Full analytics dashboard
- RAG ingestion
- Fine-tuned LLM
- Voice cloning
- Custom AI personalities
- Tone/emotion AI
- Heavy multi-tenant architecture
- Advanced CRM integrations
- GPU autoscaling

## Provider Choices

Recommended first integrations:

- Telephony: Exotel first, Plivo fallback
- English STT: Deepgram or Google
- Hindi/Kannada STT: Sarvam AI
- Hindi TTS: Sarvam AI
- English premium TTS: ElevenLabs
- LLM: GPT-4.1-mini or Gemini Flash

Provider integrations should be implemented behind the existing ports in `app/core/ports.py`.

