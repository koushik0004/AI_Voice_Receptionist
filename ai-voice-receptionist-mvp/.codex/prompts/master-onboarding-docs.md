# Repository Understanding and Architecture Documentation

Use GitHub MCP.

Read repository:

owner: snehashisc
repo: AI_Voice_Receptionist

You are acting as a senior software architect, technical writer, and onboarding mentor.

You have full access to the repository through GitHub.

Your task is NOT to merely summarize files.

Your task is to help a new engineer understand the application from the outside-in and then from the inside-out.

Assume:

* The reader did not build this system.
* The reader does not understand the codebase.
* The reader wants to become productive in maintaining and extending it.
* The reader may not even understand the business purpose of the application.

Generate a comprehensive documentation package with the following sections.

---

# 1. Executive Summary

Explain:

* What problem this application solves.
* Who the intended users are.
* What the application appears to do.
* The major business capabilities.

Avoid implementation details.

Write this section for a non-technical person.

---

# 2. What the Application Looks Like When Running

Based on the codebase:

* Infer the user-facing screens.
* Infer the workflows available to users.
* Infer the navigation structure.
* Infer major pages, APIs, services, jobs, or integrations.

If the application has a frontend:

Describe the likely UI and user journey.

If the application is API-only:

Describe how consumers interact with it.

If assumptions are required:

Clearly label them as assumptions.

---

# 3. High-Level Architecture

Produce:

* System overview
* Main components
* Major modules
* External dependencies
* Third-party services
* Databases
* Queues
* Background jobs

Include Mermaid diagrams whenever possible.

Example:

* User
* Frontend
* Backend
* Database
* External services

Show how data flows between them.

---

# 4. Repository Map

Explain the repository structure.

For every major folder:

* Purpose
* Responsibility
* Important files
* Why it exists

Create a table:

| Path | Purpose | Importance |
| ---- | ------- | ---------- |

Highlight the folders a new engineer should read first.

---

# 5. Request Lifecycle

Choose a representative user action.

Trace it through the codebase.

For example:

User clicks button
→ frontend handler
→ API endpoint
→ service layer
→ repository layer
→ database
→ response

Show actual file names and functions involved.

Provide at least 3 important user journeys.

---

# 6. Entry Points

Identify:

* Main application entry point
* Startup sequence
* Dependency initialization
* Configuration loading
* Routing setup

Explain:

"What happens first when the application starts?"

Provide a step-by-step walkthrough.

---

# 7. Core Domain Concepts

Identify:

* Main business entities
* Domain models
* Aggregates
* Resources

For each:

* Purpose
* Relationships
* Where implemented

Explain the business language of the system.

---

# 8. Design Patterns and Architecture Patterns

Identify patterns such as:

* Adapter
* Repository
* Service Layer
* CQRS
* Event Driven
* Hexagonal Architecture
* Clean Architecture
* MVC
* Dependency Injection

For each pattern found:

* Explain where it exists
* Explain why it was likely used
* Point to files implementing it

---

# 9. Dependency Graph

Explain:

* Which modules depend on which modules
* Which modules are central
* Which modules are isolated

Identify:

* Tight coupling
* Potential architectural risks

---

# 10. Database Understanding

Document:

* Main tables
* Relationships
* Data lifecycle

Explain:

* How data enters the system
* How it is stored
* How it is retrieved

Include diagrams when possible.

---

# 11. Integrations and Adapters

Identify every external integration.

Examples:

* GitHub
* Stripe
* AWS
* OpenAI
* Email providers
* Message queues

For each integration:

* Why it exists
* Which files implement it
* How the integration flows through the system

Create a dedicated section called:

"Adapter and Integration Guide"

---

# 12. Reading Order for New Engineers

Create a learning path.

Example:

Day 1:

* Read X
* Read Y

Day 2:

* Read A
* Read B

Day 3:

* Follow request lifecycle

Provide a recommended order for understanding the system.

---

# 13. Glossary

Create a glossary of:

* Business terms
* Technical terms
* Internal naming conventions

Explain each in plain English.

---

# 14. Unknowns and Assumptions

List:

* Areas that could not be determined
* Ambiguous design choices
* Missing context

Do not invent facts.

Clearly separate facts from assumptions.

---

# Output Requirement

Generate the documentation as a set of Markdown files:

docs/
|-- generated-onboarding/
  ├── 01-executive-summary.md
  ├── 02-application-overview.md
  ├── 03-architecture.md
  ├── 04-repository-map.md
  ├── 05-request-lifecycle.md
  ├── 06-entry-points.md
  ├── 07-domain-model.md
  ├── 08-design-patterns.md
  ├── 09-database.md
  ├── 10-integrations.md
  ├── 11-learning-path.md
  └── README.md

The documentation should optimize for understanding, onboarding, and maintainability rather than code-level completeness.
