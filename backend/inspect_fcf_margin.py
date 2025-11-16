"""Inspect Macrotrends financial-statements page to find FCF Margin."""
from app.scrapers.macrotrends import MacrotrendsScraper

scraper = MacrotrendsScraper()
soup = scraper._get_metric_page("PLTR", "financial-statements")

if soup:
    print("=== Looking for FCF Margin in financial-statements ===")
    
    # Look for tables
    tables = soup.find_all('table')
    print(f"Found {len(tables)} tables")
    
    # Search for FCF-related text
    page_text = soup.get_text()
    
    # Look for FCF Margin patterns
    import re
    fcf_patterns = [
        r'Free Cash Flow Margin',
        r'FCF Margin',
        r'Free Cash Flow.*Margin',
        r'Cash Flow Margin'
    ]
    
    print("\n=== Searching for FCF Margin patterns ===")
    for pattern in fcf_patterns:
        matches = re.findall(pattern, page_text, re.IGNORECASE)
        if matches:
            print(f"Found '{pattern}': {matches[:3]}")
    
    # Look in tables for FCF-related rows
    print("\n=== Checking tables for FCF-related rows ===")
    for i, table in enumerate(tables[:3]):
        rows = table.find_all('tr')
        for j, row in enumerate(rows[:15]):
            row_text = row.get_text()
            if 'cash flow' in row_text.lower() and 'margin' in row_text.lower():
                print(f"\nTable {i+1}, Row {j}:")
                cells = row.find_all(['td', 'th'])
                for k, cell in enumerate(cells):
                    print(f"  Cell {k}: '{cell.get_text(strip=True)}'")

