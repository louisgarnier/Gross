"""Deep inspection of Morningstar Key Metrics page to find where Gross Profit Margin is stored."""
from app.scrapers.morningstar import MorningstarScraper
from bs4 import BeautifulSoup
import re

scraper = MorningstarScraper()

# Test Key Metrics page for NVDA
print("=== Deep Inspection of Morningstar Key Metrics page for NVDA ===")
soup = scraper._get_key_metrics_page("NVDA")

if soup:
    print("\n--- All text content (first 2000 chars) ---")
    all_text = soup.get_text()
    print(all_text[:2000])
    
    print("\n--- Searching for 'Gross Profit Margin' in all text ---")
    if 'Gross Profit Margin' in all_text or 'gross profit margin' in all_text.lower():
        print("✅ Found 'Gross Profit Margin' in page text!")
        # Find all occurrences
        lines = all_text.split('\n')
        for i, line in enumerate(lines):
            if 'gross profit margin' in line.lower() or 'gross margin' in line.lower():
                print(f"Line {i}: {line[:200]}")
    else:
        print("❌ 'Gross Profit Margin' NOT found in page text")
    
    print("\n--- Searching for percentage patterns near 'gross' ---")
    gross_pattern = r'gross[^%]*?(\d+\.?\d*)%'
    matches = re.findall(gross_pattern, all_text, re.IGNORECASE)
    if matches:
        print(f"Found percentage patterns near 'gross': {matches[:5]}")
    
    print("\n--- Looking for all divs with data attributes ---")
    divs_with_data = soup.find_all('div', attrs=lambda x: x and any(k.startswith('data-') for k in x.keys()))
    print(f"Found {len(divs_with_data)} divs with data attributes")
    for div in divs_with_data[:5]:
        print(f"  Div: {div.get('class')} - {div.get_text(strip=True)[:100]}")
    
    print("\n--- Looking for script tags (might contain data) ---")
    scripts = soup.find_all('script')
    print(f"Found {len(scripts)} script tags")
    for i, script in enumerate(scripts[:3]):
        script_text = script.get_text()
        if 'gross' in script_text.lower() or 'margin' in script_text.lower():
            print(f"  Script {i} contains 'gross' or 'margin': {script_text[:300]}")
    
    print("\n--- Looking for JSON data in script tags ---")
    for script in scripts:
        script_text = script.get_text()
        if 'json' in script_text.lower() or '{' in script_text:
            # Try to find JSON-like structures
            if 'gross' in script_text.lower():
                print(f"  Found potential JSON with 'gross': {script_text[:500]}")
    
    print("\n--- All table elements (even if empty) ---")
    tables = soup.find_all('table')
    print(f"Found {len(tables)} table elements")
    for i, table in enumerate(tables):
        print(f"  Table {i}: {len(table.find_all('tr'))} rows, {len(table.find_all('td'))} cells")
        if len(table.find_all('td')) > 0:
            first_row = table.find('tr')
            if first_row:
                cells = first_row.find_all(['td', 'th'])
                print(f"    First row cells: {[c.get_text(strip=True)[:50] for c in cells[:5]]}")
    
    print("\n--- Looking for elements with 'gross' or 'margin' in class or id ---")
    elements = soup.find_all(attrs={'class': re.compile(r'gross|margin', re.I)})
    elements += soup.find_all(attrs={'id': re.compile(r'gross|margin', re.I)})
    print(f"Found {len(elements)} elements with 'gross' or 'margin' in class/id")
    for elem in elements[:5]:
        print(f"  {elem.name}: class={elem.get('class')}, id={elem.get('id')}, text={elem.get_text(strip=True)[:100]}")
    
else:
    print("Failed to fetch Morningstar Key Metrics page.")

