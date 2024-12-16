# src/backend/analysis/case_analysis.py
from typing import Dict, List
import re
from collections import Counter
from datetime import datetime
from utils.logging_config import LegalLogger
from utils.monitoring import PerformanceMonitor


class CaseAnalysis:
    def __init__(self):
        self.logger = LegalLogger(__name__)
        self.monitor = PerformanceMonitor()
        self.precedent_weight = {"Supreme Court": 1.0, "Circuit Court": 0.8, "District Court": 0.6}

    def analyze(self, case_data: Dict) -> Dict:
        start_time = self.monitor.start_operation("case_analysis")
        try:
            """
            Comprehensive case analysis including multiple factors
            """
            analysis_results = {
                "relevance_score": self._calculate_relevance(case_data),
                "precedential_value": self._analyze_precedential_value(case_data),
                "key_points": self._extract_key_points(case_data),
                "citation_analysis": self._analyze_citations(case_data),
                "outcome_prediction": self._predict_outcome(case_data),
            }
            self.logger.logger.info(
                f"Completed analysis for case: {case_data.get('id', 'unknown')}"
            )
            self.monitor.end_operation("case_analysis", start_time)
            return analysis_results
        except Exception as e:
            self.logger.logger.error(f"Analysis failed: {str(e)}")
            self.monitor.end_operation("case_analysis", start_time, False, e)
            raise

    def _calculate_relevance(self, case_data: Dict) -> float:
        """Calculate relevance score based on multiple factors"""
        relevance_score = 0.0

        # Check recency
        if "date" in case_data["metadata"]:
            year = self._extract_year(case_data["metadata"]["date"])
            relevance_score += self._calculate_time_weight(year)

        # Check jurisdiction relevance
        if "court" in case_data["metadata"]:
            relevance_score += self.precedent_weight.get(case_data["metadata"]["court"], 0.4)

        # Check citation frequency
        citation_score = len(case_data.get("citations", [])) * 0.1
        relevance_score += min(citation_score, 1.0)

        return min(relevance_score / 3, 1.0)  # Normalize to 0-1

    def _analyze_precedential_value(self, case_data: Dict) -> Dict:
        """Analyze the precedential value of the case"""
        return {
            "court_level": self._determine_court_level(case_data),
            "citation_count": len(case_data.get("citations", [])),
            "subsequent_history": self._check_subsequent_history(case_data),
        }

    def _extract_key_points(self, case_data: Dict) -> List[str]:
        """Extract key legal points from the case"""
        key_points = []

        # Look for holding statements
        holdings = self._find_holdings(case_data["content"])
        key_points.extend(holdings)

        # Look for reasoning patterns
        reasoning = self._extract_reasoning(case_data["content"])
        key_points.extend(reasoning)

        return key_points

    def _analyze_citations(self, case_data: Dict) -> Dict:
        """Analyze the citation network"""
        citations = case_data.get("citations", [])
        return {
            "total_citations": len(citations),
            "citation_frequency": Counter(citations),
            "citation_patterns": self._identify_citation_patterns(citations),
        }

    def _extract_year(self, date_str: str) -> int:
        """Extract year from date string"""
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").year
        except ValueError:
            return datetime.now().year

    def _calculate_time_weight(self, year: int) -> float:
        """Calculate time-based weight"""
        current_year = datetime.now().year
        years_diff = current_year - year
        return max(0.1, 1 - (years_diff * 0.05))

    def _determine_court_level(self, case_data: Dict) -> str:
        """Determine the court level from case data"""
        court = case_data.get("metadata", {}).get("court", "")
        return court if court in self.precedent_weight else "Other"

    def _check_subsequent_history(self, case_data: Dict) -> Dict:
        """Check subsequent history of the case"""
        return {"overruled": False, "questioned": False, "followed": 0, "cited": 0}

    def _find_holdings(self, content: str) -> List[str]:
        """Extract holding statements from case content"""
        holdings = []
        holding_patterns = [
            r"The Court holds that.*?(?=\.)",
            r"We hold that.*?(?=\.)",
            r"It is hereby held that.*?(?=\.)",
        ]

        for pattern in holding_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            holdings.extend(match.group(0) for match in matches)

        return holdings

    def _extract_reasoning(self, content: str) -> List[str]:
        """Extract reasoning patterns from case content"""
        reasoning = []
        reasoning_patterns = [r"because.*?(?=\.)", r"therefore.*?(?=\.)", r"consequently.*?(?=\.)"]

        for pattern in reasoning_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            reasoning.extend(match.group(0) for match in matches)

        return reasoning

    def _predict_outcome(self, case_data: Dict) -> Dict:
        """Predict case outcome based on analysis"""
        try:
            strength_score = self._calculate_relevance(case_data)
            precedent_score = self._analyze_precedential_value(case_data)["citation_count"] / 100

            prediction_score = (strength_score + precedent_score) / 2

            return {
                "probability": prediction_score,
                "confidence": min(prediction_score * 1.2, 1.0),
                "factors": {"strength": strength_score, "precedent": precedent_score},
            }
        except Exception as e:
            return {"error": str(e), "probability": 0.5, "confidence": 0.0}
