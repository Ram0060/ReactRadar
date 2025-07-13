from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .data_loader import DataLoader
from .brand_extractor import BrandExtractor
from .sentiment_analyzer import SentimentAnalyzer, BrandSentiment
from .brand_segmenter import BrandSegmenter, BrandSegment
from .insight_generator import InsightGenerator, BrandInsight


@dataclass
class AnalysisResult:
    brands: List[str]
    brand_ratings: List[Dict[str, Any]]
    brand_sentiments: List[BrandSentiment]
    brand_segments: List[BrandSegment]
    brand_insights: List[BrandInsight]
    comparative_insights: Dict[str, Any]
    summary: Dict[str, Any]


class ReactRadarEngine:
    def __init__(self, data_dir: str = "experiment"):
        self.data_loader = DataLoader(data_dir)
        self.brand_extractor = BrandExtractor()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.brand_segmenter = BrandSegmenter()
        self.insight_generator = InsightGenerator()

    def run_full_analysis(self, transcript: Optional[str] = None) -> AnalysisResult:
        if transcript is None:
            transcript = self.data_loader.load_transcript()

        print("\n🔍 Extracting brands...")
        brands = self.brand_extractor.get_unique_brands(transcript)
        if not brands:
            print("⚠️ No brands found in transcript. Exiting early.")
            return AnalysisResult([], [], [], [], [], {}, {})

        print(f"✅ Found {len(brands)} brands: {brands}")
        self.brand_extractor.add_known_brands(brands)

        brand_sentiments = []
        brand_ratings = []

        for brand in brands:
            print(f"\n💬 Processing brand: {brand}")
            statements = self.sentiment_analyzer.extract_statements_about_brand(transcript, brand)
            print(f"📌 Found {len(statements)} statements")
            if not statements:
                print(f"⚠️ No statements for {brand}, assigning neutral sentiment.")
                neutral_sentiment = BrandSentiment(
                    brand=brand,
                    statements=[],
                    avg_score=0.5,
                    avg_rating=3.0,
                    positive_count=0,
                    negative_count=0,
                    neutral_count=0
                )
                brand_sentiments.append(neutral_sentiment)
                brand_ratings.append({
                    "brand": brand,
                    "avg_rating": 3.0,
                    "avg_score": 0.5,
                    "total_statements": 0,
                    "positive_percentage": 0.0,
                    "negative_percentage": 0.0,
                    "neutral_percentage": 0.0,
                    "statements": []
                })
                continue

            sentiment = self.sentiment_analyzer.analyze_brand_statements(brand, statements)
            brand_sentiments.append(sentiment)
            rating_summary = self.sentiment_analyzer.create_rating_summary(sentiment)
            brand_ratings.append(rating_summary)

        if not brand_ratings:
            print("⚠️ No ratings found. Skipping downstream tasks.")
            return AnalysisResult(brands, brand_ratings, brand_sentiments, [], [], {}, {})

        brand_segments = self.brand_segmenter.segment_all_brands(brand_ratings)

        brand_insights = []
        for segment in brand_segments:
            sentiment_data = next((s for s in brand_sentiments if s.brand == segment.brand), None)
            if not sentiment_data:
                print(f"⚠️ No sentiment data for {segment.brand}. Skipping insight.")
                continue

            insight = self.insight_generator.generate_brand_insight(segment, sentiment_data)
            if not insight:
                print(f"⚠️ Insight generation failed for {segment.brand}")
                continue

            brand_insights.append(insight)

        comparative_insights = self.insight_generator.generate_comparative_insights(brand_segments)
        summary = self._create_analysis_summary(brands, brand_ratings, brand_segments)

        print("\n📦 Analysis complete.")
        return AnalysisResult(
            brands=brands,
            brand_ratings=brand_ratings,
            brand_sentiments=brand_sentiments,
            brand_segments=brand_segments,
            brand_insights=brand_insights,
            comparative_insights=comparative_insights,
            summary=summary
        )

    def run_full_pipeline(self, transcript: str) -> None:
        print("\n🚀 Running full pipeline...")
        result = self.run_full_analysis(transcript)
        self.save_analysis_results(result)

    def save_analysis_results(self, result: AnalysisResult, output_dir: str = "experiment") -> None:
        print("\n💾 Saving analysis results...")
        self.data_loader.save_json(result.brand_ratings, "brand_ratings.json")

        sentiment_data = []
        for sentiment in result.brand_sentiments:
            sentiment_data.append({
                "brand": sentiment.brand,
                "statements": [
                    {"text": s.text, "label": s.label, "score": s.score}
                    for s in sentiment.statements
                ]
            })
        self.data_loader.save_json(sentiment_data, "brand_sentiment_analysis.json")

        segment_data = self.brand_segmenter.create_segmentation_summary(result.brand_segments)
        self.data_loader.save_json(segment_data, "brand_segmented.json")

        insight_data = []
        for insight in result.brand_insights:
            insight_data.append({
                "brand": insight.brand,
                "summary": insight.summary,
                "strengths": insight.strengths,
                "weaknesses": insight.weaknesses,
                "recommendations": insight.recommendations,
                "key_features": insight.key_features,
                "target_audience": insight.target_audience
            })
        self.data_loader.save_json(insight_data, "brand_insight_summaries.json")

        self.data_loader.save_json(result.comparative_insights, "comparative_insights.json")
        self.data_loader.save_json(result.summary, "analysis_summary.json")
        print("✅ All results saved to disk.")

    def _create_analysis_summary(self, brands: List[str],
                                 brand_ratings: List[Dict[str, Any]],
                                 brand_segments: List[BrandSegment]) -> Dict[str, Any]:
        total_brands = len(brands)
        if not brand_ratings:
            return {"error": "No brand ratings available"}

        avg_rating = sum(r["avg_rating"] for r in brand_ratings) / len(brand_ratings)
        highest_rated = max(brand_ratings, key=lambda x: x["avg_rating"])
        lowest_rated = min(brand_ratings, key=lambda x: x["avg_rating"])

        budget_brands = [s for s in brand_segments if s.price_category.value == "budget"]
        premium_brands = [s for s in brand_segments if s.price_category.value == "premium"]
        high_quality_brands = [s for s in brand_segments if s.quality_category.value in ["standard", "premium"]]

        return {
            "total_brands_analyzed": total_brands,
            "average_rating": round(avg_rating, 2),
            "highest_rated_brand": {
                "brand": highest_rated["brand"],
                "rating": highest_rated["avg_rating"]
            },
            "lowest_rated_brand": {
                "brand": lowest_rated["brand"],
                "rating": lowest_rated["avg_rating"]
            },
            "price_distribution": {
                "budget_brands": len(budget_brands),
                "premium_brands": len(premium_brands),
                "mid_range_brands": total_brands - len(budget_brands) - len(premium_brands)
            },
            "quality_distribution": {
                "high_quality_brands": len(high_quality_brands),
                "basic_quality_brands": total_brands - len(high_quality_brands)
            },
            "analysis_timestamp": "2024-01-01T00:00:00Z"
        }
