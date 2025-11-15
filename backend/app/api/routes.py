"""
API routes for the financial analysis application.

This defines the endpoints that the frontend will call.
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import AnalysisResponse
from app.services.ratio_fetcher import fetch_analysis

router = APIRouter()


@router.get("/analyze/{ticker}", response_model=AnalysisResponse)
async def analyze_ticker(ticker: str):
    """
    Analyze a stock ticker and return financial ratios from multiple sources.
    
    This now uses real scrapers (Finviz for Gross Margin and P/E Ratio).
    Other sources will be added incrementally.
    
    Args:
        ticker: Stock ticker symbol (e.g., PLTR, NVDA, AAPL)
    
    Returns:
        AnalysisResponse with ratios, consensus values, and pass/fail status
    """
    if not ticker or len(ticker) > 10:
        raise HTTPException(status_code=400, detail="Invalid ticker symbol")
    
    try:
        analysis = fetch_analysis(ticker)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing ticker: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint to verify the API is running."""
    return {"status": "healthy", "service": "gross-backend"}

