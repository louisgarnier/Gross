"""
Base scraper class with common functionality.
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional
import time
import re


class BaseScraper:
    """Base class for all financial data scrapers."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def fetch_page(self, url: str, retries: int = 3) -> Optional[BeautifulSoup]:
        """Fetch and parse a web page."""
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return BeautifulSoup(response.content, 'lxml')
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                print(f"Error fetching {url}: {e}")
                return None
    
    def extract_number(self, text: str) -> Optional[float]:
        """Extract a number from text, handling percentages and formatting."""
        if not text:
            return None
        
        # Remove common formatting
        text = text.replace(',', '').replace('$', '').strip()
        
        # Handle percentages
        is_percentage = '%' in text
        text = text.replace('%', '')
        
        # Extract number (handles negative, decimals, etc.)
        match = re.search(r'-?\d+\.?\d*', text)
        if match:
            value = float(match.group())
            return value
        return None
    
    def clean_ticker(self, ticker: str) -> str:
        """Clean and uppercase ticker symbol."""
        return ticker.upper().strip()

