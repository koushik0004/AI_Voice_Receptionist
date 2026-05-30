# Generated Onboarding Docs

This directory contains the generated onboarding package for the repository.

## Index

1. [`01-executive-summary.md`](./01-executive-summary.md)
2. [`02-application-overview.md`](./02-application-overview.md)
3. [`03-architecture.md`](./03-architecture.md)
4. [`04-repository-map.md`](./04-repository-map.md)
5. [`05-request-lifecycle.md`](./05-request-lifecycle.md)
6. [`06-entry-points.md`](./06-entry-points.md)
7. [`07-domain-model.md`](./07-domain-model.md)
8. [`08-design-patterns.md`](./08-design-patterns.md)
9. [`09-database.md`](./09-database.md)
10. [`10-integrations.md`](./10-integrations.md)
11. [`11-learning-path.md`](./11-learning-path.md)

## Dependency Graph

The repository is organized around a single workflow core:

- FastAPI routes expose HTTP endpoints and the simulator UI.
- `ReceptionistWorkflow` owns the call logic.
- `core/ports.py` defines the boundaries for telephony, WhatsApp, booking, session state, and business lookup.
- `adapters/memory.py` provides the current in-memory implementations.
- `core/bootstrap.py` wires the demo container together.

That makes the workflow the central module, with HTTP and adapters sitting on either side.

## Glossary

- **BusinessProfile**: per-business configuration, including transfer numbers and FAQ content.
- **CallSession**: mutable state for an active call.
- **WorkflowResult**: the workflow response containing the reply, actions, and summary.
- **BookingAdapter**: booking integration contract.
- **SessionStore**: active-call state storage contract.
- **TelephonyClient**: outbound callback / transfer integration contract.
- **WhatsAppClient**: owner notification integration contract.

## Unknowns and Assumptions

### Unknowns

- Which telephony provider will be used first in production.
- Which WhatsApp provider will be used first in production.
- Whether Redis will be introduced before Postgres or alongside it.
- Which industries beyond the demo salon and restaurant will be prioritized first.

### Assumptions

- The current in-memory adapters are temporary MVP scaffolding.
- The future production stack will keep the same ports-and-adapters shape.
- The generated docs should remain aligned with the workflow-first design described in the upstream docs.

## Generated file set

The generated package is meant to be read as a set:

- sections 1-8 cover the business and technical foundation
- sections 9-11 cover storage, integrations, and onboarding order
- this README holds the cross-cutting graph, glossary, and open questions
