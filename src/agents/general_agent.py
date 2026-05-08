from langchain.agents import create_agent
from src.models.patched_deepseek import PatchedChatDeepSeek
from src.tools.bash_tool import bash_tool
from src.tools.edit_file_tool import edit_file_tool
from src.tools.read_file_tool import read_file_tool
from src.tools.write_file_tool import write_file_tool

def create_general_agent():
    agent = create_agent(
        model = PatchedChatDeepSeek(model_name="deepseek-v4-flash", api_key="sk-2497ca6339ee4ae586e1ee76c6b92535"),
        tools=[bash_tool, read_file_tool, write_file_tool, edit_file_tool],
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
