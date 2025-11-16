"""
QuickFS scraper for financial ratios.

QuickFS URL format: https://quickfs.net/company/{TICKER}

IMPORTANT: This is web scraping, not an official API.
- Be respectful: Add delays between requests
- Rate limiting: Don't make too many requests too quickly
- Cache results when possible to avoid repeated requests
"""

from typing import Optional
from bs4 import BeautifulSoup
from .base import BaseScraper
from app.services.cache import scraper_cache


class QuickFSScraper(BaseScraper):
    """Scraper for QuickFS financial data."""
    
    BASE_URL = "https://quickfs.net/company"
    
    def _get_company_page(self, ticker: str) -> Optional[BeautifulSoup]:
        """Fetch the company page for a ticker."""
        ticker = self.clean_ticker(ticker)
        url = f"{self.BASE_URL}/{ticker}"
        return self.fetch_page(url)
    
    def _find_metric_value(self, soup: BeautifulSoup, metric_label: str) -> Optional[float]:
        """
        Find a metric value in the QuickFS company page.
        
        QuickFS displays metrics in various formats (tables, cards, etc.).
        We search for the label text and extract the value.
        """
        if not soup:
            return None
        
        # Strategy 1: Look for the metric in tables
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                for i, cell in enumerate(cells):
                    text = cell.get_text(strip=True)
                    if metric_label.lower() in text.lower():
                        # Try to get value from adjacent cell
                        if i + 1 < len(cells):
                            value_text = cells[i + 1].get_text(strip=True)
                            value = self.extract_number(value_text)
                            if value is not None:
                                return value
        
        # Strategy 2: Look for metric in divs/cards
        # QuickFS might display metrics in card format
        all_divs = soup.find_all('div')
        for div in all_divs:
            div_text = div.get_text(strip=True)
            if metric_label.lower() in div_text.lower():
                # Try to extract number from this div or its children
                value = self.extract_number(div_text)
                if value is not None:
                    return value
        
        # Strategy 3: Search in page text with regex
        page_text = soup.get_text()
        import re
        # Pattern: "ROIC" or "Return on Invested Capital" followed by number
        pattern = rf'{re.escape(metric_label)}[:\s]+([\d.]+)%?'
        match = re.search(pattern, page_text, re.IGNORECASE)
        if match:
            return float(match.group(1))
        
        return None
    
    def get_roic(self, ticker: str) -> Optional[float]:
        """
        Get ROIC (Return on Invested Capital) percentage from QuickFS.
        
        Uses caching to avoid repeated requests to the same ticker.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'PLTR')
            
        Returns:
            ROIC as a percentage (e.g., 15.5 for 15.5%)
            Returns None if not found or error occurs
        """
        ticker_upper = self.clean_ticker(ticker)
        cache_key = f"quickfs_roic_{ticker_upper}"
        
        # Check cache first
        cached_value = scraper_cache.get(cache_key)
        if cached_value is not None:
            return cached_value
        
        # Fetch from website
        soup = self._get_company_page(ticker_upper)
        if not soup:
            return None
        
        # Try different label variations
        value = self._find_metric_value(soup, "ROIC")
        if value is not None:
            scraper_cache.set(cache_key, value)
            return value
        
        value = self._find_metric_value(soup, "Return on Invested Capital")
        if value is not None:
            scraper_cache.set(cache_key, value)
            return value
        
        return None
    
    def get_fcf_margin(self, ticker: str) -> Optional[float]:
        """
        Get FCF Margin percentage from QuickFS.
        
        Uses caching to avoid repeated requests to the same ticker.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'PLTR')
            
        Returns:
            FCF Margin as a percentage (e.g., 25.5 for 25.5%)
            Returns None if not found or error occurs
        """
        ticker_upper = self.clean_ticker(ticker)
        cache_key = f"quickfs_fcf_margin_{ticker_upper}"
        
        # Check cache first
        cached_value = scraper_cache.get(cache_key)
        if cached_value is not None:
            return cached_value
        
        # Fetch from website
        soup = self._get_company_page(ticker_upper)
        if not soup:
            return None
        
        # Try different label variations
        value = self._find_metric_value(soup, "FCF Margin")
        if value is not None:
            scraper_cache.set(cache_key, value)
            return value
        
        value = self._find_metric_value(soup, "Free Cash Flow Margin")
        if value is not None:
            scraper_cache.set(cache_key, value)
            return value
        
        return None

