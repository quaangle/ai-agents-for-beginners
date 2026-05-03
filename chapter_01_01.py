import logging
logging.getLogger("agent_framework.azure").setLevel(logging.ERROR)

import os
import asyncio

from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential


# Tool definition
@tool(approval_mode="never_require")
def get_destinations() -> list[str]:
    """Get a list of popular vacation destinations."""
    return [
        "Barcelona", "Paris", "Berlin", "Tokyo", "Sydney",
        "New York City", "Cairo", "Cape Town", "Rio de Janeiro", "Bali",
    ]


async def main():
    # Read config from environment
    project_endpoint = (
        os.getenv("AZURE_AI_PROJECT_ENDPOINT")
        or os.getenv("FOUNDRY_PROJECT_ENDPOINT")
        or ""
    )
    model = (
        os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")
        or os.getenv("FOUNDRY_MODEL")
        or ""
    )

    # Create client (connects to Azure AI Foundry)
    client = FoundryChatClient(
        project_endpoint=project_endpoint,
        model=model,
        credential=AzureCliCredential(),
    )

    # Create agent directly (no provider)
    agent = Agent(
        client=client,
        tools=[get_destinations],
        name="TravelAgent",
        instructions=(
            "You are a helpful travel agent. Help users find their perfect "
            "vacation destination based on their preferences. "
            "Use the get_destinations tool when needed."
        ),
    )

    # Run agent
    response = await agent.run(
        "I'm looking for a warm beach destination. What do you recommend?"
    )
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
    