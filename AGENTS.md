# AGENTS

## Scope

- This file applies to the repository root `/Users/bytedance/aurora-agent` and all of its subdirectories.
- This repository is a small Python Agent project built on LangChain, LangGraph, and DeepSeek model integrations.

## Project Structure

```text
.
├── .agents/
│   └── skills/
│       └── project-agents-maintainer/
│           └── SKILL.md
├── src/
│   ├── agents/
│   │   └── general_agent.py
│   ├── models/
│   │   └── patched_deepseek.py
│   └── tools/
│       └── bash_tool.py
├── Makefile
├── langgraph.json
├── main.py
├── pyproject.toml
└── uv.lock
```

## Module Responsibilities

- `src/agents/general_agent.py`
  - Defines `create_general_agent()`, which assembles the model, tools, and system prompt.
- `src/models/patched_deepseek.py`
  - Defines `PatchedChatDeepSeek`, which fixes `reasoning_content` propagation in multi-turn conversations.
- `src/tools/bash_tool.py`
  - Defines an asynchronous Bash tool used by the Agent to invoke system commands as a tool.
- `.agents/skills/project-agents-maintainer/SKILL.md`
  - Defines the project-local skill used to refresh and maintain this `AGENTS.md` from repository evidence.
- `langgraph.json`
  - Defines the LangGraph local development entrypoint. The current graph is `general_agent`.
- `main.py`
  - Minimal manual debugging entrypoint for directly invoking the model and verifying basic connectivity.

## Code Style

- Prefer minimal changes first; do not add new entities or spread responsibilities unless necessary.
- Keep the code highly cohesive and loosely coupled, with clear separation across `agents`, `models`, and `tools`.
- Prefer programming around interfaces and responsibility boundaries. Do not mix tool logic, model adaptation logic, and Agent assembly logic in the same file.
- Follow the existing Python style:
  - Use type annotations.
  - Use concise but complete docstrings, especially for tool functions and model patch classes.
  - Keep imports simple and direct. Do not introduce unnecessary abstraction or reshuffling.
  - Write comments only when they add real context. Avoid obvious comments.
- For the `tool` decorator, use the repository-validated form `@tool("name", parse_docstring=True)`. Do not use the `name=` keyword argument.
- Bash execution tools must be asynchronous and use `asyncio.create_subprocess_shell` to avoid blocking the event loop.
- Keep the Bash tool return contract stable:
  - Return `stdout` on success.
  - Return readable error information on failure, preferably `stderr`, with exit code information when needed.
- For model secrets, environment variables, and external configuration, prefer environment-based configuration. Do not expand the use of hard-coded sensitive values in new code.

## Prompting Style

- System prompts should use a structured, machine-readable style, preferably with XML-like sections such as:
  - `<identity>`
  - `<workspace>`
  - other explicit constraint sections
- Keep prompts short, precise, and actionable. Avoid long background-heavy instructions.
- State the workspace root path, identity, boundaries, and tool constraints explicitly so the model acts within repository context first.
- For tool-oriented prompts, state these four things clearly:
  - What the goal is.
  - What the executable root directory is.
  - Which tools are allowed or preferred.
  - What constraints the output must satisfy.
- When adding engineering rules, prefer concrete and verifiable constraints over abstract slogans.

## Local Commands

- Install dependencies

```bash
make install
```

- Equivalent command

```bash
uv sync
```

- Start the LangGraph local development server

```bash
make dev
```

- Equivalent command

```bash
uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.13 langgraph dev --allow-blocking
```

- Run the minimal debugging entrypoint directly

```bash
python3 main.py
```

- Verify that the graph entrypoint can be imported

```bash
python3 -c "from src.agents.general_agent import create_general_agent; print('import ok')"
```

## Development Constraints

- When modifying `src/agents/`, make sure the system prompt, tool registration, and model initialization still match.
- When modifying `src/models/`, keep the patch scope minimal. Fix adaptation issues without changing upper-layer Agent semantics.
- When modifying `src/tools/`, keep tool signatures clear, return values stable, and error handling readable.
- Before adding a new tool, confirm that a new file is actually necessary. Reuse existing modules when possible.
- Run at least one import validation before submitting changes. If tool or Agent assembly logic changed, prioritize verifying that `general_agent` still loads successfully.

## Current Known Constraints

- Python version should be treated as `3.13`, and the LangGraph entrypoint is defined in `langgraph.json`.
- The repository does not yet have a complex multi-module structure, so confirm real need before adding new directories.
- `README.md` is currently empty. Do not move Agent-oriented constraints into the README; maintain this file as the primary source instead.

## Recent Changes

- The repository currently has no Git commit history yet, so this section reflects observed current state rather than commit-derived history.
- The project now includes a project-local skill at `.agents/skills/project-agents-maintainer/SKILL.md` to keep this file aligned with repository reality.
- The current handbook reflects the present Python/LangGraph layout, local commands, prompting style, and repository-specific tool conventions.

## AGENTS Maintenance

- Use the project-local skill in `.agents/skills/project-agents-maintainer/` whenever the user asks to create, refresh, audit, or update `AGENTS.md`.
- Before editing this file, inspect the current repository structure, key entry files, local commands, and project-local skills.
- Always check recent commits with `git log --oneline -n 10` before updating the `Recent Changes` section.
- If there are still no commits, say so explicitly. Do not invent repository history.
- Prefer updating this file in place. Keep it concise, specific, and grounded in the current repository.
