"""
Sentiment analysis module for ReactRadar brand analysis system.
Handles sentiment analysis and rating calculations for brands.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import re


@dataclass
class SentimentResult:
    """Represents the result of sentiment analysis for a statement."""
    text: str
    label: str  # POSITIVE, NEGATIVE, NEUTRAL
    score: float
    rating: int  # 1-5 star rating


@dataclass
class BrandSentiment:
    """Represents sentiment analysis results for a brand."""
    brand: str
    statements: List[SentimentResult]
    avg_score: float
    avg_rating: float
    positive_count: int
    negative_count: int
    neutral_count: int


class SentimentAnalyzer:
    """Analyzes sentiment and ratings for brand-related statements."""

    def __init__(self):
        self.positive_keywords = {
            'excellent', 'great', 'good', 'best', 'outstanding', 'impressive',
            'recommend', 'love', 'enjoy', 'smooth', 'delicious', 'rich',
            'high quality', 'solid', 'versatile', 'convenient', 'effective'
        }

        self.negative_keywords = {
            'bad', 'poor', 'worst', 'terrible', 'disappointing', 'awful',
            'expensive', 'overpriced', 'clumpy', 'gritty', 'artificial',
            'aftertaste', 'digestive', 'discomfort', 'drawback', 'downside'
        }

        self.neutral_keywords = {
            'offers', 'contains', 'delivers', 'provides', 'includes',
            'available', 'priced', 'costs', 'flavors', 'serving'
        }

    def analyze_statement(self, text: str) -> SentimentResult:
        text_lower = text.lower()

        positive_count = sum(1 for word in self.positive_keywords if word in text_lower)
        negative_count = sum(1 for word in self.negative_keywords if word in text_lower)
        neutral_count = sum(1 for word in self.neutral_keywords if word in text_lower)

        total_keywords = positive_count + negative_count + neutral_count
        if total_keywords == 0:
            score = 0.5  # Neutral if no keywords found
        else:
            score = (positive_count - negative_count) / total_keywords
            score = (score + 1) / 2  # Normalize to 0-1 range

        if score > 0.6:
            label = "POSITIVE"
        elif score < 0.4:
            label = "NEGATIVE"
        else:
            label = "NEUTRAL"

        rating = self._score_to_rating(score)

        return SentimentResult(
            text=text,
            label=label,
            score=score,
            rating=rating
        )

    def _score_to_rating(self, score: float) -> int:
        if score >= 0.8:
            return 5
        elif score >= 0.6:
            return 4
        elif score >= 0.4:
            return 3
        elif score >= 0.2:
            return 2
        else:
            return 1

    def analyze_brand_statements(self, brand: str, statements: List[str]) -> BrandSentiment:
        sentiment_results = []

        for statement in statements:
            result = self.analyze_statement(statement)
            sentiment_results.append(result)

        if not sentiment_results:
            print(f"⚠️ No sentiment results for brand '{brand}'")
            return BrandSentiment(brand, [], 0.0, 0.0, 0, 0, 0)

        avg_score = sum(r.score for r in sentiment_results) / len(sentiment_results)
        avg_rating = sum(r.rating for r in sentiment_results) / len(sentiment_results)

        positive_count = sum(1 for r in sentiment_results if r.label == "POSITIVE")
        negative_count = sum(1 for r in sentiment_results if r.label == "NEGATIVE")
        neutral_count = sum(1 for r in sentiment_results if r.label == "NEUTRAL")

        return BrandSentiment(
            brand=brand,
            statements=sentiment_results,
            avg_score=avg_score,
            avg_rating=avg_rating,
            positive_count=positive_count,
            negative_count=negative_count,
            neutral_count=neutral_count
        )

    def extract_statements_about_brand(self, text: str, brand: str) -> List[str]:
        print(f"🔍 Extracting statements about brand: {brand}")
        statements = []
        brand_normalized = brand.lower().strip()

        # Split text into sentences
        sentences = re.split(r'[.!?]+', text)

        for sentence in sentences:
            sentence_clean = sentence.lower().strip()
            if brand_normalized in sentence_clean:
                statements.append(sentence.strip())

        print(f"📌 Found {len(statements)} statements for '{brand}'")
        return statements

    def create_rating_summary(self, brand_sentiment: BrandSentiment) -> Dict[str, Any]:
        total = len(brand_sentiment.statements)
        if total == 0:
            return {
                "brand": brand_sentiment.brand,
                "avg_rating": 0.0,
                "avg_score": 0.0,
                "total_statements": 0,
                "positive_percentage": 0.0,
                "negative_percentage": 0.0,
                "neutral_percentage": 0.0,
                "statements": []
            }

        return {
            "brand": brand_sentiment.brand,
            "avg_rating": round(brand_sentiment.avg_rating, 2),
            "avg_score": round(brand_sentiment.avg_score, 3),
            "total_statements": total,
            "positive_percentage": round(
                brand_sentiment.positive_count / total * 100, 1
            ),
            "negative_percentage": round(
                brand_sentiment.negative_count / total * 100, 1
            ),
            "neutral_percentage": round(
                brand_sentiment.neutral_count / total * 100, 1
            ),
            "statements": [
                {
                    "text": s.text,
                    "label": s.label,
                    "rating": s.rating
                }
                for s in brand_sentiment.statements
            ]
        }
