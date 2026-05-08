import asyncio
from pathlib import Path

from langchain_core.tools import tool


def _write_file(file_path: str, content: str) -> None:
    Path(file_path).write_text(content, encoding="utf-8")


@tool("write_file", parse_docstring=True)
async def write_file_tool(description: str, file_path: str, content: str) -> str:
    """Write content to a local file.

    Args:
        description: A brief natural-language description of why the file is being written.
        file_path: The path to the file that should be written.
        content: The full content to write into the file.

    Returns:
        A success message on success, or a readable error message on failure.
    """
    _ = description

    try:
        await asyncio.to_thread(_write_file, file_path, content)
        return f"Successfully wrote file '{file_path}'"
    except Exception as exc:
        return f"Failed to write file '{file_path}': {exc}"
