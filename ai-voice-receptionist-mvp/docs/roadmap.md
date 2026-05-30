# Roadmap

## Near-term (recommended implementation order)

1. **Telephony provider adapter**
   - Replace `LocalTelephonyClient` with Exotel or Plivo implementation behind `TelephonyClient`.
   - Implement webhook verification and retry/idempotency strategy.
2. **Redis SessionStore**
   - Replace `InMemorySessionStore` with Redis-backed `SessionStore` with TTL.
3. **Postgres persistence**
   - Business profiles (multi-tenant config), call records, bookings.
4. **WhatsApp provider adapter**
   - Replace `LocalWhatsAppClient` with WhatsApp Business provider integration.
5. **Real-time audio support**
   - Add WebSocket audio streaming endpoints once telephony choice is finalized.

## Next (AI + product)

- Add **STT/TTS** ports and one initial provider per language.
- Add **bounded extraction** for bookings (schema-first) and robust multilingual parsing.
- Add **operator console** for call monitoring and handoff.
- Add **industry templates** (salon/clinic/restaurant) for faster onboarding.

## Deferred by design (non-goals for MVP)

- RAG ingestion pipelines (PDF/menu scraping, vector DB, etc.)
- Fine-tuning / custom personalities / voice cloning
- Heavy multi-tenant platform work
- Advanced CRM integrations
- GPU autoscaling

