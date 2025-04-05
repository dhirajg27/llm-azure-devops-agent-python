from azure_devops_client import AzureDevOpsClient
from openrouter_client import OpenRouterClient
from teams_client import TeamsClient
import logging

class ScrumBoardAgent:
    """
    Orchestrates the operations of the Scrum board agent.
    """
    def __init__(self, azure_client, openrouter_client, teams_client):
        """
        Initializes the ScrumBoardAgent with clients for Azure DevOps,
        OpenRouter.ai, and Microsoft Teams.

        Args:
            azure_client (AzureDevOpsClient): An instance of AzureDevOpsClient.
            openrouter_client (OpenRouterClient): An instance of OpenRouterClient.
            teams_client (TeamsClient): An instance of TeamsClient.
        """
        self.azure_client = azure_client
        self.openrouter_client = openrouter_client
        self.teams_client = teams_client

    def handle_delayed_tasks(self):
        """
        Retrieves delayed tasks from Azure DevOps and sends a notification to Teams.
        """
        delayed_tasks = self.azure_client.get_delayed_tasks()
        if delayed_tasks:
            message = "🚨 Delayed Tasks Detected:\n"
            for task in delayed_tasks:
                message += f"- {task['title']} (ID: {task['id']})\n"
            self.teams_client.send_notification(message)

    def handle_user_query(self, user_query):
        """
        Processes a user query using OpenRouter.ai and sends a response to Teams.

        Args:
            user_query (str): The user's query.
        """
        intent, entities = self.openrouter_client.get_intent_and_entities(user_query)

        if intent == "GetDelayedTasks":
            num_tasks = entities.get("number", None)
            if num_tasks:
                try:
                    num_tasks = int(num_tasks)
                    response_message = f"Here are the top {num_tasks} delayed tasks:\n"
                    for i in range(min(num_tasks, len(self.azure_client.get_delayed_tasks()))):
                        response_message += f"- {self.azure_client.get_delayed_tasks()[i]['title']} (ID: {self.azure_client.get_delayed_tasks()[i]['id']})\n"
                    self.teams_client.send_notification(response_message)
                except ValueError:
                    self.teams_client.send_notification(
                        f"Invalid number provided: {num_tasks}. Please provide a valid number."
                    )
            else:
                response_message = "Here are the delayed tasks:\n"
                for task in self.azure_client.get_delayed_tasks():
                    response_message += f"- {task['title']} (ID: {task['id']})\n"
                self.teams_client.send_notification(response_message)
        elif intent == "unknown":
            self.teams_client.send_notification(f"Sorry, I could not understand the query: {user_query}")
        else:
            self.teams_client.send_notification(f"Intent not recognized: {intent}")

    def run(self, user_query=None):
        """
        Runs the agent: checks for delayed tasks and handles user queries.

        Args:
            user_query (str, optional): The user's query. Defaults to None.
        """
        self.handle_delayed_tasks()
        if user_query:
            self.handle_user_query(user_query)