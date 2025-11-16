"""
Service for fetching financial ratios from multiple sources.

This service coordinates all scrapers and aggregates the data.
"""

from typing import List, Optional
from app.models.schemas import AnalysisResponse, RatioResult, SourceValue
from app.scrapers.finviz import FinvizScraper
from app.scrapers.yahoo import YahooScraper


def calculate_consensus(values: List[SourceValue]) -> Optional[float]:
    """
    Calculate consensus (average) from non-null values.
    
    Args:
        values: List of SourceValue objects
        
    Returns:
        Average of non-null values, or None if no values
    """
    valid_values = [v.value for v in values if v.value is not None]
    if not valid_values:
        return None
    return sum(valid_values) / len(valid_values)


def calculate_spread(values: List[SourceValue]) -> Optional[float]:
    """
    Calculate spread (max - min) between sources to detect inconsistencies.
    
    This helps identify when sources disagree significantly.
    
    Args:
        values: List of SourceValue objects
        
    Returns:
        Spread (max - min) of non-null values, or None if less than 2 values
    """
    valid_values = [v.value for v in values if v.value is not None]
    if len(valid_values) < 2:
        return None
    return max(valid_values) - min(valid_values)


def evaluate_status(metric: str, consensus: Optional[float], target: str) -> str:
    """
    Evaluate if a metric passes, fails, or is info only.
    
    Args:
        metric: Metric name
        consensus: Consensus value (average of sources)
        target: Target threshold string (e.g., ">60%", ">10-12%")
        
    Returns:
        "Pass", "Fail", or "Info Only"
    """
    # P/E Ratio is always "Info Only"
    if metric == "P/E Ratio":
        return "Info Only"
    
    if consensus is None:
        return "Fail"
    
    # Parse target string
    # Examples: ">60%", ">10-12%", "≥3-4x", ">20%"
    target_lower = target.lower()
    
    # Extract minimum threshold
    import re
    # Find number in target (e.g., ">60%" -> 60, ">10-12%" -> 10)
    numbers = re.findall(r'\d+\.?\d*', target)
    if not numbers:
        return "Fail"
    
    min_threshold = float(numbers[0])
    
    # Check if consensus meets threshold
    if consensus >= min_threshold:
        return "Pass"
    else:
        return "Fail"


def fetch_analysis(ticker: str) -> AnalysisResponse:
    """
    Fetch financial analysis for a ticker from all available sources.
    
    This is the main function that coordinates all scrapers.
    Currently implements Finviz for Gross Margin.
    More scrapers will be added incrementally.
    
    Args:
        ticker: Stock ticker symbol (e.g., "PLTR", "NVDA")
        
    Returns:
        AnalysisResponse with all ratios and their status
    """
    ticker_upper = ticker.upper().strip()
    
    # Initialize scrapers
    finviz = FinvizScraper()
    yahoo = YahooScraper()
    
    # Fetch Gross Margin from Finviz
    finviz_gross_margin = finviz.get_gross_margin(ticker_upper)
    
    # Build Gross Margin ratio
    gross_margin_values = [
        SourceValue(source="Finviz", value=finviz_gross_margin),
        SourceValue(source="Morningstar", value=None),  # TODO: Add Morningstar scraper
        SourceValue(source="Macrotrends", value=None)  # TODO: Add Macrotrends scraper
    ]
    gross_margin_consensus = calculate_consensus(gross_margin_values)
    gross_margin_spread = calculate_spread(gross_margin_values)
    gross_margin_status = evaluate_status("Gross Margin", gross_margin_consensus, ">60%")
    
    # Build ROIC ratio (no scrapers yet)
    roic_values = [
        SourceValue(source="QuickFS", value=None),  # TODO: Add QuickFS scraper
        SourceValue(source="Morningstar", value=None),  # TODO: Add Morningstar scraper
        SourceValue(source="Koyfin", value=None)  # TODO: Add Koyfin scraper
    ]
    roic_consensus = calculate_consensus(roic_values)
    roic_spread = calculate_spread(roic_values)
    roic_status = evaluate_status("ROIC", roic_consensus, ">10-12%")
    
    # Build FCF Margin ratio (no scrapers yet)
    fcf_margin_values = [
        SourceValue(source="QuickFS", value=None),  # TODO: Add QuickFS scraper
        SourceValue(source="Koyfin", value=None),  # TODO: Add Koyfin scraper
        SourceValue(source="Macrotrends", value=None)  # TODO: Add Macrotrends scraper
    ]
    fcf_margin_consensus = calculate_consensus(fcf_margin_values)
    fcf_margin_spread = calculate_spread(fcf_margin_values)
    fcf_margin_status = evaluate_status("FCF Margin", fcf_margin_consensus, ">20%")
    
    # Build Interest Coverage ratio
    yahoo_interest_coverage = yahoo.get_interest_coverage(ticker_upper)
    interest_coverage_values = [
        SourceValue(source="Morningstar", value=None),  # TODO: Add Morningstar scraper
        SourceValue(source="Koyfin", value=None),  # TODO: Add Koyfin scraper
        SourceValue(source="Yahoo Finance", value=yahoo_interest_coverage)
    ]
    interest_coverage_consensus = calculate_consensus(interest_coverage_values)
    interest_coverage_spread = calculate_spread(interest_coverage_values)
    interest_coverage_status = evaluate_status("Interest Coverage", interest_coverage_consensus, "≥3-4x")
    
    # Fetch P/E Ratio from Finviz and Yahoo Finance
    finviz_pe = finviz.get_pe_ratio(ticker_upper)
    yahoo_pe = yahoo.get_pe_ratio(ticker_upper)
    
    # Build P/E Ratio
    pe_values = [
        SourceValue(source="Finviz", value=finviz_pe),
        SourceValue(source="Yahoo Finance", value=yahoo_pe),
        SourceValue(source="Morningstar", value=None)  # TODO: Add Morningstar scraper
    ]
    pe_consensus = calculate_consensus(pe_values)
    pe_spread = calculate_spread(pe_values)
    pe_status = evaluate_status("P/E Ratio", pe_consensus, "Info Only")
    
    # Build ratios list
    ratios = [
        RatioResult(
            metric="Gross Margin",
            values=gross_margin_values,
            consensus=gross_margin_consensus,
            spread=gross_margin_spread,
            target=">60%",
            status=gross_margin_status
        ),
        RatioResult(
            metric="ROIC",
            values=roic_values,
            consensus=roic_consensus,
            spread=roic_spread,
            target=">10-12%",
            status=roic_status
        ),
        RatioResult(
            metric="FCF Margin",
            values=fcf_margin_values,
            consensus=fcf_margin_consensus,
            spread=fcf_margin_spread,
            target=">20%",
            status=fcf_margin_status
        ),
        RatioResult(
            metric="Interest Coverage",
            values=interest_coverage_values,
            consensus=interest_coverage_consensus,
            spread=interest_coverage_spread,
            target="≥3-4x",
            status=interest_coverage_status
        ),
        RatioResult(
            metric="P/E Ratio",
            values=pe_values,
            consensus=pe_consensus,
            spread=pe_spread,
            target="Info Only",
            status=pe_status
        )
    ]
    
    # Calculate overall score (count Pass statuses, excluding P/E)
    overall_score = sum(1 for r in ratios if r.status == "Pass" and r.metric != "P/E Ratio")
    max_score = 4  # 4 metrics that can pass (P/E is info only)
    
    return AnalysisResponse(
        ticker=ticker_upper,
        ratios=ratios,
        overall_score=overall_score,
        max_score=max_score
    )

