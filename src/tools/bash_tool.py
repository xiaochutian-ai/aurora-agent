import asyncio

from langchain_core.tools import tool


@tool("bash", parse_docstring=True)
async def bash_tool(description: str, command: str) -> str:
    """Run a bash command asynchronously and return its output.

    Args:
        description: A brief natural-language description of what the command does.
        command: The bash command to execute.

    Returns:
        The command's standard output when it succeeds, or the standard error when it fails.
    """
    _ = description

    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        return stdout.decode("utf-8", errors="replace").strip()

    error_output = stderr.decode("utf-8", errors="replace").strip()
    if error_output:
        return error_output
    return f"Command failed with exit code {process.returncode}"
