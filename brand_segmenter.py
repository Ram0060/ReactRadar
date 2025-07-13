"""
Brand segmentation module for ReactRadar brand analysis system.
Handles categorization and segmentation of brands by various criteria.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class PriceCategory(Enum):
    """Price categories for brands."""
    BUDGET = "budget"
    MID_RANGE = "mid_range"
    PREMIUM = "premium"


class QualityCategory(Enum):
    """Quality categories for brands."""
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"


@dataclass
class BrandSegment:
    """Represents a brand segment with various attributes."""
    brand: str
    price_category: PriceCategory
    quality_category: QualityCategory
    avg_rating: float
    price_per_serving: Optional[float]
    protein_content: Optional[int]
    third_party_tested: bool
    artificial_sweeteners: bool
    features: List[str]


class BrandSegmenter:
    """Segments brands by various criteria and attributes."""
    
    def __init__(self):
        """Initialize the brand segmenter."""
        # Price thresholds (in dollars per serving)
        self.price_thresholds = {
            PriceCategory.BUDGET: 0.90,
            PriceCategory.MID_RANGE: 1.20,
            PriceCategory.PREMIUM: float('inf')
        }
        
        # Quality thresholds (based on average rating)
        self.quality_thresholds = {
            QualityCategory.BASIC: 4.0,
            QualityCategory.STANDARD: 4.5,
            QualityCategory.PREMIUM: float('inf')
        }
        
        # Brand-specific data (could be loaded from external source)
        self.brand_data = {
            "Kirkland": {
                "price_per_serving": 0.78,
                "protein_content": 25,
                "third_party_tested": False,
                "artificial_sweeteners": True,
                "features": ["Costco brand", "Good mixability", "Budget friendly"]
            },
            "Isopure": {
                "price_per_serving": 1.30,
                "protein_content": 25,
                "third_party_tested": False,
                "artificial_sweeteners": True,
                "features": ["High protein percentage", "Added vitamins", "Premium quality"]
            },
            "Datiz": {
                "price_per_serving": 1.26,
                "protein_content": 25,
                "third_party_tested": True,
                "artificial_sweeteners": True,
                "features": ["Third party tested", "High protein content", "BCAAs included"]
            },
            "Accent": {
                "price_per_serving": 0.88,
                "protein_content": 25,
                "third_party_tested": True,
                "artificial_sweeteners": False,
                "features": ["Clean ingredients", "No artificial sweeteners", "Athlete tested"]
            },
            "My Protein": {
                "price_per_serving": 0.62,
                "protein_content": 25,
                "third_party_tested": True,
                "artificial_sweeteners": True,
                "features": ["Best value", "High protein percentage", "Third party tested"]
            },
            "Optimum Nutrition": {
                "price_per_serving": 0.88,
                "protein_content": 24,
                "third_party_tested": False,
                "artificial_sweeteners": True,
                "features": ["Widely recognized", "18 flavors", "Good value"]
            }
        }
    
    def segment_brand(self, brand: str, avg_rating: float) -> BrandSegment:
        """
        Segment a brand based on its attributes and rating.
        
        Args:
            brand: Brand name
            avg_rating: Average rating for the brand
            
        Returns:
            BrandSegment object
        """
        brand_info = self.brand_data.get(brand, {})
        
        # Determine price category
        price_per_serving = brand_info.get("price_per_serving")
        price_category = self._categorize_price(price_per_serving)
        
        # Determine quality category
        quality_category = self._categorize_quality(avg_rating)
        
        return BrandSegment(
            brand=brand,
            price_category=price_category,
            quality_category=quality_category,
            avg_rating=avg_rating,
            price_per_serving=price_per_serving,
            protein_content=brand_info.get("protein_content"),
            third_party_tested=brand_info.get("third_party_tested", False),
            artificial_sweeteners=brand_info.get("artificial_sweeteners", False),
            features=brand_info.get("features", [])
        )
    
    def _categorize_price(self, price_per_serving: Optional[float]) -> PriceCategory:
        """
        Categorize brand by price.
        
        Args:
            price_per_serving: Price per serving in dollars
            
        Returns:
            PriceCategory enum value
        """
        if price_per_serving is None:
            return PriceCategory.MID_RANGE
        
        for category, threshold in self.price_thresholds.items():
            if price_per_serving <= threshold:
                return category
        
        return PriceCategory.PREMIUM
    
    def _categorize_quality(self, avg_rating: float) -> QualityCategory:
        """
        Categorize brand by quality based on rating.
        
        Args:
            avg_rating: Average rating (1-5)
            
        Returns:
            QualityCategory enum value
        """
        for category, threshold in self.quality_thresholds.items():
            if avg_rating <= threshold:
                return category
        
        return QualityCategory.PREMIUM
    
    def segment_all_brands(self, brand_ratings: List[Dict[str, Any]]) -> List[BrandSegment]:
        """
        Segment all brands from rating data.
        
        Args:
            brand_ratings: List of brand rating dictionaries
            
        Returns:
            List of BrandSegment objects
        """
        segments = []
        
        for brand_data in brand_ratings:
            brand = brand_data.get("brand")
            avg_rating = brand_data.get("avg_rating", 0.0)
            
            if brand:
                segment = self.segment_brand(brand, avg_rating)
                segments.append(segment)
        
        return segments
    
    def get_brands_by_category(self, segments: List[BrandSegment], 
                             price_category: Optional[PriceCategory] = None,
                             quality_category: Optional[QualityCategory] = None) -> List[BrandSegment]:
        """
        Filter brands by category criteria.
        
        Args:
            segments: List of brand segments
            price_category: Optional price category filter
            quality_category: Optional quality category filter
            
        Returns:
            Filtered list of brand segments
        """
        filtered = segments
        
        if price_category:
            filtered = [s for s in filtered if s.price_category == price_category]
        
        if quality_category:
            filtered = [s for s in filtered if s.quality_category == quality_category]
        
        return filtered
    
    def create_segmentation_summary(self, segments: List[BrandSegment]) -> Dict[str, Any]:
        """
        Create a summary of brand segmentation.
        
        Args:
            segments: List of brand segments
            
        Returns:
            Dictionary with segmentation summary
        """
        summary = {
            "total_brands": len(segments),
            "price_categories": {},
            "quality_categories": {},
            "brands": []
        }
        
        # Count by price category
        for category in PriceCategory:
            count = len([s for s in segments if s.price_category == category])
            summary["price_categories"][category.value] = count
        
        # Count by quality category
        for category in QualityCategory:
            count = len([s for s in segments if s.quality_category == category])
            summary["quality_categories"][category.value] = count
        
        # Brand details
        for segment in segments:
            summary["brands"].append({
                "brand": segment.brand,
                "price_category": segment.price_category.value,
                "quality_category": segment.quality_category.value,
                "avg_rating": segment.avg_rating,
                "price_per_serving": segment.price_per_serving,
                "protein_content": segment.protein_content,
                "third_party_tested": segment.third_party_tested,
                "artificial_sweeteners": segment.artificial_sweeteners,
                "features": segment.features
            })
        
        return summary
    
    def find_best_value_brands(self, segments: List[BrandSegment]) -> List[BrandSegment]:
        """
        Find brands with the best value (high quality, low price).
        
        Args:
            segments: List of brand segments
            
        Returns:
            List of best value brands
        """
        # Filter for high quality brands
        high_quality = [s for s in segments if s.quality_category in [QualityCategory.STANDARD, QualityCategory.PREMIUM]]
        
        # Sort by price (ascending)
        return sorted(high_quality, key=lambda x: x.price_per_serving or float('inf'))
    
    def find_premium_brands(self, segments: List[BrandSegment]) -> List[BrandSegment]:
        """
        Find premium brands (high quality, regardless of price).
        
        Args:
            segments: List of brand segments
            
        Returns:
            List of premium brands
        """
        return [s for s in segments if s.quality_category == QualityCategory.PREMIUM] 