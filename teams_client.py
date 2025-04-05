import pymsteams
import logging
from config import Config

class TeamsClient:
    """
    Encapsulates interactions with the Microsoft Teams API.
    """
    def __init__(self):
        """
        Initializes the TeamsClient with the webhook URL.
        """
        self.webhook_url = Config.TEAMS_WEBHOOK

    def send_notification(self, message):
        """
        Sends a notification to a Microsoft Teams channel using a webhook.

        Args:
            message (str): The message to send.
        """
        teams_message = pymsteams.connectorcard(self.webhook_url)
        teams_message.text(message)
        try:
            teams_message.send()
        except pymsteams.connectorcard.PyMsTeamsException as e:
            logging.error(f"Error sending notification to Microsoft Teams: {e}")
            # Consider logging the error or taking other corrective action.