# src/backend/prediction/counter_argument.py
from typing import List, Dict
import spacy
from collections import defaultdict


class CounterArgumentPredictor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

        # Common legal argument patterns
        self.argument_patterns = {
            "statutory": ["statute requires", "law states", "according to section"],
            "precedential": ["court held", "precedent establishes", "as decided in"],
            "factual": ["evidence shows", "facts demonstrate", "record indicates"],
            "policy": ["public policy", "legislative intent", "purpose of the law"],
        }

        # Counter-argument strategies
        self.counter_strategies = {
            "statutory": self._generate_statutory_counter,
            "precedential": self._generate_precedent_counter,
            "factual": self._generate_factual_counter,
            "policy": self._generate_policy_counter,
        }

    def predict(self, argument: str) -> List[Dict]:
        """
        Predict potential counter-arguments based on the input argument
        """
        doc = self.nlp(argument)

        # Identify argument type
        arg_type = self._identify_argument_type(doc)

        # Generate counter-arguments based on type
        counter_arguments = self._generate_counter_arguments(doc, arg_type)

        # Score and rank counter-arguments
        scored_counters = self._score_counter_arguments(counter_arguments, argument)

        return sorted(scored_counters, key=lambda x: x["strength"], reverse=True)

    def _identify_argument_type(self, doc) -> str:
        """Identify the type of legal argument"""
        type_scores = defaultdict(int)

        for token in doc:
            for arg_type, patterns in self.argument_patterns.items():
                if any(pattern in token.text.lower() for pattern in patterns):
                    type_scores[arg_type] += 1

        return max(type_scores.items(), key=lambda x: x[1])[0] if type_scores else "general"

    def _generate_counter_arguments(self, doc, arg_type: str) -> List[str]:
        """Generate counter-arguments based on argument type"""
        if arg_type in self.counter_strategies:
            return self.counter_strategies[arg_type](doc)
        return self._generate_general_counter(doc)

    def _generate_statutory_counter(self, doc) -> List[str]:
        """Generate counter-arguments for statutory interpretation"""
        counters = [
            "The statute should be interpreted differently considering...",
            "Legislative history suggests a different interpretation...",
            "The plain meaning rule leads to a different conclusion...",
        ]
        return counters

    def _generate_precedent_counter(self, doc) -> List[str]:
        """Generate counter-arguments for precedential arguments"""
        counters = [
            "This case is distinguishable from the cited precedent...",
            "Subsequent cases have limited this precedent's scope...",
            "The precedent's reasoning doesn't apply here because...",
        ]
        return counters

    def _generate_factual_counter(self, doc) -> List[str]:
        """Generate counter-arguments for factual claims"""
        counters = [
            "The evidence is insufficient to support this conclusion...",
            "Alternative interpretations of these facts suggest...",
            "Key contextual factors have been overlooked...",
        ]
        return counters

    def _generate_policy_counter(self, doc) -> List[str]:
        """Generate counter-arguments for policy arguments"""
        counters = [
            "This policy interpretation leads to unintended consequences...",
            "Competing policy considerations suggest...",
            "The proposed interpretation undermines the law's purpose...",
        ]
        return counters

    def _generate_general_counter(self, doc) -> List[str]:
        """Generate general counter-arguments"""
        return [
            "The argument fails to consider important factors...",
            "Alternative approaches would better serve the interests of justice...",
            "The reasoning is flawed because...",
        ]

    def _score_counter_arguments(self, counters: List[str], original_argument: str) -> List[Dict]:
        """Score counter-arguments based on relevance and strength"""
        scored_counters = []

        for counter in counters:
            score = self._calculate_counter_strength(counter, original_argument)
            scored_counters.append(
                {
                    "text": counter,
                    "strength": score,
                    "type": self._identify_argument_type(self.nlp(counter)),
                }
            )

        return scored_counters

    def _calculate_counter_strength(self, counter: str, original: str) -> float:
        """Calculate the strength of a counter-argument"""
        # Implement scoring logic based on:
        # - Relevance to original argument
        # - Logical structure
        # - Supporting evidence
        # This is a simplified version
        return 0.7  # Placeholder score
