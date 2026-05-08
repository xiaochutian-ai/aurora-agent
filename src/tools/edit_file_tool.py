import asyncio
from pathlib import Path

from langchain_core.tools import tool


def _edit_file(file_path: str, old_text: str, new_text: str) -> str:
    path = Path(file_path)
    content = path.read_text(encoding="utf-8")

    if old_text not in content:
        return f"Failed to edit file '{file_path}': target text not found"

    path.write_text(content.replace(old_text, new_text), encoding="utf-8")
    return f"Successfully edited file '{file_path}'"


@tool("edit_file", parse_docstring=True)
async def edit_file_tool(
    description: str, file_path: str, old_text: str, new_text: str
) -> str:
    """Edit a local file by replacing a target text fragment.

    Args:
        description: A brief natural-language description of why the file is being edited.
        file_path: The path to the file that should be edited.
        old_text: The existing text fragment that should be replaced.
        new_text: The replacement text fragment.

    Returns:
        A success message on success, or a readable error message on failure.
    """
    _ = description

    try:
        return await asyncio.to_thread(_edit_file, file_path, old_text, new_text)
    except Exception as exc:
        return f"Failed to edit file '{file_path}': {exc}"
