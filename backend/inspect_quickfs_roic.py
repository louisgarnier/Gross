"""
Inspect QuickFS page structure for ROIC extraction.
"""

from app.scrapers.quickfs import QuickFSScraper
from bs4 import BeautifulSoup

scraper = QuickFSScraper()
print("=== Fetching QuickFS page for PLTR ===\n")

soup = scraper._get_company_page_selenium("PLTR")

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
            print(f"  Parent HTML: {str(parent)[:300]}")
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
    
    # Look for tables with ROIC
    print("\n=== Looking for tables with ROIC ===\n")
    tables = soup.find_all('table')
    print(f"Found {len(tables)} tables")
    for i, table in enumerate(tables):
        print(f"\n=== Table {i+1} ===")
        rows = table.find_all('tr')
        for row in rows:
            cells = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
            if any('ROIC' in str(cell).upper() or 'Return on Invested Capital' in str(cell) for cell in cells):
                print(f"ROIC row found: {cells}")
                print(f"  Number of cells: {len(cells)}")
                # Print HTML structure
                print(f"  HTML: {str(row)[:500]}")
                # Find which cell has ROIC
                for j, cell in enumerate(row.find_all(['td', 'th'])):
                    cell_text = cell.get_text(strip=True)
                    if 'ROIC' in cell_text.upper() or 'Return on Invested Capital' in cell_text:
                        print(f"  Cell {j} contains ROIC label: '{cell_text}'")
                        # Check adjacent cells
                        if j + 1 < len(cells):
                            print(f"  Cell {j+1} (next): '{cells[j+1]}'")
                        # Check last cell (most recent year)
                        if len(cells) > 1:
                            print(f"  Last cell (most recent): '{cells[-1]}'")
                print()
else:
    print("Failed to fetch page")

