"""
Brand extraction module for ReactRadar brand analysis system.
Handles extraction of brand names from text content.
"""

import os
import re
import json
from typing import List, Set, Optional
from dataclasses import dataclass
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI

load_dotenv()

@dataclass
class BrandMatch:
    """Represents a brand match found in text."""
    brand_name: str
    start_pos: int
    end_pos: int
    context: str

class BrandExtractor:
    """Extracts brand names from text content."""

    def __init__(self, known_brands: Optional[List[str]] = None):
        self.known_brands = set(known_brands) if known_brands is not None else set()
        self._build_brand_patterns()

        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            print("❌ OPENAI_API_KEY environment variable not found.")
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=openai_key)

        self.prompt = PromptTemplate.from_template("""
        You are an intelligent assistant.

        Your task is to read the transcript of a YouTube video reviewing protein powders and extract all brand names mentioned in the video.

        Only include real or recognizable product brands related to protein powders.

        Output the result as a valid JSON array like:
        ["Kirkland", "Isopure", "Transparent Labs", "Datiz"]

        Do NOT include any commentary, markdown, or explanation. Return only valid JSON.

        Transcript:
        {transcript}
        """)

        self.chain: RunnableSequence = self.prompt | self.llm

    def get_unique_brands(self, text: str) -> List[str]:
        response = self.chain.invoke({"transcript": text})
        print("🧪 Raw LLM response:", response)
        try:
            brands = json.loads(response.content)
            print("✅ Brands from LLM:", brands)
            return sorted(set(brands))
        except json.JSONDecodeError:
            print("❌ Failed to parse brand list:", response.content)
            return []

    def _build_brand_patterns(self) -> None:
        self.brand_patterns = [
            r'\b(?:' + '|'.join(re.escape(brand) for brand in self.known_brands) + r')\b',
            r'\b(?:Kirkland|Isopure|Transparent\s+Labs|Datiz|Accent|My\s+Protein|Optimum\s+Nutrition)\b',
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:brand|protein|powder|supplement)\b',
        ]

    def extract_brands_from_text(self, text: str) -> List[BrandMatch]:
        matches = []
        for pattern in self.brand_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                brand_name = self._clean_brand_name(match.group())
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end]
                matches.append(BrandMatch(
                    brand_name=brand_name,
                    start_pos=match.start(),
                    end_pos=match.end(),
                    context=context
                ))
        return sorted(self._deduplicate_matches(matches), key=lambda x: x.start_pos)

    def _clean_brand_name(self, brand_name: str) -> str:
        suffixes = [' brand', ' protein', ' powder', ' supplement']
        for suffix in suffixes:
            if brand_name.lower().endswith(suffix.lower()):
                brand_name = brand_name[:-len(suffix)]

        brand_mappings = {
            'my protein': 'My Protein',
            'optimum nutrition': 'Optimum Nutrition',
            'transparent labs': 'Transparent Labs',
        }
        return brand_mappings.get(brand_name.lower(), brand_name)

    def _deduplicate_matches(self, matches: List[BrandMatch]) -> List[BrandMatch]:
        seen = set()
        unique_matches = []
        for match in matches:
            key = (match.brand_name.lower(), match.start_pos // 100)
            if key not in seen:
                seen.add(key)
                unique_matches.append(match)
        return unique_matches

    def add_known_brands(self, brands: List[str]) -> None:
        self.known_brands.update(brands)
        self._build_brand_patterns()
