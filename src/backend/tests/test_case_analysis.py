import pytest
from ..analysis.case_analysis import CaseAnalysis


class TestCaseAnalysis:
    @pytest.fixture
    def case_analyzer(self):
        return CaseAnalysis()

    @pytest.fixture
    def sample_case_data(self):
        return {
            "id": "case123",
            "metadata": {"date": "2023-01-01", "court": "Supreme Court", "case_number": "123-456"},
            "content": "The Court holds that...",
            "citations": ["410 U.S. 113", "347 U.S. 483"],
        }

    def test_calculate_relevance(self, case_analyzer, sample_case_data):
        score = case_analyzer._calculate_relevance(sample_case_data)
        assert 0 <= score <= 1
        assert isinstance(score, float)

    def test_analyze_precedential_value(self, case_analyzer, sample_case_data):
        value = case_analyzer._analyze_precedential_value(sample_case_data)
        assert "court_level" in value
        assert "citation_count" in value
        assert value["citation_count"] == 2
