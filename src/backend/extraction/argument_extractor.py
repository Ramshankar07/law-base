# src/backend/extraction/argument_extractor.py
import spacy
from typing import List, Dict
import re


class ArgumentExtractor:
    def __init__(self):
        # Load SpaCy model for NLP tasks
        self.nlp = spacy.load("en_core_web_sm")

        # Keywords indicating argumentative statements
        self.argument_indicators = [
            "therefore",
            "thus",
            "hence",
            "consequently",
            "because",
            "since",
            "as",
            "given that",
            "argues that",
            "contends that",
            "claims that",
        ]

        # Legal reasoning patterns
        self.legal_patterns = [
            r"The Court (holds|finds|concludes)",
            r"(Plaintiff|Defendant) argues that",
            r"We conclude that",
            r"It follows that",
        ]

    def extract_arguments(self, legal_text: str) -> Dict:
        """
        Extract and classify legal arguments from text
        """
        doc = self.nlp(legal_text)

        arguments = {
            "main_arguments": self._extract_main_arguments(doc),
            "supporting_arguments": self._extract_supporting_arguments(doc),
            "counter_arguments": self._extract_counter_arguments(doc),
            "conclusions": self._extract_conclusions(doc),
        }

        return arguments

    def _extract_main_arguments(self, doc) -> List[str]:
        """Extract main legal arguments"""
        main_arguments = []

        # Process each sentence
        for sent in doc.sents:
            # Check for argument indicators
            if any(indicator in sent.text.lower() for indicator in self.argument_indicators):
                main_arguments.append(sent.text.strip())

            # Check for legal patterns
            if any(re.search(pattern, sent.text) for pattern in self.legal_patterns):
                main_arguments.append(sent.text.strip())

        return main_arguments

    def _extract_supporting_arguments(self, doc) -> List[str]:
        """Extract supporting arguments"""
        supporting_args = []

        for sent in doc.sents:
            # Look for supporting argument patterns
            if any(word.text.lower() in ["because", "since", "as"] for word in sent):
                supporting_args.append(sent.text.strip())

        return supporting_args

    def _extract_counter_arguments(self, doc) -> List[str]:
        """Extract counter-arguments"""
        counter_args = []

        for sent in doc.sents:
            # Look for counter-argument patterns
            if any(
                word.text.lower() in ["however", "nevertheless", "although", "but"] for word in sent
            ):
                counter_args.append(sent.text.strip())

        return counter_args

    def _extract_conclusions(self, doc) -> List[str]:
        """Extract legal conclusions"""
        conclusions = []

        conclusion_patterns = [r"Therefore,.*", r"Thus,.*", r"Accordingly,.*", r"In conclusion,.*"]

        for sent in doc.sents:
            if any(re.match(pattern, sent.text) for pattern in conclusion_patterns):
                conclusions.append(sent.text.strip())

        return conclusions

    def analyze_argument_strength(self, argument: str) -> Dict:
        """Analyze the strength of an argument"""
        doc = self.nlp(argument)

        return {
            "citation_count": self._count_citations(argument),
            "precedent_references": self._find_precedent_references(doc),
            "reasoning_indicators": self._count_reasoning_indicators(doc),
            "confidence_score": self._calculate_confidence_score(doc),
        }
