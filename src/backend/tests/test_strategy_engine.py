import pytest
from ..strategy.suggestion_engine import StrategySuggestionEngine, Strategy, StrategyType


class TestStrategySuggestionEngine:
    @pytest.fixture
    def strategy_engine(self):
        return StrategySuggestionEngine()

    @pytest.fixture
    def sample_analysis(self):
        return {
            "evidence_score": 0.8,
            "precedent_score": 0.7,
            "coherence_score": 0.9,
            "counter_argument_strength": 0.4,
            "opposing_evidence_strength": 0.3,
        }

    def test_evaluate_case_strength(self, strategy_engine, sample_analysis):
        strength = strategy_engine._evaluate_case_strength(sample_analysis)
        assert 0 <= strength <= 1

    def test_generate_primary_strategy(self, strategy_engine):
        strategy = strategy_engine._generate_primary_strategy(0.8, 0.3)
        assert isinstance(strategy, Strategy)
        assert strategy.type == StrategyType.AGGRESSIVE
