"""Inspect QuickFS page structure to find correct selectors."""
from app.scrapers.quickfs import QuickFSScraper
from bs4 import BeautifulSoup

scraper = QuickFSScraper()

# Test ROIC page
print("=== Inspecting QuickFS company page for PLTR ===")
soup = scraper._get_company_page("PLTR")

if soup:
    print("\n--- Page Title ---")
    title = soup.find('title')
    if title:
        print(f"Title: {title.get_text()}")
    
    print("\n--- Looking for ROIC in tables ---")
    tables = soup.find_all('table')
    if tables:
        for i, table in enumerate(tables):
            print(f"\n--- Table {i+1} ---")
            rows = table.find_all('tr')
            for j, row in enumerate(rows[:10]):  # Inspect first 10 rows
                cells = row.find_all(['td', 'th'])
                cell_texts = [cell.get_text(strip=True) for cell in cells]
                print(f"Row {j}: {cell_texts}")
                # Check for ROIC related text
                row_text = ' '.join(cell_texts).lower()
                if 'roic' in row_text or 'return on invested capital' in row_text:
                    print(f"    *** FOUND POTENTIAL ROIC MATCH in row {j} ***")
                    for k, cell in enumerate(cells):
                        print(f"      Cell {k}: '{cell.get_text(strip=True)}'")
    else:
        print("No tables found on page.")
    
    print("\n--- Looking for ROIC in divs/cards ---")
    # Look for common patterns in divs
    all_text = soup.get_text()
    import re
    roic_pattern = r'(roic|return on invested capital)[:\s]*([\d.]+)%?'
    matches = re.findall(roic_pattern, all_text, re.IGNORECASE)
    if matches:
        print(f"Found ROIC patterns: {matches}")
    else:
        print("No ROIC patterns found in page text.")
    
    # Test _find_metric_value
    print("\n=== Testing _find_metric_value ===")
    roic_value = scraper._find_metric_value(soup, "ROIC")
    print(f"_find_metric_value for ROIC returned: {roic_value}")
    
else:
    print("Failed to fetch QuickFS page.")

