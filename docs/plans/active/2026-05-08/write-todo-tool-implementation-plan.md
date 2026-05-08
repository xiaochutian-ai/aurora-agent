# Write Todos Tool Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `write_todos` LangChain tool that writes validated JSON todo content to disk and register it in `general_agent.py`.

**Architecture:** Follow the existing `src/tools/*_tool.py` pattern: a small helper function for synchronous disk work plus an async tool wrapper using `asyncio.to_thread`. Keep the interface minimal by accepting a JSON string, parsing and pretty-printing it, then wiring the tool into the existing agent tool list.

**Tech Stack:** Python 3.13, `langchain_core.tools.tool`, `asyncio`, `json`, `pathlib`

---

### Task 1: Add `write_todos_tool`

**Files:**
- Create: `src/tools/write_todos_tool.py`

- [x] **Step 1: Run a failing import check**

Run:

```bash
python3 -c "from src.tools.write_todos_tool import write_todos_tool"
```

Expected: FAIL with `ModuleNotFoundError`

- [x] **Step 2: Write the minimal implementation**

Create `src/tools/write_todos_tool.py` with:

```python
import asyncio
import json
from pathlib import Path

from langchain_core.tools import tool


def _write_todos(file_path: str, todos_json: str) -> None:
    todos = json.loads(todos_json)
    Path(file_path).write_text(
        json.dumps(todos, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


@tool("write_todos", parse_docstring=True)
async def write_todos_tool(description: str, file_path: str, todos_json: str) -> str:
    """Write JSON todo data to a local file.

    Args:
        description: A brief natural-language description of why the todo file is being written.
        file_path: The path to the todo file that should be written.
        todos_json: A JSON string describing the todo data to persist.

    Returns:
        A success message on success, or a readable error message on failure.
    """
    _ = description

    try:
        await asyncio.to_thread(_write_todos, file_path, todos_json)
        return f"Successfully wrote todo file '{file_path}'"
    except Exception as exc:
        return f"Failed to write todo file '{file_path}': {exc}"
```

- [x] **Step 3: Verify the new tool imports**

Run:

```bash
python3 -c "from src.tools.write_todos_tool import write_todos_tool; print('import ok')"
```

Expected: `import ok`

### Task 2: Register `write_todos_tool` in `general_agent.py`

**Files:**
- Modify: `src/agents/general_agent.py`

- [x] **Step 1: Update imports and tool registration**

Change `src/agents/general_agent.py` to:

```python
from langchain.agents import create_agent
from src.models.patched_deepseek import PatchedChatDeepSeek
from src.tools.bash_tool import bash_tool
from src.tools.edit_file_tool import edit_file_tool
from src.tools.read_file_tool import read_file_tool
from src.tools.write_file_tool import write_file_tool
from src.tools.write_todos_tool import write_todos_tool


def create_general_agent():
    agent = create_agent(
        model=PatchedChatDeepSeek(
            model_name="deepseek-v4-flash",
            api_key="sk-2497ca6339ee4ae586e1ee76c6b92535",
        ),
        tools=[
            bash_tool,
            read_file_tool,
            write_file_tool,
            edit_file_tool,
            write_todos_tool,
        ],
        system_prompt="""
<identity>
You are Aurora, a coding agent.
</identity>

<workspace>
<root path="/Users/bytedance/aurora-agent" />
</workspace>
""",
    )
    return agent
```

- [x] **Step 2: Verify agent import**

Run:

```bash
python3 -c "from src.agents.general_agent import create_general_agent; print('import ok')"
```

Expected: `import ok`

### Task 3: Diagnostics Check

**Files:**
- Check: `src/tools/write_todos_tool.py`
- Check: `src/agents/general_agent.py`

- [x] **Step 1: Confirm diagnostics are empty**

Check editor diagnostics for:

- `src/tools/write_todos_tool.py`
- `src/agents/general_agent.py`

Expected: no diagnostics

- [x] **Step 2: Confirm worktree diff is limited**

Run:

```bash
git status --short
```

Expected: `src/tools/write_todos_tool.py` and `src/agents/general_agent.py` are changed for this task. This worktree also already contains untracked `docs/` files from earlier plan work.
