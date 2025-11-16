"""
Koyfin scraper for financial ratios.

Koyfin URL format: https://app.koyfin.com/company/{TICKER}/overview

IMPORTANT: This is web scraping, not an official API.
- Be respectful: Add delays between requests
- Rate limiting: Don't make too many requests too quickly
- Cache results when possible to avoid repeated requests

NOTE: Koyfin likely uses JavaScript to render content, so we may need Selenium
to execute JavaScript and extract the rendered content.
"""

from typing import Optional
from bs4 import BeautifulSoup
from app.services.cache import scraper_cache
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


class KoyfinScraper:
    """Scraper for Koyfin financial data using Selenium for JavaScript rendering."""
    
    BASE_URL = "https://app.koyfin.com/company"
    
    def __init__(self):
        """Initialize Koyfin scraper with Selenium WebDriver."""
        self._driver = None
        self._last_request_time = 0
        self._min_delay = 2  # Minimum delay between requests (seconds)
    
    def _get_driver(self):
        """Get or create undetected Chrome WebDriver instance (bypasses bot detection)."""
        if self._driver is None:
            try:
                # Use undetected-chromedriver to bypass bot detection
                options = uc.ChromeOptions()
                options.add_argument('--headless=new')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                options.add_argument('--window-size=1920,1080')
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_argument('--disable-extensions')
                options.add_argument('--disable-plugins')
                options.add_argument('--disable-images')
                
                self._driver = uc.Chrome(options=options, version_main=None, use_subprocess=True)
            except Exception as e:
                print(f"Error initializing undetected Chrome WebDriver: {e}")
                print("Make sure Chrome is installed")
                raise
        
        return self._driver
    
    def clean_ticker(self, ticker: str) -> str:
        """Clean and uppercase ticker symbol."""
        return ticker.upper().strip()
    
    def extract_number(self, text: str) -> Optional[float]:
        """Extract a number from text, handling percentages and formatting."""
        if not text:
            return None
        
        import re
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
    
    def _get_company_page_selenium(self, ticker: str) -> Optional[BeautifulSoup]:
        """
        Fetch the company overview page using Selenium to render JavaScript.
        
        Returns BeautifulSoup of the rendered page.
        """
        ticker_upper = self.clean_ticker(ticker)
        url = f"{self.BASE_URL}/{ticker_upper}/overview"
        
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
                if self._driver:
                    try:
                        self._driver.quit()
                    except:
                        pass
                self._driver = None
                driver = self._get_driver()
            
            driver.get(url)
            
            # Wait for page to load
            try:
                WebDriverWait(driver, 10).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
                
                # Wait for JavaScript to render content
                time.sleep(3)
                
                # Try to find ROIC or table content
                try:
                    WebDriverWait(driver, 8).until(
                        EC.any_of(
                            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'ROIC')]")),
                            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Return on Invested Capital')]")),
                            EC.presence_of_element_located((By.TAG_NAME, "table"))
                        )
                    )
                except TimeoutException:
                    print(f"Warning: Could not find ROIC or table on {url}")
                    # Continue anyway
                
            except TimeoutException:
                print(f"Timeout waiting for page to load on {url}")
                time.sleep(2)
            
            # Get page source after JavaScript execution
            page_source = driver.page_source
            self._last_request_time = time.time()
            
            return BeautifulSoup(page_source, 'lxml')
            
        except Exception as e:
            print(f"Error fetching Koyfin page with Selenium: {e}")
            return None
    
    def __del__(self):
        """Clean up WebDriver on deletion."""
        if self._driver is not None:
            try:
                self._driver.quit()
            except:
                pass
    
    def _find_metric_value(self, soup: BeautifulSoup, metric_label: str) -> Optional[float]:
        """
        Find a metric value in the Koyfin company page.
        
        Koyfin displays metrics in various formats (tables, cards, etc.).
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
                cell_texts = [cell.get_text(strip=True) for cell in cells]
                
                # Check if this row contains our metric label
                for i, text in enumerate(cell_texts):
                    if metric_label.lower() in text.lower():
                        # Try last cell first (most recent)
                        if len(cells) > 1:
                            last_value_text = cell_texts[-1]
                            if last_value_text and last_value_text != '-':
                                value = self.extract_number(last_value_text)
                                if value is not None:
                                    return value
                            
                            # Try backwards from second-to-last
                            for j in range(len(cells) - 2, 0, -1):
                                value_text = cell_texts[j]
                                if value_text and value_text != '-':
                                    value = self.extract_number(value_text)
                                    if value is not None:
                                        return value
                        
                        # Fallback: try adjacent cell
                        if i + 1 < len(cells):
                            value_text = cell_texts[i + 1]
                            if value_text and value_text != '-':
                                value = self.extract_number(value_text)
                                if value is not None:
                                    return value
        
        # Strategy 2: Look for metric in divs/cards
        all_divs = soup.find_all('div')
        for div in all_divs:
            div_text = div.get_text(strip=True)
            if metric_label.lower() in div_text.lower():
                # Try to extract number from the div
                value = self.extract_number(div_text)
                if value is not None:
                    return value
        
        return None
    
    def get_roic(self, ticker: str) -> Optional[float]:
        """
        Get ROIC (Return on Invested Capital) percentage from Koyfin using Selenium.
        
        POLICY: Uses Annual data (most recent fiscal year) for consistency with other sources.
        
        Uses caching to avoid repeated requests to the same ticker.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'PLTR')
            
        Returns:
            ROIC as a percentage (e.g., 15.5 for 15.5%)
            Returns None if not found or error occurs
        """
        ticker_upper = self.clean_ticker(ticker)
        cache_key = f"koyfin_roic_{ticker_upper}"
        
        # Check cache first
        cached_value = scraper_cache.get(cache_key)
        if cached_value is not None:
            return cached_value
        
        # Fetch from website using Selenium (renders JavaScript)
        soup = self._get_company_page_selenium(ticker_upper)
        if not soup:
            return None
        
        # Try different label variations (prioritize full label)
        value = self._find_metric_value(soup, "Return on Invested Capital")
        if value is not None:
            scraper_cache.set(cache_key, value)
            return value
        
        # Fallback to "ROIC"
        value = self._find_metric_value(soup, "ROIC")
        if value is not None:
            scraper_cache.set(cache_key, value)
            return value
        
        return None

