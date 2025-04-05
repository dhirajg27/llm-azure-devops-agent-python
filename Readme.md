# Azure DevOps Scrum Board Agent

## Description

This agent automates Scrum board tasks in Azure DevOps and provides integration with Microsoft Teams. It helps teams track delayed tasks, query task status in natural language, and receive proactive notifications.

## Features

* **Delayed Task Tracking:** The agent identifies tasks in Azure DevOps that are past their target date and not yet completed.
* **Natural Language Queries:** Users can ask questions about their Scrum board in plain English, such as "What are the top 3 delayed tasks?".  The agent uses OpenRouter.ai to understand these queries.
* **Microsoft Teams Notifications:**
  * The agent sends notifications to a Microsoft Teams channel when tasks become delayed.

## Prerequisites

* **Azure DevOps:**
  * An Azure DevOps organization and project.
  * A Personal Access Token (PAT) with permissions to access work items.
* **OpenRouter.ai:**
  * An OpenRouter.ai account and API key.
* **Microsoft Teams:**
  * A Microsoft Teams team and channel.
  * A webhook URL for the Teams channel.
* **Python 3.6 or later**
* **Required Python Packages:**
  * requests
  * pymsteams
  * logging

## Setup

1. **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd azure-devops-scrum-agent
    ```

2. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Configure environment variables:**
    Create a `.env` file in the project root directory and add the following environment variables:

    ```
    AZURE_DEVOPS_ORG=<your_azure_devops_organization>
    AZURE_DEVOPS_PROJECT=<your_azure_devops_project>
    AZURE_DEVOPS_PAT=<your_azure_devops_personal_access_token>
    OPENROUTER_API_KEY=<your_openrouter_api_key>
    TEAMS_WEBHOOK=<your_microsoft_teams_webhook_url>
    LOG_LEVEL=INFO # Optional: Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    ```

    Replace the placeholder values with your actual values.
4. **Run the application:**

    ```bash
    python main.py
    ```

## Usage

The agent can be used in two ways:

1. **Delayed Task Notifications:** The agent will automatically check for delayed tasks in Azure DevOps and send a notification to the configured Microsoft Teams channel.
2. **Natural Language Queries:** You can send a natural language query to the agent, and it will respond with relevant information from Azure DevOps.  For example:

    ```bash
    python main.py "What are the top 5 delayed tasks?"
    ```

## Code Structure

The application is organized into the following modules:

* `config.py`:  Manages configuration settings.
* `azure_devops_client.py`:  Interacts with the Azure DevOps API.
* `openrouter_client.py`:  Interacts with the OpenRouter.ai API.
* `teams_client.py`:  Sends notifications to Microsoft Teams.
* `scrum_board_agent.py`:  Orchestrates the agent's operations.
* `main.py`:  The main entry point for the application.

## Contributing

Contributions are welcome!  Please submit a pull request or create an issue to propose changes.
