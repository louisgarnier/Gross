"""
Inspect Morningstar page structure for ROIC extraction.
"""

from app.scrapers.morningstar import MorningstarScraper
from bs4 import BeautifulSoup

scraper = MorningstarScraper()
print("=== Testing different Morningstar pages for ROIC ===\n")

# Try different pages
pages_to_test = [
    ("Key Ratios", lambda: scraper._get_key_ratios_page_selenium("PLTR")),
    ("Key Metrics", lambda: scraper._get_key_metrics_page_selenium("PLTR")),
]

for page_name, fetch_func in pages_to_test:
    print(f"\n--- Testing {page_name} page ---")
    soup = fetch_func()
    if soup:
        full_text = soup.get_text()
        if 'ROIC' in full_text.upper() or 'Return on Invested Capital' in full_text:
            print(f"✅ ROIC FOUND on {page_name} page!")
            # Show context
            lines = full_text.split('\n')
            for i, line in enumerate(lines):
                if 'ROIC' in line.upper() or 'Return on Invested Capital' in line:
                    start = max(0, i-2)
                    end = min(len(lines), i+3)
                    print(f"Context (line {i}):")
                    for j in range(start, end):
                        marker = ">>> " if j == i else "    "
                        print(f"{marker}{lines[j]}")
                    break
        else:
            print(f"❌ ROIC not found on {page_name} page")
    else:
        print(f"❌ Could not fetch {page_name} page")

if soup:
    print("=== Looking for ROIC text ===\n")
    
    # Find all elements containing ROIC
    roic_elements = soup.find_all(string=lambda text: text and ('ROIC' in text.upper() or 'Return on Invested Capital' in text))
    
    print(f"Found {len(roic_elements)} elements with ROIC text:\n")
    for i, elem in enumerate(roic_elements[:10]):
        parent = elem.parent if elem.parent else None
        print(f"Element {i+1}:")
        print(f"  Text: {elem.strip()}")
        if parent:
            print(f"  Parent tag: {parent.name}")
            print(f"  Parent text: {parent.get_text(strip=True)[:200]}")
        print()
    
    # Also search in all text
    print("\n=== Full page text (searching for ROIC context) ===\n")
    full_text = soup.get_text()
    lines = full_text.split('\n')
    for i, line in enumerate(lines):
        if 'ROIC' in line.upper() or 'Return on Invested Capital' in line:
            # Print context (previous and next lines)
            start = max(0, i-2)
            end = min(len(lines), i+3)
            print(f"Line {i} (context):")
            for j in range(start, end):
                marker = ">>> " if j == i else "    "
                print(f"{marker}{lines[j]}")
            print()
    
    # Look for tables
    print("\n=== Looking for tables with ROIC ===\n")
    tables = soup.find_all('table')
    print(f"Found {len(tables)} tables")
    for i, table in enumerate(tables):
        rows = table.find_all('tr')
        for row in rows:
            cells = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
            if any('ROIC' in str(cell).upper() or 'Return on Invested Capital' in str(cell) for cell in cells):
                print(f"Table {i+1}, ROIC row: {cells}")
                print(f"  HTML: {str(row)[:500]}")
                print()
else:
    print("Failed to fetch page")

