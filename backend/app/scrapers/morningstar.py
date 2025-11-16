"""
Morningstar scraper for financial ratios.

Morningstar URL format: https://www.morningstar.com/stocks/{exchange}/{TICKER}/quote

Examples:
- PLTR (NASDAQ): https://www.morningstar.com/stocks/xnas/PLTR/quote
- NVDA (NASDAQ): https://www.morningstar.com/stocks/xnas/NVDA/quote

IMPORTANT: This is web scraping, not an official API.
- Be respectful: Add delays between requests
- Rate limiting: Don't make too many requests too quickly
- Cache results when possible to avoid repeated requests

NOTE: Morningstar uses JavaScript to render table content, so we use Selenium
to execute JavaScript and extract the rendered content.
"""

from typing import Optional
from bs4 import BeautifulSoup
from app.services.cache import scraper_cache
import re
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


class MorningstarScraper:
    """Scraper for Morningstar financial data using Selenium for JavaScript rendering."""
    
    BASE_URL = "https://www.morningstar.com/stocks"
    
    def __init__(self):
        """Initialize Morningstar scraper with Selenium WebDriver."""
        self._driver = None
        self._last_request_time = 0
        self._min_delay = 2  # Minimum delay between requests (seconds) - reduced for speed
    
    def _get_driver(self):
        """Get or create undetected Chrome WebDriver instance (bypasses bot detection)."""
        if self._driver is None:
            try:
                # Use undetected-chromedriver to bypass bot detection
                options = uc.ChromeOptions()
                # Use headless mode to avoid window popup and improve speed
                options.add_argument('--headless=new')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                options.add_argument('--window-size=1920,1080')
                options.add_argument('--disable-blink-features=AutomationControlled')
                # Reduce resource usage
                options.add_argument('--disable-extensions')
                options.add_argument('--disable-plugins')
                options.add_argument('--disable-images')  # Don't load images for speed
                
                self._driver = uc.Chrome(options=options, version_main=None, use_subprocess=True)
            except Exception as e:
                print(f"Error initializing undetected Chrome WebDriver: {e}")
                print("Make sure Chrome is installed")
                raise
        
        return self._driver
    
    def clean_ticker(self, ticker: str) -> str:
        """Clean and uppercase ticker symbol."""
        return ticker.upper().strip()
    
    def _get_exchange(self, ticker: str) -> str:
        """
        Get exchange code from ticker.
        
        For now, we'll assume most stocks are on NASDAQ (xnas).
        In production, you might need to look up the exchange.
        """
        # Common exchanges mapping
        # Most tech stocks are on NASDAQ
        # We can expand this later if needed
        return "xnas"  # Default to NASDAQ
    
    def _get_key_metrics_page_selenium(self, ticker: str) -> Optional[BeautifulSoup]:
        """
        Fetch the key metrics page using Selenium to render JavaScript.
        
        Returns BeautifulSoup of the rendered page.
        """
        ticker_upper = self.clean_ticker(ticker)
        exchange = self._get_exchange(ticker_upper)
        url = f"{self.BASE_URL}/{exchange}/{ticker_upper.lower()}/key-metrics"
        
        # Rate limiting
        current_time = time.time()
        time_since_last = current_time - self._last_request_time
        if time_since_last < self._min_delay:
            time.sleep(self._min_delay - time_since_last)
        
        driver = None
        try:
            driver = self._get_driver()
            
            # Check if driver is still valid
            try:
                driver.current_url
            except:
                # Driver closed, recreate it
                if self._driver:
                    try:
                        self._driver.quit()
                    except:
                        pass
                self._driver = None
                driver = self._get_driver()
            
            driver.get(url)
            
            # Wait for page to load - try multiple strategies
            try:
                # Wait for any content to load (reduced timeout for speed)
                WebDriverWait(driver, 10).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
                
                # Try to find "Gross Profit Margin" text directly (faster than waiting for all tables)
                try:
                    WebDriverWait(driver, 8).until(
                        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Gross Profit Margin')]"))
                    )
                except TimeoutException:
                    # If not found, wait a bit and try table
                    time.sleep(1)
                    try:
                        WebDriverWait(driver, 3).until(
                            EC.presence_of_element_located((By.TAG_NAME, "table"))
                        )
                    except TimeoutException:
                        print(f"Warning: Could not find 'Gross Profit Margin' or table on {url}")
                        # Continue anyway, maybe it's there but selector is different
                
            except TimeoutException:
                print(f"Timeout waiting for page to load on {url}")
                # Continue anyway, try to get page source
                time.sleep(2)
            
            # Get page source after JavaScript execution
            page_source = driver.page_source
            self._last_request_time = time.time()
            
            return BeautifulSoup(page_source, 'lxml')
            
        except Exception as e:
            print(f"Error fetching Morningstar page with Selenium: {e}")
            # Don't close driver on error, keep it for next request
            return None
    
    def __del__(self):
        """Clean up WebDriver on deletion."""
        if self._driver is not None:
            try:
                self._driver.quit()
            except:
                pass
    
    def _find_table_row_value(self, soup: BeautifulSoup, row_label: str, column_index: int = 1) -> Optional[float]:
        """
        Find a value in a Morningstar financial table.
        
        Morningstar Financials page has tables with structure:
        - First column: Metric name (e.g., "Gross Profit", "Revenue")
        - Subsequent columns: Years (TTM, 2025, 2024, etc.)
        
        We find the row by label and extract the value from the specified column.
        Column index 1 = first year column (usually most recent)
        
        Args:
            soup: BeautifulSoup object
            row_label: Label to search for (e.g., "Gross Profit", "Revenue")
            column_index: Column index to extract (1 = first year, 2 = second year, etc.)
            
        Returns:
            Value as float, or None if not found
        """
        if not soup:
            return None
        
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) < 2:
                    continue
                
                # Check first cell for the label
                first_cell_text = cells[0].get_text(strip=True)
                if row_label.lower() in first_cell_text.lower():
                    # Found the row, extract value from specified column
                    if column_index < len(cells):
                        value_text = cells[column_index].get_text(strip=True)
                        # Remove commas and convert
                        value_text = value_text.replace(',', '').strip()
                        # Handle empty or dash
                        if value_text == '' or value_text == '—' or value_text == '-':
                            return None
                        try:
                            # Handle percentage values (e.g., "80.81%")
                            if '%' in value_text:
                                value_text = value_text.replace('%', '')
                            # Extract number (handles negative, decimals, etc.)
                            import re
                            match = re.search(r'-?\d+\.?\d*', value_text)
                            if match:
                                value = float(match.group())
                                return value
                        except (ValueError, TypeError):
                            continue
        
        return None
    
    def get_gross_margin(self, ticker: str) -> Optional[float]:
        """
        Get Gross Margin percentage from Morningstar using Selenium.
        
        POLICY: Uses Annual data (most recent fiscal year) for consistency with other sources.
        
        Strategy: Morningstar Key Metrics page displays "Gross Profit Margin %" directly in a table.
        We use Selenium to render JavaScript, then extract the value from the most recent fiscal year column.
        
        Uses caching to avoid repeated requests to the same ticker.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'PLTR')
            
        Returns:
            Gross Margin as a percentage (e.g., 80.81 for 80.81%)
            Returns None if not found or error occurs
        """
        ticker_upper = self.clean_ticker(ticker)
        cache_key = f"morningstar_gross_margin_{ticker_upper}"
        
        # Check cache first
        cached_value = scraper_cache.get(cache_key)
        if cached_value is not None:
            return cached_value
        
        # Fetch Key Metrics page using Selenium (renders JavaScript)
        soup = self._get_key_metrics_page_selenium(ticker_upper)
        if not soup:
            return None
        
        # Look for "Gross Profit Margin %" in table
        gross_margin = self._find_table_row_value(soup, "Gross Profit Margin", column_index=1)
        if gross_margin is not None:
            scraper_cache.set(cache_key, gross_margin)
            return gross_margin
        
        return None

