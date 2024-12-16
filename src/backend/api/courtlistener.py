import os
import requests


class CourtListenerAPI:
    def __init__(self):
        self.api_url = os.environ["COURT_LISTENER_API_URL"]

    def search_case(self, search_statement):
        try:
            response = requests.get(f"{self.api_url}/search/", params={"q": search_statement})
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during CourtListener API request: {e}")
            return None  # Return None or handle error as needed

    def get_case_details(self, case_id):
        try:
            response = requests.get(f"{self.api_url}/cases/{case_id}/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during CourtListener API case details request: {e}")
            return None
