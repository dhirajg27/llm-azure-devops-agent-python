import os
import logging

class Config:
    """
    Manages configuration settings for the application.
    """
    AZURE_DEVOPS_ORG = os.getenv("AZURE_DEVOPS_ORG")
    AZURE_DEVOPS_PROJECT = os.getenv("AZURE_DEVOPS_PROJECT")
    AZURE_DEVOPS_PAT = os.getenv("AZURE_DEVOPS_PAT")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
    TEAMS_WEBHOOK = os.getenv("TEAMS_WEBHOOK")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

    @staticmethod
    def initialize_logging():
        """
        Initializes logging configuration.
        """
        log_level = getattr(logging, Config.LOG_LEVEL, logging.INFO)
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.StreamHandler()],
        )
        