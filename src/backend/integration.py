from typing import Dict, List
from .analysis.case_analysis import CaseAnalysis
from .weakness.analysis import WeaknessAnalysis
from .strategy.suggestion_engine import StrategySuggestionEngine
from .dual_perspective import DualPerspectiveAnalysis
from .scraper.legal_scraper import LegalScraper
from utils.logging_config import LegalLogger
from utils.monitoring import PerformanceMonitor


class LegalAnalysisIntegrator:
    def __init__(self):
        self.logger = LegalLogger(__name__)
        self.monitor = PerformanceMonitor()
        self.case_analyzer = CaseAnalysis()
        self.weakness_analyzer = WeaknessAnalysis()
        self.strategy_engine = StrategySuggestionEngine()
        self.dual_perspective = DualPerspectiveAnalysis()
        self.scraper = LegalScraper()

    def process_case(self, case_url: str) -> Dict:
        start_time = self.monitor.start_operation("case_processing")
        try:
            # Step 1: Scrape case data
            case_data = self.scraper.scrape(case_url)
            if not case_data:
                raise ValueError("Failed to scrape case data")

            # Step 2: Analyze case
            case_analysis = self.case_analyzer.analyze(case_data)

            # Step 3: Analyze weaknesses
            weaknesses = self.weakness_analyzer.analyze(case_analysis["key_points"])

            # Step 4: Generate strategies
            strategies = self.strategy_engine.suggest({**case_analysis, "weaknesses": weaknesses})

            # Step 5: Dual perspective analysis
            self.dual_perspective.process_arguments(case_analysis["key_points"])

            result = {
                "case_analysis": case_analysis,
                "weaknesses": weaknesses,
                "strategies": strategies,
                "dual_perspective": self.dual_perspective.get_summary(),
            }

            self.monitor.end_operation("case_processing", start_time)
            return result

        except Exception as e:
            self.logger.logger.error(f"Integration error: {str(e)}")
            self.monitor.end_operation("case_processing", start_time, False, e)
            raise
