"""Inspect Morningstar page structure to find correct selectors."""
from app.scrapers.morningstar import MorningstarScraper
from bs4 import BeautifulSoup

scraper = MorningstarScraper()

# Test Gross Margin page
print("=== Inspecting Morningstar quote page for PLTR ===")
soup = scraper._get_quote_page("PLTR")

if soup:
    print("\n--- Page Title ---")
    title = soup.find('title')
    if title:
        print(f"Title: {title.get_text()}")
    
    print("\n--- Looking for Gross Margin in tables ---")
    tables = soup.find_all('table')
    if tables:
        for i, table in enumerate(tables):
            print(f"\n--- Table {i+1} ---")
            rows = table.find_all('tr')
            for j, row in enumerate(rows[:10]):  # Inspect first 10 rows
                cells = row.find_all(['td', 'th'])
                cell_texts = [cell.get_text(strip=True) for cell in cells]
                print(f"Row {j}: {cell_texts}")
                # Check for Gross Margin related text
                row_text = ' '.join(cell_texts).lower()
                if 'gross margin' in row_text or 'gross profit' in row_text:
                    print(f"    *** FOUND POTENTIAL GROSS MARGIN MATCH in row {j} ***")
                    for k, cell in enumerate(cells):
                        print(f"      Cell {k}: '{cell.get_text(strip=True)}'")
    else:
        print("No tables found on page.")
    
    print("\n--- Looking for Gross Margin in divs/cards ---")
    # Look for common patterns in divs
    all_text = soup.get_text()
    import re
    gm_pattern = r'(gross margin|gross profit margin)[:\s]*([\d.]+)%?'
    matches = re.findall(gm_pattern, all_text, re.IGNORECASE)
    if matches:
        print(f"Found Gross Margin patterns: {matches}")
    else:
        print("No Gross Margin patterns found in page text.")
    
    # Test _find_metric_value
    print("\n=== Testing _find_metric_value ===")
    gm_value = scraper._find_metric_value(soup, "Gross Margin")
    print(f"_find_metric_value for Gross Margin returned: {gm_value}")
    
    # Print a sample of page text to see structure
    print("\n--- Sample page text (first 1000 chars) ---")
    print(all_text[:1000])
    
    # Search for all percentage values near "gross" or "margin"
    print("\n--- Searching for 'gross' or 'margin' in page text ---")
    lines = all_text.split('\n')
    for i, line in enumerate(lines):
        line_lower = line.lower()
        if 'gross' in line_lower or 'margin' in line_lower:
            print(f"Line {i}: {line[:200]}")
    
    # Check for data attributes or specific classes
    print("\n--- Looking for data attributes or classes with 'gross' or 'margin' ---")
    elements_with_gross = soup.find_all(attrs={'class': re.compile(r'gross|margin', re.I)})
    if elements_with_gross:
        print(f"Found {len(elements_with_gross)} elements with 'gross' or 'margin' in class")
        for elem in elements_with_gross[:5]:
            print(f"  {elem.name}: {elem.get('class')} - {elem.get_text(strip=True)[:100]}")
    
    # Check all text content for percentage patterns near "gross"
    print("\n--- Looking for percentage patterns near 'gross' ---")
    gross_pattern = r'gross[^%]*?(\d+\.?\d*)%'
    matches = re.findall(gross_pattern, all_text, re.IGNORECASE)
    if matches:
        print(f"Found percentage patterns near 'gross': {matches}")
    
else:
    print("Failed to fetch Morningstar page.")

