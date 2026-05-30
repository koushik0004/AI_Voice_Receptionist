# Single-file prompt: Application Overview

Use GitHub MCP.

Read repository:

owner: snehashisc
repo: AI_Voice_Receptionist

This prompt is for generating only:

- `docs/generated-onboarding/02-application-overview.md`

If you want the full multi-file onboarding documentation workflow in Codex CLI, run:

- `.codex/prompts/run-onboarding-docs-fanout.md`

Do not generate the entire onboarding package from this prompt.

# Section scope

Generate only the content for section 2 from `.codex/prompts/master-onboarding-docs.md`:

- `What the Application Looks Like When Running`

# Requirements

- Use markdown.
- Focus on user-facing behavior, workflows, navigation, major pages, APIs, services, jobs, and integrations.
- Clearly label assumptions.
- Optimize for onboarding and maintainability rather than code-level completeness.
- Do not create or update any other generated onboarding file.
