Use GitHub MCP and `multi_agent_v1`.

Read repository:

owner: snehashisc
repo: AI_Voice_Receptionist

# Parent Agent for Onboarding Documentation Fanout

You are the manual parent orchestrator for generating onboarding documentation in Codex CLI.

This prompt is intended to be run manually by a human in Codex CLI.

Do not generate the full documentation package in a single response.

Your job is to:

1. Read `.codex/prompts/master-onboarding-docs.md`
2. Parse the numbered sections in that file
3. Map each output file to its assigned section(s)
4. Spawn one sub-agent per output file using `multi_agent_v1.spawn_agent`
5. Force every spawned sub-agent to use model `gpt-5.4`
6. Give each spawned sub-agent only:
   - the repository identity
   - the exact section text it owns
   - the output file path it owns
   - the shared writing rules below
7. Wait for all sub-agents to complete with `multi_agent_v1.wait_agent`
8. Ensure the generated files are written under `docs/generated-onboarding/`

## Critical orchestration rules

- Spawn exactly one sub-agent per output file.
- Use `agent_type: worker` for every spawned sub-agent.
- Use `model: gpt-5.4` for every spawned sub-agent.
- Do not let any sub-agent own more than one output file.
- Do not let multiple sub-agents write the same file.
- Do not send the entire master prompt as one prompt to one generator agent.
- Each sub-agent must work only on its own file and must not edit any sibling file.
- If a file already exists, update it in place rather than creating duplicate files.

## Shared writing rules for every spawned sub-agent

- Use markdown.
- Optimize for onboarding and maintainability.
- Be concrete and repository-grounded.
- Do not invent facts; label assumptions clearly.
- Avoid duplicating content that belongs in other generated files.
- Include Mermaid diagrams where relevant.
- Keep the document focused on the assigned section(s) only.

## Fixed section-to-file mapping

- `docs/generated-onboarding/01-executive-summary.md` ← section 1 `Executive Summary`
- `docs/generated-onboarding/02-application-overview.md` ← section 2 `What the Application Looks Like When Running`
- `docs/generated-onboarding/03-architecture.md` ← section 3 `High-Level Architecture`
- `docs/generated-onboarding/04-repository-map.md` ← section 4 `Repository Map`
- `docs/generated-onboarding/05-request-lifecycle.md` ← section 5 `Request Lifecycle`
- `docs/generated-onboarding/06-entry-points.md` ← section 6 `Entry Points`
- `docs/generated-onboarding/07-domain-model.md` ← section 7 `Core Domain Concepts`
- `docs/generated-onboarding/08-design-patterns.md` ← section 8 `Design Patterns and Architecture Patterns`
- `docs/generated-onboarding/09-database.md` ← section 10 `Database Understanding`
- `docs/generated-onboarding/10-integrations.md` ← section 11 `Integrations and Adapters`
- `docs/generated-onboarding/11-learning-path.md` ← section 12 `Reading Order for New Engineers`
- `docs/generated-onboarding/README.md` ← sections 9 `Dependency Graph`, 13 `Glossary`, and 14 `Unknowns and Assumptions`, plus a short index of all generated files

## Sub-agent prompt contract

For each spawned sub-agent, provide a prompt that contains:

- repository identity:
  - owner: `snehashisc`
  - repo: `AI_Voice_Receptionist`
- the exact target output path
- the exact source section text copied from `.codex/prompts/master-onboarding-docs.md`
- the shared writing rules
- a hard ownership statement:
  - "You own only `<target-file>`."
  - "Do not create or edit any other generated onboarding file."
  - "If `<target-file>` exists, update it in place."

## Completion criteria

The run is complete only when:

- all 12 target files above have been handled
- every source section from the master file is assigned exactly once
- `README.md` contains:
  - a short index of the generated onboarding docs
  - dependency graph content
  - glossary content
  - unknowns and assumptions content

## Manual usage

This is the manual entrypoint prompt for Codex CLI.

Run this prompt directly when you want the parent agent to orchestrate the onboarding doc generation workflow.
