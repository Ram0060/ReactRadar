"""
FastAPI application for ReactRadar brand analysis system.
Provides REST API endpoints for all analysis functionality.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import uvicorn
import json
import sys
import os

# Add parent directory to path to import src modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analysis_engine import ReactRadarEngine, AnalysisResult
from src.data_loader import DataLoader
from src.brand_extractor import BrandExtractor
from src.sentiment_analyzer import SentimentAnalyzer
from src.brand_segmenter import BrandSegmenter
from src.insight_generator import InsightGenerator


# Pydantic models for request/response
class TranscriptRequest(BaseModel):
    transcript: str = Field(..., description="Text transcript to analyze")
    save_results: bool = Field(default=True, description="Whether to save results to files")

class BrandAnalysisRequest(BaseModel):
    brand: str = Field(..., description="Brand name to analyze")
    transcript: Optional[str] = Field(None, description="Optional transcript text")

class BrandComparisonRequest(BaseModel):
    brands: List[str] = Field(..., description="List of brand names to compare")
    transcript: Optional[str] = Field(None, description="Optional transcript text")

class CustomAnalysisRequest(BaseModel):
    transcript: str = Field(..., description="Text transcript to analyze")
    known_brands: Optional[List[str]] = Field(None, description="Known brand names to look for")

class AnalysisResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

# Initialize FastAPI app
app = FastAPI(
    title="ReactRadar API",
    description="Brand analysis API for sentiment analysis, segmentation, and insights",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the analysis engine
engine = ReactRadarEngine(data_dir="experiment")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "ReactRadar Brand Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "analyze": "/analyze",
            "brand": "/brand/{brand_name}",
            "compare": "/compare",
            "extract_brands": "/extract-brands",
            "sentiment": "/sentiment",
            "segments": "/segments",
            "insights": "/insights",
            "files": "/files"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Test if we can load data
        data_loader = DataLoader()
        available_files = data_loader.list_available_files()
        return {
            "status": "healthy",
            "available_files": available_files,
            "engine_ready": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_transcript(request: TranscriptRequest):
    """
    Analyze a transcript and extract brand insights.
    
    This endpoint performs the complete analysis pipeline:
    - Brand extraction
    - Sentiment analysis
    - Brand segmentation
    - Insight generation
    """
    try:
        # Run full analysis
        result = engine.run_full_analysis(request.transcript)
        
        # Save results if requested
        if request.save_results:
            engine.save_analysis_results(result)
        
        # Prepare response data
        response_data = {
            "brands": result.brands,
            "summary": result.summary,
            "comparative_insights": result.comparative_insights,
            "brand_insights": [
                {
                    "brand": insight.brand,
                    "summary": insight.summary,
                    "strengths": insight.strengths,
                    "weaknesses": insight.weaknesses,
                    "recommendations": insight.recommendations,
                    "target_audience": insight.target_audience
                }
                for insight in result.brand_insights
            ]
        }
        
        return AnalysisResponse(
            success=True,
            message=f"Analysis complete. Found {len(result.brands)} brands.",
            data=response_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/brand/{brand_name}")
async def analyze_single_brand(brand_name: str, transcript: Optional[str] = None):
    """
    Analyze a single brand in detail.
    
    Args:
        brand_name: Name of the brand to analyze
        transcript: Optional transcript text (uses saved data if not provided)
    """
    try:
        brand_analysis = engine.analyze_single_brand(brand_name, transcript)
        
        if "error" in brand_analysis:
            raise HTTPException(status_code=404, detail=brand_analysis["error"])
        
        return AnalysisResponse(
            success=True,
            message=f"Analysis complete for {brand_name}",
            data=brand_analysis
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Brand analysis failed: {str(e)}")


@app.post("/compare", response_model=AnalysisResponse)
async def compare_brands(request: BrandComparisonRequest):
    """
    Compare multiple brands side by side.
    
    Args:
        brands: List of brand names to compare
        transcript: Optional transcript text
    """
    try:
        comparison = engine.compare_brands(request.brands, request.transcript)
        
        return AnalysisResponse(
            success=True,
            message=f"Comparison complete for {len(request.brands)} brands",
            data=comparison
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Brand comparison failed: {str(e)}")


@app.post("/extract-brands")
async def extract_brands(transcript: str, known_brands: Optional[List[str]] = None):
    """
    Extract brand names from text.
    
    Args:
        transcript: Text to extract brands from
        known_brands: Optional list of known brand names
    """
    try:
        extractor = BrandExtractor(known_brands)
        brands = extractor.get_unique_brands(transcript)
        
        # Get brand matches with context
        matches = extractor.extract_brands_from_text(transcript)
        
        return AnalysisResponse(
            success=True,
            message=f"Extracted {len(brands)} brands",
            data={
                "brands": brands,
                "matches": [
                    {
                        "brand": match.brand_name,
                        "start_pos": match.start_pos,
                        "end_pos": match.end_pos,
                        "context": match.context
                    }
                    for match in matches
                ]
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Brand extraction failed: {str(e)}")


@app.post("/sentiment")
async def analyze_sentiment(brand: str, statements: List[str]):
    """
    Analyze sentiment for specific statements about a brand.
    
    Args:
        brand: Brand name
        statements: List of statements to analyze
    """
    try:
        analyzer = SentimentAnalyzer()
        sentiment = analyzer.analyze_brand_statements(brand, statements)
        rating_summary = analyzer.create_rating_summary(sentiment)
        
        return AnalysisResponse(
            success=True,
            message=f"Sentiment analysis complete for {brand}",
            data={
                "brand": brand,
                "sentiment": {
                    "avg_rating": sentiment.avg_rating,
                    "avg_score": sentiment.avg_score,
                    "positive_count": sentiment.positive_count,
                    "negative_count": sentiment.negative_count,
                    "neutral_count": sentiment.neutral_count
                },
                "rating_summary": rating_summary
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {str(e)}")


@app.get("/segments")
async def get_brand_segments():
    """Get all brand segments from saved data."""
    try:
        data_loader = DataLoader()
        brand_ratings = data_loader.load_brand_ratings()
        
        segmenter = BrandSegmenter()
        segments = segmenter.segment_all_brands(brand_ratings)
        
        segment_data = []
        for segment in segments:
            segment_data.append({
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
        
        return AnalysisResponse(
            success=True,
            message=f"Retrieved {len(segments)} brand segments",
            data={"segments": segment_data}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get segments: {str(e)}")


@app.get("/insights")
async def get_brand_insights():
    """Get all brand insights from saved data."""
    try:
        data_loader = DataLoader()
        insights = data_loader.load_brand_insights()
        
        return AnalysisResponse(
            success=True,
            message=f"Retrieved {len(insights)} brand insights",
            data={"insights": insights}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get insights: {str(e)}")


@app.get("/files")
async def list_available_files():
    """List all available data files."""
    try:
        data_loader = DataLoader()
        files = data_loader.list_available_files()
        
        return AnalysisResponse(
            success=True,
            message=f"Found {len(files)} data files",
            data={"files": files}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")


@app.post("/upload-transcript")
async def upload_transcript(file: UploadFile = File(...)):
    """
    Upload a transcript file and analyze it.
    
    Supports JSON files with transcript data.
    """
    try:
        if not file.filename.endswith('.json'):
            raise HTTPException(status_code=400, detail="Only JSON files are supported")
        
        # Read file content
        content = await file.read()
        data = json.loads(content.decode('utf-8'))
        
        # Extract transcript
        transcript = data.get('transcript', '')
        if not transcript:
            raise HTTPException(status_code=400, detail="No transcript found in file")
        
        # Run analysis
        result = engine.run_full_analysis(transcript)
        
        return AnalysisResponse(
            success=True,
            message=f"File uploaded and analyzed. Found {len(result.brands)} brands.",
            data={
                "filename": file.filename,
                "brands": result.brands,
                "summary": result.summary
            }
        )
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")


@app.get("/stats")
async def get_analysis_stats():
    """Get overall statistics about the analysis system."""
    try:
        data_loader = DataLoader()
        
        # Load various data files
        brands = data_loader.load_extracted_brands()
        ratings = data_loader.load_brand_ratings()
        sentiments = data_loader.load_brand_sentiment()
        segments = data_loader.load_brand_segmented()
        insights = data_loader.load_brand_insights()
        
        # Calculate statistics
        avg_rating = sum(r.get('avg_rating', 0) for r in ratings) / len(ratings) if ratings else 0
        
        stats = {
            "total_brands": len(brands),
            "total_ratings": len(ratings),
            "total_sentiments": len(sentiments),
            "total_segments": len(segments),
            "total_insights": len(insights),
            "average_rating": round(avg_rating, 2),
            "available_files": data_loader.list_available_files()
        }
        
        return AnalysisResponse(
            success=True,
            message="Statistics retrieved successfully",
            data=stats
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 