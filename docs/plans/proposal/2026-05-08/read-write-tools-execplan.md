# ExecPlan: Add `read_file`, `write_file`, and `edit_file` tools under `src/tools`

## Goal And Big Picture

Add three new LangChain tools under `src/tools` that mirror the repository style used by `src/tools/bash_tool.py`, including file naming:

- `read_file`: read a local file and return its content or a readable error message
- `write_file`: write content to a local file and return a success message or a readable error message
- `edit_file`: edit an existing local file by replacing a target text fragment and return a success message or a readable error message

After this work, the repository will have a minimal file I/O tool set alongside the existing Bash tool, with matching decorator style, Python docstrings, readable return contracts, and consistent `_tool.py` filenames.

## Progress Tracking

- [x] [2026-05-08 15:50:43 +0800] Investigated the current `src/tools` layout and existing `bash_tool.py`
- [x] [2026-05-08 15:50:43 +0800] Captured Git baseline and local timestamp
- [x] [2026-05-08 16:02:00 +0800] Create `src/tools/read_file_tool.py`
- [x] [2026-05-08 16:02:00 +0800] Create `src/tools/write_file_tool.py`
- [x] [2026-05-08 16:02:00 +0800] Create `src/tools/edit_file_tool.py`
- [x] [2026-05-08 16:02:00 +0800] Verify imports and diagnostics
- [x] [2026-05-08 16:02:00 +0800] Update this plan with completion notes

## Unexpected Findings

- [2026-05-08 15:50:43 +0800] A previous assumption that the repository had no commits is no longer accurate. Current Git history includes the initial commit `78531f1 feat: init`.

## Decision Log

- [2026-05-08 15:50:43 +0800] Decision: create one tool per file under `src/tools/`, and keep the filename suffix `_tool.py`.
  Reason: this matches the current repository layout, keeps tool responsibilities narrow, and follows the existing naming pattern established by `bash_tool.py`.
- [2026-05-08 15:50:43 +0800] Decision: keep return values simple strings instead of structured payloads.
  Reason: `bash_tool.py` already returns plain strings, and matching that contract reduces integration risk with the existing agent setup.
- [2026-05-08 15:50:43 +0800] Decision: avoid introducing path policy or sandbox logic in this change.
  Reason: the user asked for tools that reference `bash_tool.py`; that file is intentionally minimal, so this change should stay scoped to basic file read/write behavior.
- [2026-05-08 15:50:43 +0800] Decision: define `edit_file` as a targeted text replacement tool using `old_text` and `new_text`.
  Reason: this is the smallest useful editing contract, keeps the tool deterministic, and avoids introducing patch parsing or multi-operation editing complexity in the first version.

## Results And Retrospective

Implemented all three planned tool modules in the isolated worktree:

- `src/tools/read_file_tool.py`
- `src/tools/write_file_tool.py`
- `src/tools/edit_file_tool.py`

All three tools follow the repository style established by `bash_tool.py`:

- `@tool("name", parse_docstring=True)`
- async tool entrypoint
- concise Python docstring
- readable string return contract

Validation completed successfully:

- import validation command returned `import ok`
- diagnostics for all three new files are empty

## Context And Direction

The repository currently contains a small Python agent stack:

- `src/agents/general_agent.py` assembles the model, tools, and system prompt
- `src/models/patched_deepseek.py` contains a focused model patch
- `src/tools/bash_tool.py` is the only existing tool implementation

The tool pattern in this repository is currently:

- `@tool("name", parse_docstring=True)`
- async tool function
- concise docstring with `Args` and `Returns`
- readable string result on success or failure

The request is specifically to add `read_file`, `write_file`, and `edit_file` under `src/tools`, using `bash_tool.py` as the style reference.

## Work Plan

First, add `src/tools/read_file_tool.py` with an async LangChain tool that accepts a natural-language description and a file path, then reads the file content in a non-blocking way suitable for the current async-oriented tool style. Error handling should catch common file failures and return readable messages instead of raising.

