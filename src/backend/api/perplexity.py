import requests


class PerplexityAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai/v1"

    def search(self, query):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            response = requests.get(
                f"{self.base_url}/search", headers=headers, params={"query": query}
            )
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during Perplexity API request: {e}")
            return None  # Return None or handle error as needed

    def get_related_topics(self, topic):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            response = requests.get(
                f"{self.base_url}/related", headers=headers, params={"topic": topic}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during Perplexity API related topics request: {e}")
            return None
