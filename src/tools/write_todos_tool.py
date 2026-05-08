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