Second, add `src/tools/write_file_tool.py` with an async LangChain tool that accepts a natural-language description, a file path, and file content, then writes the content to disk and reports success or failure as a string. The implementation should avoid unnecessary abstraction and keep behavior explicit.

Third, add `src/tools/edit_file_tool.py` with an async LangChain tool that accepts a natural-language description, a file path, an `old_text` fragment, and a `new_text` fragment. The tool should read the file, replace the target fragment, write the updated content back, and return readable success or failure output. If the target fragment does not exist, the tool should return a clear error message instead of silently succeeding.

Fourth, run import validation and diagnostics to ensure all three modules load cleanly and align with the existing repository conventions.

## Concrete Steps

1. Create `src/tools/read_file_tool.py`
   - Working directory: repository root
   - Implement `@tool("read_file", parse_docstring=True)`
   - Use async function signature
   - Read file content and return text on success
   - Return readable error text on failure

2. Create `src/tools/write_file_tool.py`
   - Working directory: repository root
   - Implement `@tool("write_file", parse_docstring=True)`
   - Use async function signature
   - Write provided content to the given path
   - Return readable success or failure text

3. Create `src/tools/edit_file_tool.py`
   - Working directory: repository root
   - Implement `@tool("edit_file", parse_docstring=True)`
   - Use async function signature
   - Read the target file, replace `old_text` with `new_text`, and persist the updated content
   - Return a readable error if the file does not exist or if `old_text` is not found

4. Validate imports
   - Command:
     ```bash
     python3 -c "from src.tools.read_file_tool import read_file_tool; from src.tools.write_file_tool import write_file_tool; from src.tools.edit_file_tool import edit_file_tool; print('import ok')"
     ```
   - Expected output:
     - `import ok`

5. Check diagnostics on touched files
   - Confirm no editor diagnostics remain in the new tool files

## Validation And Acceptance

The work is accepted only if all of the following are true:

- `src/tools/read_file_tool.py` exists and exports a tool function named `read_file_tool`
- `src/tools/write_file_tool.py` exists and exports a tool function named `write_file_tool`
- `src/tools/edit_file_tool.py` exists and exports a tool function named `edit_file_tool`
- all three tools use `@tool("name", parse_docstring=True)`
- all three tools include Python docstrings with argument and return descriptions
- import validation command prints `import ok`
- diagnostics for all new files are empty

## Documentation Updates

Assessed: no immediate `AGENTS.md` update is required for this change unless these tools are later registered in `src/agents/general_agent.py` or become part of the stable project surface described there.

## Idempotency And Recovery

The implementation is low risk and repeatable:

- re-running file creation should only overwrite the target files with the intended contents
- if import validation fails, inspect decorator usage, symbol names, and syntax before retrying
- if diagnostics fail, fix the touched files before proceeding
- `edit_file_tool` intentionally returns a readable error if `old_text` is not found rather than silently reporting success

## Artifacts And Notes

- Git branch: `main`
- Git commit baseline: `78531f1d3b91c727e8484065b8a8acacac570b1f`
- Latest visible commit during planning: `78531f1 feat: init`
- Planning timestamp: `2026-05-08 15:50:43 +0800 CST`
- Implementation workspace: `.worktrees/file-tools`
- Validation result: `python3 -c "from src.tools.read_file_tool import read_file_tool; from src.tools.write_file_tool import write_file_tool; from src.tools.edit_file_tool import edit_file_tool; print('import ok')"` -> `import ok`

## Interfaces And Dependencies

- Dependency: `langchain_core.tools.tool`
- Style reference: `src/tools/bash_tool.py`
- Planned interfaces:
  - `async def read_file_tool(description: str, file_path: str) -> str`
  - `async def write_file_tool(description: str, file_path: str, content: str) -> str`
  - `async def edit_file_tool(description: str, file_path: str, old_text: str, new_text: str) -> str`
