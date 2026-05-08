---
name: project-agents-maintainer
description: Maintain the root AGENTS.md for this repository. Use this skill whenever the user asks to create, update, refresh, rewrite, or audit AGENTS.md, project agent rules, repository conventions, prompting style, local commands, or development constraints. Also use it when the user asks to reflect recent commits or recent project changes in AGENTS.md.
---

# Project AGENTS Maintainer

Maintain `/Users/bytedance/aurora-agent/AGENTS.md` as the canonical agent-facing project handbook for this repository.

## Goal

Keep `AGENTS.md` accurate, concise, and grounded in the actual repository state.

## Repository-Specific Scope

This repository currently contains:

- `src/agents/` for agent assembly
- `src/models/` for model adaptation
- `src/tools/` for tool implementations
- `Makefile`, `langgraph.json`, `main.py`, `pyproject.toml`, and `uv.lock`
- project-local skills under `.agents/skills/`

## When Updating AGENTS.md

Always gather evidence before editing.

1. Inspect the current repository structure from the root.
2. Read the existing `AGENTS.md`.
3. Read the key entry files that define behavior and local commands:
   - `Makefile`
   - `langgraph.json`
   - `pyproject.toml`
   - `main.py`
   - `src/agents/general_agent.py`
   - `src/models/patched_deepseek.py`
   - `src/tools/bash_tool.py`
4. Inspect project-local skills under `.agents/skills/` if they exist.
5. Check recent commits with `git log --oneline -n 10`.

## Commit History Rules

- If commit history exists, summarize only the recent commits that materially affect repository guidance.
- If the repository has no commits yet, explicitly say that there is no commit history yet.
- Do not invent commit history.
- If there is no commit history, you may describe observed current state, but label it as current state rather than commit-derived history.

## Required Sections In AGENTS.md

Keep these sections accurate unless the repository outgrows them:

- `Scope`
- `Project Structure`
- `Module Responsibilities`
- `Code Style`
- `Prompting Style`
- `Local Commands`
- `Development Constraints`
- `Current Known Constraints`
- `Recent Changes`
- `AGENTS Maintenance`

## Writing Rules

- Use English.
- Prefer updating the existing `AGENTS.md` in place rather than rewriting from scratch.
- Keep the document specific to this repository. Do not copy generic policy text.
- Do not document directories, commands, or files that do not exist.
- Do not claim a command is supported unless it is present in the repository or has been verified directly.
- Keep guidance actionable. Favor short bullets over long prose.
- Preserve the spirit of minimal change, high cohesion, and low coupling.

## Repository Conventions To Preserve

- Prefer minimal changes first.
- Keep clear separation across `agents`, `models`, and `tools`.
- Tool implementations that execute shell commands must remain asynchronous.
- For LangChain tool registration in this repository, use `@tool("name", parse_docstring=True)`.
- Prefer environment-based configuration for secrets and external configuration.

## Update Procedure

Use this sequence:

1. Gather current repository evidence.
2. Compare the existing `AGENTS.md` against current reality.
3. Add or update only the sections that changed.
4. Refresh `Recent Changes` from recent commits when available.
5. If no commits exist, state that clearly and note that the section reflects current repository state.
6. Verify links, paths, and commands before finishing.

## Output Expectations

When you finish:

- the root `AGENTS.md` reflects the current repository
- the document includes project-local skills when relevant
- `Recent Changes` is truthful about commit history availability
- no section contains fabricated structure or stale commands
