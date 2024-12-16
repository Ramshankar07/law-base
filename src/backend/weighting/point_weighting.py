# src/backend/weighting/point_weighting.py
from typing import Dict, List, Union
from datetime import datetime


class PointWeighting:
    def __init__(self):
        # Initialize weighting factors
        self.court_hierarchy_weights = {
            "Supreme Court": 1.0,
            "Circuit Court": 0.8,
            "District Court": 0.6,
            "State Supreme Court": 0.7,
            "State Appellate Court": 0.5,
            "State Trial Court": 0.4,
        }

        # Time decay factor (more recent cases get higher weight)
        self.time_decay_factor = 0.98

        # Citation impact threshold
        self.citation_threshold = 50

    def weight_points(self, case: Dict) -> Dict[str, float]:
        """
        Calculate weighted scores for different aspects of a legal case
        """
        weights = {
            "relevance": self._calculate_relevance_weight(case),
            "citation_frequency": self._calculate_citation_weight(case),
            "court_hierarchy": self._calculate_hierarchy_weight(case),
            "case_outcome_impact": self._calculate_outcome_impact(case),
            "temporal_relevance": self._calculate_temporal_weight(case),
        }

        # Normalize weights
        total_weight = sum(weights.values())
        return {k: v / total_weight for k, v in weights.items()}

    def _calculate_relevance_weight(self, case: Dict) -> float:
        """Calculate relevance based on keyword matching and context"""
        relevance_score = 0.0

        if "keywords" in case:
            # Weight based on keyword matches
            relevance_score += len(case["keywords"]) * 0.1

        if "context_similarity" in case:
            # Weight based on context similarity
            relevance_score += case["context_similarity"] * 0.5

        return min(relevance_score, 1.0)

    def _calculate_citation_weight(self, case: Dict) -> float:
        """Calculate weight based on citation frequency"""
        citations = case.get("citation_count", 0)
        return min(citations / self.citation_threshold, 1.0)

    def _calculate_hierarchy_weight(self, case: Dict) -> float:
        """Calculate weight based on court hierarchy"""
        court_type = case.get("court_type", "District Court")
        return self.court_hierarchy_weights.get(court_type, 0.4)

    def _calculate_outcome_impact(self, case: Dict) -> float:
        """Calculate weight based on case outcome impact"""
        impact_factors = {
            "precedent_setting": 0.3,
            "overturned_previous": 0.2,
            "widely_cited": 0.2,
            "current_relevance": 0.3,
        }

        impact_score = 0.0
        for factor, weight in impact_factors.items():
            if case.get(factor, False):
                impact_score += weight

        return impact_score

    def _calculate_temporal_weight(self, case: Dict) -> float:
        """Calculate weight based on temporal relevance"""
        if "date" not in case:
            return 0.5

        case_year = datetime.strptime(case["date"], "%Y-%m-%d").year
        current_year = datetime.now().year
        years_diff = current_year - case_year

        return self.time_decay_factor**years_diff
