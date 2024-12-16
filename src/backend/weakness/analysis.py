# src/backend/weakness/analysis.py
from typing import List, Dict, Optional
from dataclasses import dataclass
import spacy
from collections import defaultdict
from utils.validators import DataValidator
from utils.logging_config import LegalLogger
from utils.monitoring import PerformanceMonitor


@dataclass
class Weakness:
    description: str
    severity: float  # 0 to 1
    type: str
    potential_remedies: List[str]


class WeaknessAnalysis:
    def __init__(self):
        self.logger = LegalLogger(__name__)
        self.monitor = PerformanceMonitor()
        self.nlp = spacy.load("en_core_web_sm")

        # Define common weakness patterns
        self.weakness_patterns = {
            "evidence_gaps": ["lack of evidence", "insufficient proof", "no direct evidence"],
            "logical_flaws": ["circular reasoning", "false equivalence", "hasty generalization"],
            "precedent_issues": [
                "distinguishable cases",
                "outdated precedent",
                "conflicting authorities",
            ],
        }

    def analyze(self, arguments: List[Dict]) -> List[Weakness]:
        start_time = self.monitor.start_operation("weakness_analysis")
        try:
            weaknesses = []

            for argument in arguments:
                # Validate argument structure
                error = DataValidator.validate_argument(argument)
                if error:
                    print(f"Skipping invalid argument: {error}")
                    continue

                # Analyze evidence strength
                evidence_weaknesses = self._analyze_evidence(argument)
                weaknesses.extend(evidence_weaknesses)

                # Analyze logical consistency
                logical_weaknesses = self._analyze_logic(argument)
                weaknesses.extend(logical_weaknesses)

                # Analyze precedential support
                precedent_weaknesses = self._analyze_precedents(argument)
                weaknesses.extend(precedent_weaknesses)

            self.logger.logger.info(f"Completed weakness analysis for {len(arguments)} arguments")
            self.monitor.end_operation("weakness_analysis", start_time)
            return self._prioritize_weaknesses(weaknesses)
        except Exception as e:
            self.logger.logger.error(f"Weakness analysis failed: {str(e)}")
            self.monitor.end_operation("weakness_analysis", start_time, False, e)
            return []

    def _analyze_evidence(self, argument: Dict) -> List[Weakness]:
        """Analyze evidence-related weaknesses"""
        weaknesses = []

        # Check for evidence gaps
        if "evidence" not in argument or not argument["evidence"]:
            weaknesses.append(
                Weakness(
                    description="Lack of supporting evidence",
                    severity=0.8,
                    type="evidence_gap",
                    potential_remedies=[
                        "Gather additional documentary evidence",
                        "Identify potential witnesses",
                        "Consider expert testimony",
                    ],
                )
            )

        # Check evidence quality
        if "evidence_quality" in argument and argument["evidence_quality"] < 0.6:
            weaknesses.append(
                Weakness(
                    description="Low quality or unreliable evidence",
                    severity=0.7,
                    type="evidence_quality",
                    potential_remedies=[
                        "Strengthen chain of custody",
                        "Obtain corroborating evidence",
                        "Address authentication issues",
                    ],
                )
            )

        return weaknesses

    def _analyze_logic(self, argument: Dict) -> List[Weakness]:
        """Analyze logical weaknesses in arguments"""
        weaknesses = []

        # Analyze argument structure
        doc = self.nlp(argument.get("text", ""))

        # Check for logical fallacies
        for sent in doc.sents:
            for fallacy_type, patterns in self.weakness_patterns["logical_flaws"]:
                if any(pattern in sent.text.lower() for pattern in patterns):
                    weaknesses.append(
                        Weakness(
                            description=f"Potential logical fallacy: {fallacy_type}",
                            severity=0.6,
                            type="logical_flaw",
                            potential_remedies=[
                                "Restructure argument logic",
                                "Address causal relationships",
                                "Strengthen logical connections",
                            ],
                        )
                    )

        return weaknesses

    def _analyze_precedents(self, argument: Dict) -> List[Weakness]:
        """Analyze precedent-related weaknesses"""
        weaknesses = []

        # Check precedent strength
        if "precedents" in argument:
            for precedent in argument["precedents"]:
                if precedent.get("distinguishable", False):
                    weaknesses.append(
                        Weakness(
                            description="Distinguishable precedent",
                            severity=0.5,
                            type="precedent_weakness",
                            potential_remedies=[
                                "Find more analogous cases",
                                "Address distinguishing factors",
                                "Emphasize policy considerations",
                            ],
                        )
                    )

        return weaknesses

    def _prioritize_weaknesses(self, weaknesses: List[Weakness]) -> List[Weakness]:
        """Prioritize weaknesses based on severity and type"""
        return sorted(weaknesses, key=lambda x: x.severity, reverse=True)

    def get_summary(self, weaknesses: List[Weakness]) -> Dict:
        """Generate a summary of weakness analysis"""
        return {
            "total_weaknesses": len(weaknesses),
            "critical_weaknesses": len([w for w in weaknesses if w.severity > 0.7]),
            "by_type": self._group_by_type(weaknesses),
            "remediation_priority": self._get_remediation_priority(weaknesses),
        }

    def _group_by_type(self, weaknesses: List[Weakness]) -> Dict:
        """Group weaknesses by type"""
        grouped = defaultdict(list)
        for weakness in weaknesses:
            grouped[weakness.type].append(weakness)
        return dict(grouped)

    def _get_remediation_priority(self, weaknesses: List[Weakness]) -> List[Dict]:
        """Generate prioritized remediation list"""
        return [
            {"weakness": w.description, "remedies": w.potential_remedies, "priority": w.severity}
            for w in sorted(weaknesses, key=lambda x: x.severity, reverse=True)
        ]
