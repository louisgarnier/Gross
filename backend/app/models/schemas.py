"""
Pydantic models for API request/response schemas.

This defines the "contract" - the exact structure of data that the API will return.
The frontend will use this same structure to know what to expect.
"""

from pydantic import BaseModel
from typing import List, Optional


class SourceValue(BaseModel):
    """Value from a single data source (e.g., Finviz, Morningstar, etc.)."""
    source: str
    value: Optional[float] = None


class RatioResult(BaseModel):
    """Result for a single financial ratio (e.g., Gross Margin, ROIC, etc.)."""
    metric: str
    values: List[SourceValue]  # List of values from different sources
    consensus: Optional[float] = None  # Average or median of all source values
    target: str  # Target threshold (e.g., ">60%", ">10-12%")
    status: str  # "Pass", "Fail", or "Info Only"


class AnalysisResponse(BaseModel):
    """Complete analysis response for a ticker.
    
    This is what the API returns when you call GET /api/analyze/{ticker}
    """
    ticker: str
    ratios: List[RatioResult]  # List of all 5 ratios
    overall_score: int  # Number of ratios that passed (0-4)
    max_score: int  # Maximum possible score (4, since P/E is info only)

