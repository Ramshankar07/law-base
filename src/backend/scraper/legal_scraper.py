import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from typing import Dict, List, Optional


class LegalScraper:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "}
        # Common legal document structure markers
        self.section_markers = [
            "OPINION",
            "BACKGROUND",
            "DISCUSSION",
            "CONCLUSION",
            "FINDINGS OF FACT",
            "CONCLUSIONS OF LAW",
        ]

    def scrape(self, url: str) -> Dict:
        """
        Scrapes legal documents with intelligent section recognition
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract document metadata
            metadata = self._extract_metadata(soup)

            # Extract main content
            content = self._extract_content(soup)

            # Extract citations
            citations = self._extract_citations(content)

            return {
                "metadata": metadata,
                "content": content,
                "citations": citations,
                "sections": self._identify_sections(content),
            }
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None

    def _extract_metadata(self, soup: BeautifulSoup) -> Dict:
        """Extract document metadata"""
        metadata = {
            "title": soup.find("h1"),
            "date": self._find_date(soup),
            "court": self._find_court(soup),
            "case_number": self._find_case_number(soup),
        }
        return {k: v.text.strip() if v else None for k, v in metadata.items()}

    def _extract_citations(self, text: str) -> List[str]:
        """Extract legal citations using regex patterns"""
        citation_patterns = [
            r"\d+\s+U\.S\.\s+\d+",  # US Reports citations
            r"\d+\s+F\.\d+d\s+\d+",  # Federal Reporter citations
            r"\d+\s+S\.Ct\.\s+\d+",  # Supreme Court Reporter citations
        ]
        citations = []
        for pattern in citation_patterns:
            citations.extend(re.findall(pattern, text))
        return citations

    def _identify_sections(self, text: str) -> Dict[str, str]:
        """Identify different sections in the legal document"""
        sections = {}
        current_section = None
        current_content = []

        for line in text.split("\n"):
            # Check if line is a section header
            if any(marker in line.upper() for marker in self.section_markers):
                if current_section:
                    sections[current_section] = "\n".join(current_content)
                current_section = line.strip()
                current_content = []
            elif current_section:
                current_content.append(line)

        return sections

    def _find_date(self, soup: BeautifulSoup) -> Optional[str]:
        """Find and extract date from document"""
        date_patterns = [
            r"\d{1,2}/\d{1,2}/\d{4}",
            r"\d{4}-\d{2}-\d{2}",
            r"[A-Z][a-z]+ \d{1,2}, \d{4}",
        ]
        for pattern in date_patterns:
            date_match = soup.find(string=re.compile(pattern))
            if date_match:
                return date_match.strip()
        return None

    def _find_court(self, soup: BeautifulSoup) -> Optional[str]:
        """Find and extract court information"""
        court_markers = ["COURT", "Circuit", "District"]
        for marker in court_markers:
            court_elem = soup.find(string=re.compile(marker))
            if court_elem:
                return court_elem.strip()
        return None
