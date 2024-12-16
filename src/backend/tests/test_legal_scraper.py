import pytest
from ..scraper.legal_scraper import LegalScraper
from bs4 import BeautifulSoup


class TestLegalScraper:
    @pytest.fixture
    def scraper(self):
        return LegalScraper()

    @pytest.fixture
    def sample_html(self):
        return """
        <html>
            <h1>Sample Case Title</h1>
            <div>Filed on January 1, 2023</div>
            <div>Supreme Court of the United States</div>
            <div class="content">The Court holds that...</div>
        </html>
        """

    def test_extract_metadata(self, scraper, sample_html):
        soup = BeautifulSoup(sample_html, "html.parser")
        metadata = scraper._extract_metadata(soup)
        assert metadata["title"] is not None
        assert metadata["court"] is not None
