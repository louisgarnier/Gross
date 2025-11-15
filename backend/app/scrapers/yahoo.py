"""
Yahoo Finance scraper for financial ratios using yfinance library.

yfinance is a Python library that provides access to Yahoo Finance data.
It's more reliable than direct web scraping and uses Yahoo Finance's API.

IMPORTANT: This uses yfinance library, which accesses Yahoo Finance data.
- Be respectful: Add delays between requests
- Rate limiting: Don't make too many requests too quickly
- Cache results when possible to avoid repeated requests
"""

from typing import Optional
import yfinance as yf
from app.services.cache import scraper_cache


class YahooScraper:
    """Scraper for Yahoo Finance financial data using yfinance library."""
    
    def __init__(self):
        """Initialize Yahoo scraper."""
        pass
    
    def clean_ticker(self, ticker: str) -> str:
        """Clean and uppercase ticker symbol."""
        return ticker.upper().strip()
    
    def get_interest_coverage(self, ticker: str) -> Optional[float]:
        """
        Get Interest Coverage ratio from Yahoo Finance using ANNUAL data.
        
        Interest Coverage = EBIT / Interest Expense
        Uses most recent fiscal year data (not TTM) for consistency with other sources.
        
        POLICY: All scrapers use Annual data to ensure comparability between sources.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'PLTR')
            
        Returns:
            Interest Coverage ratio (e.g., 5.2 for 5.2x)
            Returns None if not found, error occurs, or company has no debt
        """
        ticker_upper = self.clean_ticker(ticker)
        cache_key = f"yahoo_interest_coverage_{ticker_upper}"
        
        # Check cache first
        cached_value = scraper_cache.get(cache_key)
        if cached_value is not None:
            return cached_value
        
        try:
            # Get stock data using yfinance
            stock = yf.Ticker(ticker_upper)
            
            # Get ANNUAL financials (last fiscal year) for consistency with other sources
            # POLICY: Use Annual data to match Finviz and other sources (not TTM)
            financials = stock.financials
            
            if financials is None or financials.empty:
                return None
            
            # Interest Coverage = Operating Income (Annual) / Interest Expense (Annual)
            # Use most recent fiscal year (first column = most recent)
            
            # Try to get Operating Income (EBIT) - Annual
            operating_income = None
            ebit_labels = ['EBIT', 'Operating Income', 'Operating Profit']
            for label in ebit_labels:
                if label in financials.index:
                    # Get most recent fiscal year (first column)
                    value = financials.loc[label].iloc[0]
                    # Check if value is valid (not NaN, not None)
                    if value is not None:
                        try:
                            value_float = float(value)
                            # Check for NaN: NaN != NaN is True
                            if value_float == value_float:  # Not NaN
                                operating_income = value_float
                                break
                        except (ValueError, TypeError):
                            continue
            
            # Try to get Interest Expense - Annual
            interest_expense = None
            interest_labels = ['Interest Expense', 'Interest Expense Non Operating', 'Interest Paid', 'Total Interest Expense']
            for label in interest_labels:
                if label in financials.index:
                    # Get most recent fiscal year (first column)
                    value = financials.loc[label].iloc[0]
                    # Check if value is valid (not NaN, not None)
                    if value is not None:
                        try:
                            value_float = float(value)
                            # Check for NaN: NaN != NaN is True
                            if value_float == value_float:  # Not NaN
                                interest_expense = value_float
                                break
                        except (ValueError, TypeError):
                            continue
            
            # Calculate Interest Coverage using Annual values
            # If no interest expense (or it's 0), company has no debt - return None
            if operating_income is not None and interest_expense is not None:
                # Interest expense might be negative, use abs
                if abs(interest_expense) > 0:
                    interest_coverage = operating_income / abs(interest_expense)
                    scraper_cache.set(cache_key, interest_coverage)
                    return interest_coverage
            elif operating_income is not None and (interest_expense is None or interest_expense == 0):
                # Company has no interest expense (no debt) - Interest Coverage is N/A
                return None
            
            return None
            
        except Exception as e:
            print(f"Error fetching Interest Coverage from Yahoo Finance for {ticker_upper}: {e}")
            return None
    
    def get_pe_ratio(self, ticker: str) -> Optional[float]:
        """
        Get P/E Ratio from Yahoo Finance.
        
        Uses trailingPE which is based on last 12 months earnings.
        Note: P/E Ratio is typically calculated on TTM earnings by convention,
        but we use trailingPE for consistency with what Yahoo Finance displays.
        
        POLICY: P/E Ratio uses trailingPE (TTM-based) as this is the industry standard.
        Other ratios use Annual data for consistency.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'PLTR')
            
        Returns:
            P/E Ratio as a float (e.g., 406.95)
            Returns None if not found or error occurs
        """
        ticker_upper = self.clean_ticker(ticker)
        cache_key = f"yahoo_pe_{ticker_upper}"
        
        # Check cache first
        cached_value = scraper_cache.get(cache_key)
        if cached_value is not None:
            return cached_value
        
        try:
            # Get stock data using yfinance
            stock = yf.Ticker(ticker_upper)
            
            # Get info which contains P/E ratio
            info = stock.info
            
            if info is None:
                return None
            
            # Try different keys for P/E ratio
            # Use trailingPE first (TTM - Trailing Twelve Months, most commonly displayed)
            # trailingPE is the P/E ratio based on last 12 months earnings (TTM)
            # This matches what Yahoo Finance shows on the summary page
            pe_keys = ['trailingPE', 'forwardPE', 'priceToEarnings', 'peRatio']
            
            for key in pe_keys:
                if key in info and info[key] is not None:
                    pe_value = float(info[key])
                    # Skip if value seems unreasonable (e.g., > 10000 or negative)
                    if 0 < pe_value < 10000:
                        scraper_cache.set(cache_key, pe_value)
                        return pe_value
            
            return None
            
        except Exception as e:
            print(f"Error fetching P/E Ratio from Yahoo Finance for {ticker_upper}: {e}")
            return None
