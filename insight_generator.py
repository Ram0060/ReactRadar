"""
Insight generator module for ReactRadar brand analysis system.
Handles generation of insights and summaries about brands.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from .brand_segmenter import BrandSegment, PriceCategory, QualityCategory


@dataclass
class BrandInsight:
    """Represents insights about a brand."""
    brand: str
    summary: str
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    key_features: List[str]
    target_audience: List[str]


class InsightGenerator:
    """Generates insights and summaries about brands."""
    
    def __init__(self):
        """Initialize the insight generator."""
        self.insight_templates = {
            "high_quality": "{} is a high-quality protein powder that delivers excellent results.",
            "budget_friendly": "{} offers great value for money, making it ideal for budget-conscious consumers.",
            "premium": "{} is a premium option with advanced features and superior quality.",
            "clean_ingredients": "{} stands out for its clean ingredient profile, appealing to health-conscious users.",
            "third_party_tested": "{} is third-party tested, providing additional quality assurance.",
            "artificial_sweeteners": "{} contains artificial sweeteners, which may be a concern for some users."
        }
    
    def generate_brand_insight(self, segment: BrandSegment, 
                             sentiment_data: Optional[Dict[str, Any]] = None) -> BrandInsight:
        """
        Generate comprehensive insights for a brand.
        
        Args:
            segment: BrandSegment object with brand data
            sentiment_data: Optional sentiment analysis data
            
        Returns:
            BrandInsight object
        """
        brand = segment.brand
        
        # Generate summary
        summary = self._generate_summary(segment, sentiment_data)
        
        # Identify strengths
        strengths = self._identify_strengths(segment, sentiment_data)
        
        # Identify weaknesses
        weaknesses = self._identify_weaknesses(segment, sentiment_data)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(segment, sentiment_data)
        
        # Key features
        key_features = segment.features.copy()
        
        # Target audience
        target_audience = self._identify_target_audience(segment)
        
        return BrandInsight(
            brand=brand,
            summary=summary,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
            key_features=key_features,
            target_audience=target_audience
        )
    
    def _generate_summary(self, segment: BrandSegment, 
                         sentiment_data: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate a summary for the brand.
        
        Args:
            segment: BrandSegment object
            sentiment_data: Optional sentiment data
            
        Returns:
            Summary string
        """
        brand = segment.brand
        rating = segment.avg_rating
        price = segment.price_per_serving
        
        summary_parts = []
        
        # Quality assessment
        if segment.quality_category == QualityCategory.PREMIUM:
            summary_parts.append(f"{brand} is a premium protein powder")
        elif segment.quality_category == QualityCategory.STANDARD:
            summary_parts.append(f"{brand} is a solid, reliable protein powder")
        else:
            summary_parts.append(f"{brand} is a basic protein powder")
        
        # Rating
        if rating >= 4.5:
            summary_parts.append("with excellent customer ratings")
        elif rating >= 4.0:
            summary_parts.append("with good customer ratings")
        else:
            summary_parts.append("with average customer ratings")
        
        # Price positioning
        if segment.price_category == PriceCategory.BUDGET:
            summary_parts.append("at an affordable price point")
        elif segment.price_category == PriceCategory.PREMIUM:
            summary_parts.append("at a premium price point")
        else:
            summary_parts.append("at a mid-range price point")
        
        # Special features
        if segment.third_party_tested:
            summary_parts.append("and is third-party tested for quality assurance")
        
        if not segment.artificial_sweeteners:
            summary_parts.append("with no artificial sweeteners")
        
        return " ".join(summary_parts) + "."
    
    def _identify_strengths(self, segment: BrandSegment, 
                          sentiment_data: Optional[Dict[str, Any]] = None) -> List[str]:
        """
        Identify strengths of the brand.
        
        Args:
            segment: BrandSegment object
            sentiment_data: Optional sentiment data
            
        Returns:
            List of strengths
        """
        strengths = []
        
        # Quality strengths
        if segment.quality_category == QualityCategory.PREMIUM:
            strengths.append("Premium quality and performance")
        elif segment.avg_rating >= 4.5:
            strengths.append("High customer satisfaction")
        
        # Price strengths
        if segment.price_category == PriceCategory.BUDGET:
            strengths.append("Excellent value for money")
        elif segment.price_per_serving and segment.price_per_serving < 1.0:
            strengths.append("Competitive pricing")
        
        # Feature strengths
        if segment.third_party_tested:
            strengths.append("Third-party quality testing")
        
        if not segment.artificial_sweeteners:
            strengths.append("Clean ingredient profile")
        
        if segment.protein_content and segment.protein_content >= 25:
            strengths.append("High protein content per serving")
        
        # Add features as strengths
        strengths.extend(segment.features)
        
        return strengths
    
    def _identify_weaknesses(self, segment: BrandSegment, 
                           sentiment_data: Optional[Dict[str, Any]] = None) -> List[str]:
        """
        Identify weaknesses of the brand.
        
        Args:
            segment: BrandSegment object
            sentiment_data: Optional sentiment data
            
        Returns:
            List of weaknesses
        """
        weaknesses = []
        
        # Quality weaknesses
        if segment.quality_category == QualityCategory.BASIC:
            weaknesses.append("Basic quality level")
        
        if segment.avg_rating < 4.0:
            weaknesses.append("Lower customer satisfaction")
        
        # Price weaknesses
        if segment.price_category == PriceCategory.PREMIUM:
            weaknesses.append("Higher price point")
        
        # Feature weaknesses
        if not segment.third_party_tested:
            weaknesses.append("No third-party testing")
        
        if segment.artificial_sweeteners:
            weaknesses.append("Contains artificial sweeteners")
        
        if segment.protein_content and segment.protein_content < 24:
            weaknesses.append("Lower protein content compared to competitors")
        
        return weaknesses
    
    def _generate_recommendations(self, segment: BrandSegment, 
                                sentiment_data: Optional[Dict[str, Any]] = None) -> List[str]:
        """
        Generate recommendations for the brand.
        
        Args:
            segment: BrandSegment object
            sentiment_data: Optional sentiment data
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Quality-based recommendations
        if segment.quality_category == QualityCategory.PREMIUM:
            recommendations.append("Ideal for serious athletes and fitness enthusiasts")
        elif segment.quality_category == QualityCategory.STANDARD:
            recommendations.append("Good choice for regular gym-goers")
        else:
            recommendations.append("Suitable for beginners or casual users")
        
        # Price-based recommendations
        if segment.price_category == PriceCategory.BUDGET:
            recommendations.append("Perfect for budget-conscious consumers")
        elif segment.price_category == PriceCategory.PREMIUM:
            recommendations.append("Best for those prioritizing quality over cost")
        
        # Feature-based recommendations
        if not segment.artificial_sweeteners:
            recommendations.append("Recommended for those avoiding artificial sweeteners")
        
        if segment.third_party_tested:
            recommendations.append("Recommended for athletes requiring quality assurance")
        
        # General recommendations
        if segment.avg_rating >= 4.5:
            recommendations.append("Highly recommended based on customer feedback")
        elif segment.avg_rating >= 4.0:
            recommendations.append("Recommended for most users")
        
        return recommendations
    
    def _identify_target_audience(self, segment: BrandSegment) -> List[str]:
        """
        Identify target audience for the brand.
        
        Args:
            segment: BrandSegment object
            
        Returns:
            List of target audience segments
        """
        audience = []
        
        # Quality-based audience
        if segment.quality_category == QualityCategory.PREMIUM:
            audience.extend(["Serious athletes", "Professional bodybuilders", "Fitness enthusiasts"])
        elif segment.quality_category == QualityCategory.STANDARD:
            audience.extend(["Regular gym-goers", "Fitness enthusiasts", "Health-conscious individuals"])
        else:
            audience.extend(["Beginners", "Casual users", "Budget-conscious consumers"])
        
        # Price-based audience
        if segment.price_category == PriceCategory.BUDGET:
            audience.append("Budget-conscious consumers")
        elif segment.price_category == PriceCategory.PREMIUM:
            audience.append("Premium market consumers")
        
        # Feature-based audience
        if not segment.artificial_sweeteners:
            audience.append("Health-conscious individuals")
        
        if segment.third_party_tested:
            audience.append("Competitive athletes")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_audience = []
        for item in audience:
            if item not in seen:
                seen.add(item)
                unique_audience.append(item)
        
        return unique_audience
    
    def generate_comparative_insights(self, segments: List[BrandSegment]) -> Dict[str, Any]:
        """
        Generate comparative insights across all brands.
        
        Args:
            segments: List of brand segments
            
        Returns:
            Dictionary with comparative insights
        """
        insights = {
            "best_value": None,
            "highest_quality": None,
            "most_affordable": None,
            "premium_choice": None,
            "clean_ingredients": [],
            "third_party_tested": [],
            "comparison_summary": ""
        }
        
        if not segments:
            return insights
        
        # Find best value (high quality, low price)
        high_quality = [s for s in segments if s.quality_category in [QualityCategory.STANDARD, QualityCategory.PREMIUM]]
        if high_quality:
            insights["best_value"] = min(high_quality, key=lambda x: x.price_per_serving or float('inf'))
        
        # Find highest quality
        insights["highest_quality"] = max(segments, key=lambda x: x.avg_rating)
        
        # Find most affordable
        insights["most_affordable"] = min(segments, key=lambda x: x.price_per_serving or float('inf'))
        
        # Find premium choice
        premium_brands = [s for s in segments if s.quality_category == QualityCategory.PREMIUM]
        if premium_brands:
            insights["premium_choice"] = max(premium_brands, key=lambda x: x.avg_rating)
        
        # Brands with clean ingredients
        insights["clean_ingredients"] = [s.brand for s in segments if not s.artificial_sweeteners]
        
        # Third-party tested brands
        insights["third_party_tested"] = [s.brand for s in segments if s.third_party_tested]
        
        # Generate comparison summary
        insights["comparison_summary"] = self._generate_comparison_summary(insights)
        
        return insights
    
    def _generate_comparison_summary(self, insights: Dict[str, Any]) -> str:
        """
        Generate a summary comparing all brands.
        
        Args:
            insights: Comparative insights dictionary
            
        Returns:
            Comparison summary string
        """
        summary_parts = []
        
        if insights["best_value"]:
            summary_parts.append(f"For best value, consider {insights['best_value'].brand}")
        
        if insights["highest_quality"]:
            summary_parts.append(f"For highest quality, {insights['highest_quality'].brand} leads the pack")
        
        if insights["most_affordable"]:
            summary_parts.append(f"{insights['most_affordable'].brand} is the most affordable option")
        
        if insights["premium_choice"]:
            summary_parts.append(f"For premium quality, {insights['premium_choice'].brand} is the top choice")
        
        if insights["clean_ingredients"]:
            brands = ", ".join(insights["clean_ingredients"])
            summary_parts.append(f"Brands with clean ingredients: {brands}")
        
        if insights["third_party_tested"]:
            brands = ", ".join(insights["third_party_tested"])
            summary_parts.append(f"Third-party tested brands: {brands}")
        
        return " ".join(summary_parts) + "." 