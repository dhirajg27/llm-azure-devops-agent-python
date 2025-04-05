import os
from dotenv import load_dotenv
import logging

load_dotenv()  # Load variables from .env file

# Add these lines to check the variables
print(f"AZURE_DEVOPS_ORG: {os.getenv('AZURE_DEVOPS_ORG')}")
print(f"AZURE_DEVOPS_PROJECT: {os.getenv('AZURE_DEVOPS_PROJECT')}")
print(f"AZURE_DEVOPS_PAT: {os.getenv('AZURE_DEVOPS_PAT')}")
print(f"OPENROUTER_API_KEY: {os.getenv('OPENROUTER_API_KEY')}")
print(f"TEAMS_WEBHOOK: {os.getenv('TEAMS_WEBHOOK')}")
print(f"LOG_LEVEL: {os.getenv('LOG_LEVEL')}")


from config import Config
from azure_devops_client import AzureDevOpsClient
from openrouter_client import OpenRouterClient
from teams_client import TeamsClient
from scrum_board_agent import ScrumBoardAgent

def main():
    """
    Main entry point for the application. Initializes configuration, logging,
    clients, and the ScrumBoardAgent, then runs the agent.
    """
    Config.initialize_logging()
    azure_client = AzureDevOpsClient()
    openrouter_client = OpenRouterClient()
    teams_client = TeamsClient()
    agent = ScrumBoardAgent(azure_client, openrouter_client, teams_client)

    # Example usage:
    # agent.run()
    agent.run("Get top 2 delayed tasks?")


if __name__ == "__main__":
    main()