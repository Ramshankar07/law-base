from .api.perplexity import PerplexityAPI
from .api.courtlistener import CourtListenerAPI
from typing import Dict, List


class DataCollectionPipeline:
    def __init__(self, perplexity_api_key):
        self.perplexity_api = PerplexityAPI(perplexity_api_key)
        self.court_listener_api = CourtListenerAPI()

    def collect_data(self, query):
        perplexity_results = self.perplexity_api.search(query)
        court_listener_results = self.court_listener_api.search_case(query)
        return {"perplexity": perplexity_results, "court_listener": court_listener_results}

    def validate_results(self, results: Dict) -> bool:
        """Validate API results"""
        if not results.get("perplexity") or not results.get("court_listener"):
            return False
        return True

    def process_results(self, results: Dict) -> Dict:
        """Process and combine API results"""
        if not self.validate_results(results):
            return {"error": "Invalid or incomplete results"}

        processed_data = {
            "legal_precedents": self._extract_precedents(results),
            "relevant_cases": self._extract_cases(results),
            "analysis": self._combine_analysis(results),
        }
        return processed_data

    def _extract_precedents(self, results: Dict) -> List[Dict]:
        """Extract precedents from API results"""
        precedents = []
        if results.get("court_listener"):
            for case in results["court_listener"].get("cases", []):
                precedents.append(
                    {
                        "case_name": case.get("case_name"),
                        "citation": case.get("citation"),
                        "date": case.get("date_filed"),
                    }
                )
        return precedents
