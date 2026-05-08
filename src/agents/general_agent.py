from langchain.agents import create_agent
from src.models.patched_deepseek import PatchedChatDeepSeek
from src.tools.bash_tool import bash_tool
from src.tools.edit_file_tool import edit_file_tool
from src.tools.read_file_tool import read_file_tool
from src.tools.write_file_tool import write_file_tool
from src.tools.write_todos_tool import write_todos_tool

def create_general_agent():
    agent = create_agent(
        model = PatchedChatDeepSeek(model_name="deepseek-v4-flash", api_key="sk-2497ca6339ee4ae586e1ee76c6b92535"),
        tools=[bash_tool, read_file_tool, write_file_tool, edit_file_tool, write_todos_tool],
        system_prompt="""
<identity>
You are Aurora, a coding agent.
</identity>

<skill-system>
You have access to skills that provide optimized workflows for specific tasks. Each skill contains best practices, frameworks, and references to additional resources.

**Progressive Loading Pattern:**
1. When a user query matches a skill's use case, immediately call \`read_file\` on the skill's main file using the path attribute provided in the skill tag below
2. If an explicit requested skill is provided in the system context, load that skill first even if the user message is short
3. Read and understand the skill's workflow and instructions
4. The skill file contains references to external resources under the same folder
5. Load referenced resources only when needed during execution
6. Follow the skill's instructions precisely
</skill-system>

<available-skills>
<skill name="frontend-design" path="~/.agents/skills/*/SKILL.md">
Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic AI aesthetics.
</skill>
</available-skills>

<workspace>
<root path="/Users/bytedance/aurora-agent" />
</workspace>
""",
    )
    return agent
