# src/backend/dual_perspective.py
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import spacy
from utils.logging_config import LegalLogger
from utils.monitoring import PerformanceMonitor


class ArgumentType(Enum):
    FACTUAL = "factual"
    LEGAL = "legal"
    PROCEDURAL = "procedural"
    POLICY = "policy"


@dataclass
class Argument:
    text: str
    type: ArgumentType
    strength: float
    supporting_citations: List[str]
    counter_arguments: List[str]


class DualPerspectiveAnalysis:
    def __init__(self):
        self.logger = LegalLogger(__name__)
        self.monitor = PerformanceMonitor()
        self.prosecution_track: List[Argument] = []
        self.defense_track: List[Argument] = []
        self.shared_facts: List[str] = []
        self.disputed_facts: Dict[str, Dict[str, str]] = {}
        self.nlp = spacy.load("en_core_web_md")

    def add_prosecution_argument(self, argument: Argument) -> None:
        start_time = self.monitor.start_operation("add_prosecution_argument")
        try:
            """Add a prosecution argument with metadata"""
            self.prosecution_track.append(argument)
            self._analyze_argument_conflicts(argument, "prosecution")
            self.logger.logger.info(f"Added prosecution argument: {argument.text[:50]}...")
            self.monitor.end_operation("add_prosecution_argument", start_time)
        except Exception as e:
            self.logger.logger.error(f"Failed to add prosecution argument: {str(e)}")
            self.monitor.end_operation("add_prosecution_argument", start_time, False, e)
            raise

    def add_defense_argument(self, argument: Argument) -> None:
        """Add a defense argument with metadata"""
        self.defense_track.append(argument)
        self._analyze_argument_conflicts(argument, "defense")

    def add_shared_fact(self, fact: str) -> None:
        """Add a fact that both sides agree on"""
        self.shared_facts.append(fact)

    def add_disputed_fact(self, fact: str, prosecution_view: str, defense_view: str) -> None:
        """Add a disputed fact with both sides' perspectives"""
        self.disputed_facts[fact] = {"prosecution": prosecution_view, "defense": defense_view}

    def get_argument_strength_analysis(self) -> Dict:
        """Analyze the relative strength of each side's arguments"""
        return {
            "prosecution": self._calculate_track_strength(self.prosecution_track),
            "defense": self._calculate_track_strength(self.defense_track),
        }

    def _calculate_track_strength(self, arguments: List[Argument]) -> float:
        """Calculate the overall strength of a track's arguments"""
        if not arguments:
            return 0.0

        total_strength = sum(arg.strength for arg in arguments)
        return total_strength / len(arguments)

    def _analyze_argument_conflicts(self, argument: Argument, side: str) -> None:
        """Analyze potential conflicts with opposing arguments"""
        opposing_track = self.defense_track if side == "prosecution" else self.prosecution_track

        for opposing_arg in opposing_track:
            if self._arguments_conflict(argument, opposing_arg):
                argument.counter_arguments.append(opposing_arg.text)

    def _arguments_conflict(self, arg1: Argument, arg2: Argument) -> bool:
        """Check if two arguments directly conflict"""
        try:
            # Check for direct contradictions
            if arg1.type != arg2.type:
                return False

            # Use spaCy for semantic similarity
            doc1 = self.nlp(arg1.text)
            doc2 = self.nlp(arg2.text)

            similarity = doc1.similarity(doc2)

            # High similarity but opposite stances indicates conflict
            if similarity > 0.7:
                # Check for opposing indicators
                opposing_pairs = [
                    ("supports", "opposes"),
                    ("proves", "disproves"),
                    ("confirms", "contradicts"),
                ]

                for pos, neg in opposing_pairs:
                    if (pos in arg1.text.lower() and neg in arg2.text.lower()) or (
                        neg in arg1.text.lower() and pos in arg2.text.lower()
                    ):
                        return True

            return False
        except Exception as e:
            print(f"Error in conflict detection: {e}")
            return False

    def get_summary(self) -> Dict:
        """Get a summary of the dual perspective analysis"""
        return {
            "prosecution_arguments": len(self.prosecution_track),
            "defense_arguments": len(self.defense_track),
            "shared_facts": len(self.shared_facts),
            "disputed_facts": len(self.disputed_facts),
            "strength_analysis": self.get_argument_strength_analysis(),
        }
