"""
Finviz scraper for financial ratios.

Finviz URL format: https://finviz.com/quote.ashx?t={TICKER}

IMPORTANT: This is web scraping, not an official API.
- Be respectful: Add delays between requests
- Rate limiting: Don't make too many requests too quickly
- Cache results when possible to avoid repeated requests
"""

from typing import Optional
from bs4 import BeautifulSoup
from .base import BaseScraper
from app.services.cache import scraper_cache


class FinvizScraper(BaseScraper):
    """Scraper for Finviz financial data."""
    
    BASE_URL = "https://finviz.com/quote.ashx"
    
    def _get_quote_page(self, ticker: str) -> Optional[BeautifulSoup]:
        """Fetch the quote page for a ticker."""
        ticker = self.clean_ticker(ticker)
        url = f"{self.BASE_URL}?t={ticker}"
        return self.fetch_page(url)
    
    def _find_metric_value(self, soup: BeautifulSoup, metric_label: str) -> Optional[float]:
        """
        Find a metric value in the Finviz quote page.
        
        Finviz displays metrics in a table. We search for the label text
        and then get the value from the adjacent cell.
        """
        if not soup:
            return None
        
        # Find all table cells
        cells = soup.find_all('td', class_='snapshot-td2')
        
        # Look for the metric label
        for i, cell in enumerate(cells):
            text = cell.get_text(strip=True)
            if metric_label.lower() in text.lower():
                # The value is typically in the next cell or in the same cell after the label
                # Try next sibling or next cell
                next_cell = cell.find_next_sibling('td')
                if not next_cell:
                    # Sometimes the value is in the same cell after a space or separator
                    # Extract number from the cell text
                    value_text = cell.get_text(strip=True)
                    # Remove the label part and get the value
                    value_text = value_text.replace(metric_label, '').strip()
                    return self.extract_number(value_text)
                else:
                    value_text = next_cell.get_text(strip=True)
                    return self.extract_number(value_text)
        
        # Alternative: search in all text and find pattern
        # Gross Margin might be displayed as "Gross Margin 80.81%"
        page_text = soup.get_text()
        import re
        # Pattern: "Gross Margin" followed by a number and %
        pattern = rf'{re.escape(metric_label)}[:\s]+([\d.]+)%'
        match = re.search(pattern, page_text, re.IGNORECASE)
        if match:
            return float(match.group(1))
        
        return None
    
    def get_gross_margin(self, ticker: str) -> Optional[float]:
        """
        Get Gross Margin percentage from Finviz.
        
        Uses caching to avoid repeated requests to the same ticker.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'PLTR')
            
        Returns:
            Gross Margin as a percentage (e.g., 80.81 for 80.81%)
            Returns None if not found or error occurs
        """
        ticker_upper = self.clean_ticker(ticker)
        cache_key = f"finviz_gross_margin_{ticker_upper}"
        
        # Check cache first
        cached_value = scraper_cache.get(cache_key)
        if cached_value is not None:
            return cached_value
        
        # Fetch from website
        soup = self._get_quote_page(ticker_upper)
        if not soup:
            return None
        
        # Try different label variations
        value = self._find_metric_value(soup, "Gross Margin")
        if value is not None:
            scraper_cache.set(cache_key, value)  # Cache the result
            return value
        
        # Try alternative labels
        value = self._find_metric_value(soup, "Gross M.")
        if value is not None:
            scraper_cache.set(cache_key, value)  # Cache the result
            return value
        
        return None
    
    def get_pe_ratio(self, ticker: str) -> Optional[float]:
        """
        Get P/E Ratio from Finviz.
        
        Uses caching to avoid repeated requests to the same ticker.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'PLTR')
            
        Returns:
            P/E Ratio as a float (e.g., 406.95)
            Returns None if not found or error occurs
        """
        ticker_upper = self.clean_ticker(ticker)
        cache_key = f"finviz_pe_{ticker_upper}"
        
        # Check cache first
        cached_value = scraper_cache.get(cache_key)
        if cached_value is not None:
            return cached_value
        
        # Fetch from website
        soup = self._get_quote_page(ticker_upper)
        if not soup:
            return None
        
        # Try different label variations
        value = self._find_metric_value(soup, "P/E")
        if value is not None:
            scraper_cache.set(cache_key, value)  # Cache the result
            return value
        
        value = self._find_metric_value(soup, "Trailing P/E")
        if value is not None:
            scraper_cache.set(cache_key, value)  # Cache the result
            return value
        
        return None

