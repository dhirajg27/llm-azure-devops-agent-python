import requests
import json
import logging
import base64  # Import the base64 module
from config import Config

class AzureDevOpsClient:
    """
    Encapsulates interactions with the Azure DevOps API.
    """
    def __init__(self):
        """
        Initializes the AzureDevOpsClient with configuration and headers.
        """
        self.base_url = f"https://dev.azure.com/{Config.AZURE_DEVOPS_ORG}/{Config.AZURE_DEVOPS_PROJECT}/_apis/wit/wiql?api-version=7.1"
        # Corrected Authorization header construction:
        pat_bytes = (':' + Config.AZURE_DEVOPS_PAT).encode('utf-8')
        pat_b64 = base64.b64encode(pat_bytes).decode('utf-8')
        self.headers = {
            "Authorization": f"Basic {pat_b64}",
            "Content-Type": "application/json",
        }

    def get_delayed_tasks(self):
        """
        Retrieves tasks from Azure DevOps that are past their target date and not yet done.

        Returns:
            list: A list of dictionaries, where each dictionary represents a delayed task
                  and contains its ID, title, state, and target date. Returns an empty
                  list if no delayed tasks are found.
        """
        query = {
            "query": """
            SELECT [System.Id], [System.Title], [System.State], [Microsoft.VSTS.Scheduling.TargetDate]
            FROM WorkItems
            WHERE [System.WorkItemType] = 'Task'
            AND [System.State] <> 'Done'
            AND [Microsoft.VSTS.Scheduling.TargetDate] = @today - 10
            """
        }

        try:
            response = requests.post(self.base_url, headers=self.headers, json=query)
            response.raise_for_status()
            results = response.json()["workItems"]
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching delayed tasks from Azure DevOps: {e}")
            return []
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON response from Azure DevOps: {e}")
            return []

        delayed_tasks = []
        if results:
            for item in results:
                try:
                    work_item_url = item["url"]
                    work_item_response = requests.get(work_item_url, headers=self.headers)
                    work_item_response.raise_for_status()
                    work_item_details = work_item_response.json()["fields"]
                    delayed_tasks.append(
                        {
                            "id": item["id"],
                            "title": work_item_details["System.Title"],
                            "state": work_item_details["System.State"],
                            "target_date": work_item_details.get("Microsoft.VSTS.Scheduling.TargetDate"),
                        }
                    )
                except requests.exceptions.RequestException as e:
                    logging.error(f"Error fetching details for work item {item['id']}: {e}")
                    continue
                except json.JSONDecodeError as e:
                    logging.error(f"Error decoding work item details for  {item['id']}: {e}")
                    continue
        return delayed_tasks
