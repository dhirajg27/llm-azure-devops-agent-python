# -*- coding: utf-8 -*-
 
import requests
import json
import logging
import re
from config import Config

class OpenRouterClient:
    """
    Encapsulates interactions with the OpenRouter.ai API.
    """
    def __init__(self):
        """
        Initializes the OpenRouterClient with the API key and URL.
        """
        self.api_key = Config.OPENROUTER_API_KEY
        self.api_url = Config.OPENROUTER_API_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def get_response(self, prompt, model: str = "deepseek/deepseek-r1:free"):
        """
        Sends a prompt to the OpenRouter.ai API and returns the response.

        Args:
            prompt (str): The prompt to send to the language model.
            model (str, optional): The language model to use.
                Defaults to "deepseek/deepseek-r1:free".

        Returns:
            dict: The JSON response from the OpenRouter.ai API. Returns an empty
                  dictionary on error.
        """
        try:
            data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            }

            response = requests.post(self.api_url, headers=self.headers, json=data)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            response_data = response.json()

            # Extract the content from the response
            content = response_data["choices"][0]["message"]["content"]

            # Use a regular expression to find the JSON within the content
            match = re.search(r"```json\n(.*?)\n```", content, re.DOTALL)
            if match:
                json_string = match.group(1)
                # Parse the extracted JSON
                inner_json = json.loads(json_string)
                return inner_json
            else:
                logging.error("No JSON found in OpenRouter response content.")
                return None

        except requests.exceptions.RequestException as e:
            logging.error(f"Error connecting to OpenRouter.ai: {e}")
            return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Error communicating with OpenRouter.ai: {e}")
            return {}

    def get_intent_and_entities(self, query):
        """
        Extracts the intent and entities from a user query using OpenRouter.ai.

        Args:
            query (str): The user's query in natural language.

        Returns:
            tuple: A tuple containing the intent (str) and a dictionary of entities.
                   Returns "unknown" and {} on error.
        """
        prompt = f"""
        Extract the intent and entities from the following query: "{query}"

        Format your response as a JSON object with "intent" and "entities" keys.
        If no entities are found, return an empty object for the entities.
        """
        response = self.get_response(prompt)
        if not response:
            return "unknown", {}

        try:
            result = response["choices"][0]["message"]["content"]
            result_json = json.loads(result)
            return result_json.get("intent", "unknown"), result_json.get("entities", {})
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            logging.error(f"Error processing OpenRouter.ai response: {e}")
            return "unknown", {}