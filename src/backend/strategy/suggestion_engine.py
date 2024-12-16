# src/backend/strategy/suggestion_engine.py
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class StrategyType(Enum):
    AGGRESSIVE = "aggressive"
    DEFENSIVE = "defensive"
    BALANCED = "balanced"
    PRECEDENT_FOCUSED = "precedent_focused"
    POLICY_BASED = "policy_based"


@dataclass
class Strategy:
    type: StrategyType
    description: str
    recommended_actions: List[str]
    priority: int
    success_probability: float


class StrategySuggestionEngine:
    def __init__(self):
        self.strategy_templates = {
            StrategyType.AGGRESSIVE: {
                "description": "Focus on strong offensive arguments and direct challenges",
                "actions": [
                    "Challenge opposing evidence validity",
                    "Present strongest arguments first",
                    "Emphasize favorable precedents",
                ],
            },
            StrategyType.DEFENSIVE: {
                "description": "Build strong defensive position and counter-arguments",
                "actions": [
                    "Strengthen procedural compliance",
                    "Prepare detailed counter-arguments",
                    "Focus on evidence reliability",
                ],
            },
            StrategyType.BALANCED: {
                "description": "Maintain balanced approach",
                "actions": [
                    "Alternate between offensive and defensive points",
                    "Address key issues systematically",
                    "Maintain credibility through balanced presentation",
                ],
            },
        }

    def suggest(self, analysis_results: Dict) -> List[Strategy]:
        """Generate strategic suggestions based on case analysis"""
        strategies = []

        # Analyze case strength
        case_strength = self._evaluate_case_strength(analysis_results)

        # Analyze opposition strength
        opposition_strength = self._evaluate_opposition_strength(analysis_results)

        # Generate primary strategy
        primary_strategy = self._generate_primary_strategy(case_strength, opposition_strength)
        strategies.append(primary_strategy)

        # Generate supplementary strategies
        supplementary = self._generate_supplementary_strategies(analysis_results)
        strategies.extend(supplementary)

        return sorted(strategies, key=lambda x: x.priority, reverse=True)

    def _evaluate_case_strength(self, analysis: Dict) -> float:
        """Evaluate the overall strength of the case"""
        strength_factors = {
            "evidence_strength": analysis.get("evidence_score", 0.5),
            "precedent_support": analysis.get("precedent_score", 0.5),
            "argument_coherence": analysis.get("coherence_score", 0.5),
        }
        return sum(strength_factors.values()) / len(strength_factors)

    def _evaluate_opposition_strength(self, analysis: Dict) -> float:
        """Evaluate the strength of opposition's case"""
        opposition_factors = {
            "counter_arguments": analysis.get("counter_argument_strength", 0.5),
            "opposing_evidence": analysis.get("opposing_evidence_strength", 0.5),
        }
        return sum(opposition_factors.values()) / len(opposition_factors)

    def _generate_primary_strategy(
        self, case_strength: float, opposition_strength: float
    ) -> Strategy:
        """Generate primary strategy based on case analysis"""
        if case_strength > 0.7 and opposition_strength < 0.5:
            return Strategy(
                type=StrategyType.AGGRESSIVE,
                description=self.strategy_templates[StrategyType.AGGRESSIVE]["description"],
                recommended_actions=self.strategy_templates[StrategyType.AGGRESSIVE]["actions"],
                priority=1,
                success_probability=case_strength,
            )
        elif opposition_strength > 0.7:
            return Strategy(
                type=StrategyType.DEFENSIVE,
                description=self.strategy_templates[StrategyType.DEFENSIVE]["description"],
                recommended_actions=self.strategy_templates[StrategyType.DEFENSIVE]["actions"],
                priority=1,
                success_probability=1 - opposition_strength,
            )
        else:
            return Strategy(
                type=StrategyType.BALANCED,
                description=self.strategy_templates[StrategyType.BALANCED]["description"],
                recommended_actions=self.strategy_templates[StrategyType.BALANCED]["actions"],
                priority=1,
                success_probability=(case_strength + (1 - opposition_strength)) / 2,
            )

    def _generate_supplementary_strategies(self, analysis: Dict) -> List[Strategy]:
        """Generate supplementary strategies based on specific case aspects"""
        supplementary = []

        # Add precedent-focused strategy if strong precedents exist
        if analysis.get("precedent_score", 0) > 0.7:
            supplementary.append(
                Strategy(
                    type=StrategyType.PRECEDENT_FOCUSED,
                    description="Leverage strong precedential support",
                    recommended_actions=[
                        "Focus on precedent application",
                        "Distinguish opposing cases",
                    ],
                    priority=2,
                    success_probability=analysis["precedent_score"],
                )
            )

        return supplementary
