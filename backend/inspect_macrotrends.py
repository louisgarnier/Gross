"""Inspect Macrotrends page structure to find correct selectors."""
from app.scrapers.macrotrends import MacrotrendsScraper

scraper = MacrotrendsScraper()
soup = scraper._get_metric_page("PLTR", "gross-margin")

if soup:
    print("=== Looking for tables (detailed) ===")
    tables = soup.find_all('table')
    print(f"Found {len(tables)} tables")
    
    for i, table in enumerate(tables):
        print(f"\n--- Table {i+1} ---")
        rows = table.find_all('tr')
        print(f"  Rows: {len(rows)}")
        for j, row in enumerate(rows[:10]):  # First 10 rows
            cells = row.find_all(['td', 'th'])
            cell_texts = [cell.get_text(strip=True) for cell in cells]
            print(f"  Row {j}: {cell_texts}")
            # Check if this row contains "80.81" or similar
            row_text = ' '.join(cell_texts)
            if '80.81' in row_text or '80' in row_text:
                print(f"    *** FOUND POTENTIAL MATCH in row {j} ***")
                for k, cell in enumerate(cells):
                    print(f"      Cell {k}: '{cell.get_text(strip=True)}'")
    
    print("\n=== Looking for '80.81' in page text ===")
    page_text = soup.get_text()
    if '80.81' in page_text:
        # Find context around 80.81
        import re
        matches = list(re.finditer(r'80\.81', page_text))
        for match in matches:
            start = max(0, match.start() - 50)
            end = min(len(page_text), match.end() + 50)
            print(f"  Context: ...{page_text[start:end]}...")

