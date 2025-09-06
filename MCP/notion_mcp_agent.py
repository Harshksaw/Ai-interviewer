# https://developers.notion.com/docs/get-started-with-mcp
# Example Notion MCP agent using Autogen's McpWorkbench
import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from dotenv import load_dotenv
load_dotenv()  # loads .env into os.environ
NOTION_API_KEY=os.getenv("NOTION_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not NOTION_API_KEY:
    raise RuntimeError("NOTION_API_KEY is not set. Export NOTION_API_KEY or add it to .env.")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set. Export OPENAI_API_KEY or add it to .env.")


SYSTEM_MESSAGE = (
    "You are a helpful assistant that can search and summarize content from the user's Notion workspace "
    "and also list what is asked. Try to assume the tool and call the same and get the answer. Say TERMINATE when you are done with the task."
)


async def config():
    params = StdioServerParams(
        command="npx",
        args=["-y", "mcp-remote", "https://mcp.notion.com/mcp"],
        env={"NOTION_API_KEY": NOTION_API_KEY},
        read_timeout_seconds=20,
    )

    model = OpenAIChatCompletionClient(model="gpt-4o", api_key=OPENAI_API_KEY)

    # Create local tool wrappers from the remote MCP server
    mcp_tools = await mcp_server_tools(server_params=params)

    agent = AssistantAgent(
        name="Notion Agent",
        system_message=SYSTEM_MESSAGE,
        model_client=model,
        tools=mcp_tools,
        reflect_on_tool_use=True,
    )

    team = RoundRobinGroupChat(
        participants=[agent],
        max_turns=5,
        termination_condition=TextMentionTermination("TERMINATE"),
    )

    return team


async def orchestrate(team, task):
    async for msg in team.run_stream(task=task):
        yield msg


async def main():
    team = await config()
    task = "List all the databases in my Notion workspace and give a summary of each"
    async for message in orchestrate(team, task):
        print("-" * 100)
        print(message)
        print("-" * 100)


if __name__ == "__main__":
    asyncio.run(main())