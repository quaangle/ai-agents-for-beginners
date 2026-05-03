import logging
logging.getLogger("agent_framework.azure").setLevel(logging.ERROR)

import os
import asyncio
from typing import Annotated

from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential


async def main():
    project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT") or os.getenv("FOUNDRY_PROJECT_ENDPOINT") or ""
    model = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME") or os.getenv("FOUNDRY_MODEL") or ""

    client = FoundryChatClient(
        project_endpoint=project_endpoint,
        model=model,
        credential=AzureCliCredential(),
    )

    agent = Agent(client=client)

    @tool(approval_mode="never_require")
    def get_destinations() -> list[str]:
        return [
            "Barcelona", "Paris", "Berlin", "Tokyo", "Sydney",
            "New York City", "Cairo", "Cape Town", "Rio de Janeiro", "Bali",
        ]

    agent = await provider.create_agent(
        tools=[get_destinations],
        name="TravelAgent",
        instructions=(
            "You are a helpful travel agent. Help users find their perfect vacation "
            "destination based on their preferences."
        ),
    )

    response = await agent.run(
        "I'm looking for a warm beach destination. What do you recommend?"
    )
    print(response)


if __name__ == "__main__":
    asyncio.run(main())