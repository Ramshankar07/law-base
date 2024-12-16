import pytest
from ..weakness.analysis import WeaknessAnalysis, Weakness


class TestWeaknessAnalysis:
    @pytest.fixture
    def weakness_analyzer(self):
        return WeaknessAnalysis()

    @pytest.fixture
    def sample_arguments(self):
        return [
            {
                "text": "The evidence clearly shows...",
                "type": "factual",
                "evidence": ["Document A", "Witness B"],
                "evidence_quality": 0.8,
            }
        ]

    def test_analyze_evidence(self, weakness_analyzer, sample_arguments):
        weaknesses = weakness_analyzer._analyze_evidence(sample_arguments[0])
        assert isinstance(weaknesses, list)
        assert all(isinstance(w, Weakness) for w in weaknesses)

    def test_analyze_logic(self, weakness_analyzer, sample_arguments):
        weaknesses = weakness_analyzer._analyze_logic(sample_arguments[0])
        assert isinstance(weaknesses, list)
