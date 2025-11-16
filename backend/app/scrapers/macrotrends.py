"""
Macrotrends scraper for financial ratios.

Macrotrends URL format: https://www.macrotrends.net/stocks/charts/{TICKER}/{company-name}/{metric}

Examples:
- Gross Margin: https://www.macrotrends.net/stocks/charts/PLTR/palantir/gross-margin
- FCF Margin: https://www.macrotrends.net/stocks/charts/PLTR/palantir/free-cash-flow-margin

IMPORTANT: This is web scraping, not an official API.
- Be respectful: Add delays between requests
- Rate limiting: Don't make too many requests too quickly
- Cache results when possible to avoid repeated requests
"""

from typing import Optional
from bs4 import BeautifulSoup
from .base import BaseScraper
from app.services.cache import scraper_cache


class MacrotrendsScraper(BaseScraper):
    """Scraper for Macrotrends financial data."""
    
    BASE_URL = "https://www.macrotrends.net/stocks/charts"
    
    def _get_company_name(self, ticker: str) -> str:
        """
        Get company name slug from ticker.
        
        This is a simplified mapping. In production, you might need to
        scrape the ticker page first to get the company name slug.
        
        For now, we'll try common patterns or use the ticker directly.
        """
        # Common mappings (can be expanded)
        company_map = {
            "PLTR": "palantir",
            "NVDA": "nvidia",
            "MSFT": "microsoft",
            "AAPL": "apple",
        }
        return company_map.get(ticker.upper(), ticker.lower())
    
    def _get_metric_page(self, ticker: str, metric: str) -> Optional[BeautifulSoup]:
        """Fetch the metric page for a ticker."""
        ticker = self.clean_ticker(ticker)
        company_name = self._get_company_name(ticker)
        url = f"{self.BASE_URL}/{ticker}/{company_name}/{metric}"
        return self.fetch_page(url)
    
    def _find_latest_value(self, soup: BeautifulSoup, metric_name: str = None) -> Optional[float]:
        """
        Find the latest (most recent) value from Macrotrends page.
        
        Macrotrends displays data in tables with structure like:
        Date | TTM Revenue | TTM Gross Profit | Gross Margin
        2025-09-30 | $3.90B | $3.15B | 80.81%
        
        We need to find the column header matching the metric and get the first data row value.
        """
        if not soup:
            return None
        
        # Strategy 1: Find table and locate the correct column by header
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            if len(rows) < 2:
                continue
            
            # Find header row (usually first row)
            header_row = rows[0]
            header_cells = header_row.find_all(['th', 'td'])
            header_texts = [cell.get_text(strip=True).lower() for cell in header_cells]
            
            # Find the column index for the metric we're looking for
            # For Gross Margin, look for "gross margin" in headers
            # For FCF Margin, look for "free cash flow margin" or "fcf margin"
            target_column = None
            if metric_name:
                metric_lower = metric_name.lower()
                for i, header_text in enumerate(header_texts):
                    if metric_lower in header_text or header_text in metric_lower:
                        target_column = i
                        break
            
            # If we found the target column, get value from first data row
            if target_column is not None and target_column < len(header_cells):
                # Get first data row (usually row 1, after header)
                for data_row in rows[1:]:
                    data_cells = data_row.find_all(['td', 'th'])
                    if target_column < len(data_cells):
                        cell_text = data_cells[target_column].get_text(strip=True)
                        value = self.extract_number(cell_text)
                        if value is not None and 0 <= value <= 100:  # Reasonable percentage
                            return value
            
            # Fallback: If no specific column found, look for percentage in first data row
            # This handles cases where column name doesn't match exactly
            if target_column is None:
                for data_row in rows[1:]:
                    data_cells = data_row.find_all(['td', 'th'])
                    # Skip first column (usually date), check others
                    for i in range(1, min(len(data_cells), 5)):  # Check columns 1-4
                        cell_text = data_cells[i].get_text(strip=True)
                        # Check if it's a percentage (contains %)
                        if '%' in cell_text:
                            value = self.extract_number(cell_text)
                            if value is not None and 0 <= value <= 100:
                                return value
        
        # Strategy 2: Look for text patterns like "80.81%" in context
        page_text = soup.get_text()
        import re
        # Look for percentage patterns
        percentage_pattern = r'(\d+\.?\d*)\s*%'
        matches = re.findall(percentage_pattern, page_text)
        for match in matches:
            try:
                value = float(match)
                if 0 <= value <= 100:  # Reasonable percentage
                    return value
            except ValueError:
                continue
        
        return None
    
    def get_gross_margin(self, ticker: str) -> Optional[float]:
        """
        Get Gross Margin percentage from Macrotrends.
        
        Uses caching to avoid repeated requests to the same ticker.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'PLTR')
            
        Returns:
            Gross Margin as a percentage (e.g., 80.81 for 80.81%)
            Returns None if not found or error occurs
        """
        ticker_upper = self.clean_ticker(ticker)
        cache_key = f"macrotrends_gross_margin_{ticker_upper}"
        
        # Check cache first
        cached_value = scraper_cache.get(cache_key)
        if cached_value is not None:
            return cached_value
        
        # Fetch from website
        soup = self._get_metric_page(ticker_upper, "gross-margin")
        if not soup:
            return None
        
        # Find the latest value (pass metric name to help find correct column)
        value = self._find_latest_value(soup, metric_name="Gross Margin")
        if value is not None:
            scraper_cache.set(cache_key, value)  # Cache the result
            return value
        
        return None
    
    def get_fcf_margin(self, ticker: str) -> Optional[float]:
        """
        Get FCF Margin percentage from Macrotrends.
        
        Uses caching to avoid repeated requests to the same ticker.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'PLTR')
            
        Returns:
            FCF Margin as a percentage (e.g., 25.5 for 25.5%)
            Returns None if not found or error occurs
        """
        ticker_upper = self.clean_ticker(ticker)
        cache_key = f"macrotrends_fcf_margin_{ticker_upper}"
        
        # Check cache first
        cached_value = scraper_cache.get(cache_key)
        if cached_value is not None:
            return cached_value
        
        # Fetch from website
        soup = self._get_metric_page(ticker_upper, "free-cash-flow-margin")
        if not soup:
            return None
        
        # Find the latest value (pass metric name to help find correct column)
        value = self._find_latest_value(soup, metric_name="Free Cash Flow Margin")
        if value is not None:
            scraper_cache.set(cache_key, value)  # Cache the result
            return value
        
        return None

