#!/usr/bin/env python3
"""
Simple example demonstrating ReactRadar API usage.
"""

import requests
import json


def test_api():
    """Test the ReactRadar API with a simple example."""
    base_url = "http://localhost:8000"
    
    print("🚀 ReactRadar API Example")
    print("=" * 40)
    
    # Test data
    transcript = """
    I've been testing various protein powders and here are my findings. 
    Optimum Nutrition Gold Standard is excellent with great taste and mixability. 
    My Protein Impact Whey offers the best value for money at only 62 cents per serving. 
    Isopure is premium quality but quite expensive at $1.30 per serving. 
    Kirkland Signature is a solid budget option with decent protein content.
    """
    
    try:
        # 1. Health check
        print("1. Checking API health...")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health = response.json()
            print(f"   ✅ API is healthy. Available files: {len(health.get('available_files', []))}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return
        
        # 2. Extract brands
        print("\n2. Extracting brands...")
        response = requests.post(f"{base_url}/extract-brands", json={
            "transcript": transcript
        })
        if response.status_code == 200:
            result = response.json()
            brands = result['data']['brands']
            print(f"   ✅ Found brands: {', '.join(brands)}")
        else:
            print(f"   ❌ Brand extraction failed: {response.status_code}")
            return
        
        # 3. Analyze transcript
        print("\n3. Analyzing transcript...")
        response = requests.post(f"{base_url}/analyze", json={
            "transcript": transcript,
            "save_results": False
        })
        if response.status_code == 200:
            result = response.json()
            data = result['data']
            print(f"   ✅ Analysis complete!")
            print(f"   📊 Found {len(data['brands'])} brands")
            print(f"   📈 Average rating: {data['summary']['average_rating']}")
            
            # Show insights for first brand
            if data['brand_insights']:
                insight = data['brand_insights'][0]
                print(f"   💡 Sample insight: {insight['brand']} - {insight['summary'][:80]}...")
        else:
            print(f"   ❌ Analysis failed: {response.status_code}")
        
        # 4. Get statistics
        print("\n4. Getting system statistics...")
        response = requests.get(f"{base_url}/stats")
        if response.status_code == 200:
            result = response.json()
            stats = result['data']
            print(f"   ✅ System stats:")
            print(f"      • Total brands: {stats['total_brands']}")
            print(f"      • Average rating: {stats['average_rating']}")
            print(f"      • Available files: {len(stats['available_files'])}")
        else:
            print(f"   ❌ Stats failed: {response.status_code}")
        
        print("\n🎉 API example completed successfully!")
        print(f"📚 View full API documentation at: {base_url}/docs")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API server.")
        print("   Make sure the server is running with: python api/start_server.py")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    test_api() 