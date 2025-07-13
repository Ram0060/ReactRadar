#!/usr/bin/env python3
"""
Test client for ReactRadar FastAPI endpoints.
Demonstrates how to use all API endpoints.
"""

import requests
import json
import time
from typing import Dict, Any, List, Optional


class ReactRadarClient:
    """Client for interacting with ReactRadar API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health."""
        response = self.session.get(f"{self.base_url}/health")
        return response.json()
    
    def analyze_transcript(self, transcript: str, save_results: bool = True) -> Dict[str, Any]:
        """Analyze a transcript."""
        data = {
            "transcript": transcript,
            "save_results": save_results
        }
        response = self.session.post(f"{self.base_url}/analyze", json=data)
        return response.json()
    
    def analyze_single_brand(self, brand_name: str, transcript: Optional[str] = None) -> Dict[str, Any]:
        """Analyze a single brand."""
        params = {}
        if transcript:
            params["transcript"] = transcript
        
        response = self.session.get(f"{self.base_url}/brand/{brand_name}", params=params)
        return response.json()
    
    def compare_brands(self, brands: List[str], transcript: Optional[str] = None) -> Dict[str, Any]:
        """Compare multiple brands."""
        data = {
            "brands": brands
        }
        if transcript:
            data["transcript"] = transcript
        
        response = self.session.post(f"{self.base_url}/compare", json=data)
        return response.json()
    
    def extract_brands(self, transcript: str, known_brands: Optional[List[str]] = None) -> Dict[str, Any]:
        """Extract brands from text."""
        data = {
            "transcript": transcript
        }
        if known_brands:
            data["known_brands"] = known_brands
        
        response = self.session.post(f"{self.base_url}/extract-brands", json=data)
        return response.json()
    
    def analyze_sentiment(self, brand: str, statements: list) -> Dict[str, Any]:
        """Analyze sentiment for statements."""
        data = {
            "brand": brand,
            "statements": statements
        }
        response = self.session.post(f"{self.base_url}/sentiment", json=data)
        return response.json()
    
    def get_segments(self) -> Dict[str, Any]:
        """Get brand segments."""
        response = self.session.get(f"{self.base_url}/segments")
        return response.json()
    
    def get_insights(self) -> Dict[str, Any]:
        """Get brand insights."""
        response = self.session.get(f"{self.base_url}/insights")
        return response.json()
    
    def get_files(self) -> Dict[str, Any]:
        """List available files."""
        response = self.session.get(f"{self.base_url}/files")
        return response.json()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get analysis statistics."""
        response = self.session.get(f"{self.base_url}/stats")
        return response.json()


def demo_api_usage():
    """Demonstrate API usage with examples."""
    print("🚀 ReactRadar API Client Demo")
    print("=" * 50)
    
    # Initialize client
    client = ReactRadarClient()
    
    try:
        # 1. Health check
        print("\n1. Health Check:")
        health = client.health_check()
        print(f"   Status: {health.get('status', 'unknown')}")
        print(f"   Available files: {len(health.get('available_files', []))}")
        
        # 2. Extract brands from custom transcript
        print("\n2. Brand Extraction:")
        custom_transcript = """
        I've been testing various protein powders and here are my findings. 
        Optimum Nutrition Gold Standard is excellent with great taste and mixability. 
        My Protein Impact Whey offers the best value for money at only 62 cents per serving. 
        Isopure is premium quality but quite expensive at $1.30 per serving.
        """
        
        extraction = client.extract_brands(custom_transcript)
        if extraction.get('success'):
            brands = extraction['data']['brands']
            print(f"   Extracted brands: {', '.join(brands)}")
        
        # 3. Analyze transcript
        print("\n3. Full Transcript Analysis:")
        analysis = client.analyze_transcript(custom_transcript, save_results=False)
        if analysis.get('success'):
            data = analysis['data']
            print(f"   Found {len(data['brands'])} brands")
            print(f"   Average rating: {data['summary']['average_rating']}")
            
            # Show insights for first brand
            if data['brand_insights']:
                insight = data['brand_insights'][0]
                print(f"   Sample insight for {insight['brand']}: {insight['summary'][:100]}...")
        
        # 4. Single brand analysis
        print("\n4. Single Brand Analysis:")
        if brands:
            brand_analysis = client.analyze_single_brand(brands[0])
            if brand_analysis.get('success'):
                data = brand_analysis['data']
                print(f"   {brands[0]} rating: {data['sentiment_analysis']['avg_rating']:.2f} stars")
                print(f"   Price category: {data['segmentation']['price_category']}")
        
        # 5. Brand comparison
        print("\n5. Brand Comparison:")
        if len(brands) >= 2:
            comparison = client.compare_brands(brands[:2])
            if comparison.get('success'):
                data = comparison['data']
                print(f"   Comparing {len(data['comparison_data'])} brands:")
                for brand_data in data['comparison_data']:
                    brand = brand_data['brand']
                    rating = brand_data['sentiment_analysis']['avg_rating']
                    price_cat = brand_data['segmentation']['price_category']
                    print(f"     • {brand}: {rating:.2f} stars ({price_cat})")
        
        # 6. Sentiment analysis
        print("\n6. Sentiment Analysis:")
        statements = [
            "My Protein offers great value for money",
            "The taste is excellent and it mixes well",
            "It's the best protein powder I've tried"
        ]
        sentiment = client.analyze_sentiment("My Protein", statements)
        if sentiment.get('success'):
            data = sentiment['data']
            print(f"   Sentiment score: {data['sentiment']['avg_score']:.3f}")
            print(f"   Rating: {data['sentiment']['avg_rating']:.2f} stars")
        
        # 7. Get segments
        print("\n7. Brand Segments:")
        segments = client.get_segments()
        if segments.get('success'):
            data = segments['data']
            print(f"   Retrieved {len(data['segments'])} segments")
            if data['segments']:
                segment = data['segments'][0]
                print(f"   Sample: {segment['brand']} - {segment['price_category']} ({segment['quality_category']})")
        
        # 8. Get insights
        print("\n8. Brand Insights:")
        insights = client.get_insights()
        if insights.get('success'):
            data = insights['data']
            print(f"   Retrieved {len(data['insights'])} insights")
        
        # 9. Get statistics
        print("\n9. System Statistics:")
        stats = client.get_stats()
        if stats.get('success'):
            data = stats['data']
            print(f"   Total brands: {data['total_brands']}")
            print(f"   Average rating: {data['average_rating']}")
            print(f"   Available files: {len(data['available_files'])}")
        
        print("\n✅ API demo completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the server is running on http://localhost:8000")
        print("   Start the server with: python api/main.py")
    except Exception as e:
        print(f"❌ Error during API demo: {e}")


def test_specific_endpoints():
    """Test specific endpoints with detailed output."""
    print("\n🔧 Detailed Endpoint Testing")
    print("=" * 50)
    
    client = ReactRadarClient()
    
    # Test cases
    test_cases = [
        {
            "name": "Health Check",
            "method": client.health_check,
            "args": []
        },
        {
            "name": "File Listing",
            "method": client.get_files,
            "args": []
        },
        {
            "name": "Statistics",
            "method": client.get_stats,
            "args": []
        }
    ]
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        try:
            result = test_case['method'](*test_case['args'])
            if result.get('success'):
                print(f"  ✅ Success: {result.get('message', '')}")
            else:
                print(f"  ❌ Failed: {result.get('message', '')}")
        except Exception as e:
            print(f"  ❌ Error: {e}")


if __name__ == "__main__":
    # Run demo
    demo_api_usage()
    
    # Run detailed tests
    test_specific_endpoints() 