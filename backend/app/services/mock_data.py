"""
Mock data for API responses during development.

This provides fake data so the frontend can be built and tested before we have real scrapers.
Later, we'll replace this with real scraped data.

IMPORTANT: These values are placeholders. Real values will come from actual website scraping.
"""

from app.models.schemas import AnalysisResponse, RatioResult, SourceValue


def get_mock_analysis(ticker: str) -> AnalysisResponse:
    """
    Generate mock analysis data for testing.
    
    This will be replaced with real scrapers later.
    For now, returns sample data for PLTR and NVDA.
    """
    ticker_upper = ticker.upper()
    
    # PLTR (Palantir) - Sample data
    if ticker_upper == "PLTR":
        return AnalysisResponse(
            ticker="PLTR",
            ratios=[
                RatioResult(
                    metric="Gross Margin",
                    values=[
                        SourceValue(source="Finviz", value=80.81),  # Will verify against Finviz
                        SourceValue(source="Morningstar", value=None),  # Will add later
                        SourceValue(source="Macrotrends", value=None)  # Will add later
                    ],
                    consensus=80.81,
                    target=">60%",
                    status="Pass"
                ),
                RatioResult(
                    metric="ROIC",
                    values=[
                        SourceValue(source="QuickFS", value=None),  # Will add later
                        SourceValue(source="Morningstar", value=None),  # Will add later
                        SourceValue(source="Koyfin", value=None)  # Will add later
                    ],
                    consensus=None,
                    target=">10-12%",
                    status="Fail"
                ),
                RatioResult(
                    metric="FCF Margin",
                    values=[
                        SourceValue(source="QuickFS", value=None),  # Will add later
                        SourceValue(source="Koyfin", value=None),  # Will add later
                        SourceValue(source="Macrotrends", value=None)  # Will add later
                    ],
                    consensus=None,
                    target=">20%",
                    status="Fail"
                ),
                RatioResult(
                    metric="Interest Coverage",
                    values=[
                        SourceValue(source="Morningstar", value=None),  # Will add later
                        SourceValue(source="Koyfin", value=None),  # Will add later
                        SourceValue(source="Yahoo Finance", value=None)  # Will add later
                    ],
                    consensus=None,
                    target="≥3-4x",
                    status="Fail"
                ),
                RatioResult(
                    metric="P/E Ratio",
                    values=[
                        SourceValue(source="Finviz", value=406.95),  # Will verify against Finviz
                        SourceValue(source="Yahoo Finance", value=None),  # Will add later
                        SourceValue(source="Morningstar", value=None)  # Will add later
                    ],
                    consensus=406.95,
                    target="Info Only",
                    status="Info Only"
                )
            ],
            overall_score=1,  # Only Gross Margin passes (for now)
            max_score=4
        )
    
    # NVDA (NVIDIA) - Sample data
    elif ticker_upper == "NVDA":
        return AnalysisResponse(
            ticker="NVDA",
            ratios=[
                RatioResult(
                    metric="Gross Margin",
                    values=[
                        SourceValue(source="Finviz", value=None),  # Will add later
                        SourceValue(source="Morningstar", value=None),  # Will add later
                        SourceValue(source="Macrotrends", value=None)  # Will add later
                    ],
                    consensus=None,
                    target=">60%",
                    status="Fail"
                ),
                RatioResult(
                    metric="ROIC",
                    values=[
                        SourceValue(source="QuickFS", value=None),  # Will add later
                        SourceValue(source="Morningstar", value=None),  # Will add later
                        SourceValue(source="Koyfin", value=None)  # Will add later
                    ],
                    consensus=None,
                    target=">10-12%",
                    status="Fail"
                ),
                RatioResult(
                    metric="FCF Margin",
                    values=[
                        SourceValue(source="QuickFS", value=None),  # Will add later
                        SourceValue(source="Koyfin", value=None),  # Will add later
                        SourceValue(source="Macrotrends", value=None)  # Will add later
                    ],
                    consensus=None,
                    target=">20%",
                    status="Fail"
                ),
                RatioResult(
                    metric="Interest Coverage",
                    values=[
                        SourceValue(source="Morningstar", value=None),  # Will add later
                        SourceValue(source="Koyfin", value=None),  # Will add later
                        SourceValue(source="Yahoo Finance", value=None)  # Will add later
                    ],
                    consensus=None,
                    target="≥3-4x",
                    status="Fail"
                ),
                RatioResult(
                    metric="P/E Ratio",
                    values=[
                        SourceValue(source="Finviz", value=None),  # Will add later
                        SourceValue(source="Yahoo Finance", value=None),  # Will add later
                        SourceValue(source="Morningstar", value=None)  # Will add later
                    ],
                    consensus=None,
                    target="Info Only",
                    status="Info Only"
                )
            ],
            overall_score=0,
            max_score=4
        )
    
    # Default for any other ticker (e.g., MSFT, AAPL, etc.)
    # Returns sample data structure - values will be replaced by real scrapers later
    else:
        return AnalysisResponse(
            ticker=ticker_upper,
            ratios=[
                RatioResult(
                    metric="Gross Margin",
                    values=[
                        SourceValue(source="Finviz", value=None),  # Will be filled by scraper
                        SourceValue(source="Morningstar", value=None),  # Will be filled by scraper
                        SourceValue(source="Macrotrends", value=None)  # Will be filled by scraper
                    ],
                    consensus=None,
                    target=">60%",
                    status="Fail"  # Will be calculated by validator
                ),
                RatioResult(
                    metric="ROIC",
                    values=[
                        SourceValue(source="QuickFS", value=None),  # Will be filled by scraper
                        SourceValue(source="Morningstar", value=None),  # Will be filled by scraper
                        SourceValue(source="Koyfin", value=None)  # Will be filled by scraper
                    ],
                    consensus=None,
                    target=">10-12%",
                    status="Fail"  # Will be calculated by validator
                ),
                RatioResult(
                    metric="FCF Margin",
                    values=[
                        SourceValue(source="QuickFS", value=None),  # Will be filled by scraper
                        SourceValue(source="Koyfin", value=None),  # Will be filled by scraper
                        SourceValue(source="Macrotrends", value=None)  # Will be filled by scraper
                    ],
                    consensus=None,
                    target=">20%",
                    status="Fail"  # Will be calculated by validator
                ),
                RatioResult(
                    metric="Interest Coverage",
                    values=[
                        SourceValue(source="Morningstar", value=None),  # Will be filled by scraper
                        SourceValue(source="Koyfin", value=None),  # Will be filled by scraper
                        SourceValue(source="Yahoo Finance", value=None)  # Will be filled by scraper
                    ],
                    consensus=None,
                    target="≥3-4x",
                    status="Fail"  # Will be calculated by validator
                ),
                RatioResult(
                    metric="P/E Ratio",
                    values=[
                        SourceValue(source="Finviz", value=None),  # Will be filled by scraper
                        SourceValue(source="Yahoo Finance", value=None),  # Will be filled by scraper
                        SourceValue(source="Morningstar", value=None)  # Will be filled by scraper
                    ],
                    consensus=None,
                    target="Info Only",
                    status="Info Only"
                )
            ],
            overall_score=0,
            max_score=4
        )

