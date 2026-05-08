import asyncio
from pathlib import Path

from langchain_core.tools import tool


def _read_file(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8")


@tool("read_file", parse_docstring=True)
async def read_file_tool(description: str, file_path: str) -> str:
    """Read a local file and return its contents.

    Args:
        description: A brief natural-language description of why the file is being read.
        file_path: The path to the file that should be read.

    Returns:
        The file contents on success, or a readable error message on failure.
    """
    _ = description

    try:
        return await asyncio.to_thread(_read_file, file_path)
    except Exception as exc:
        return f"Failed to read file '{file_path}': {exc}"
