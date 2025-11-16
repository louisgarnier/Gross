"""Inspect Morningstar Key Metrics page structure to find Gross Profit Margin."""
from app.scrapers.morningstar import MorningstarScraper
from bs4 import BeautifulSoup

scraper = MorningstarScraper()

# Test Key Metrics page for NVDA
print("=== Inspecting Morningstar Key Metrics page for NVDA ===")
soup = scraper._get_key_metrics_page("NVDA")

if soup:
    print("\n--- Page Title ---")
    title = soup.find('title')
    if title:
        print(f"Title: {title.get_text()}")
    
    print("\n--- Looking for Gross Profit Margin in tables ---")
    tables = soup.find_all('table')
    if tables:
        for i, table in enumerate(tables):
            print(f"\n--- Table {i+1} ---")
            rows = table.find_all('tr')
            for j, row in enumerate(rows[:15]):  # Inspect first 15 rows
                cells = row.find_all(['td', 'th'])
                cell_texts = [cell.get_text(strip=True) for cell in cells]
                print(f"Row {j}: {cell_texts}")
                # Check for Gross Profit Margin related text
                row_text = ' '.join(cell_texts).lower()
                if 'gross profit margin' in row_text or 'gross margin' in row_text:
                    print(f"    *** FOUND POTENTIAL GROSS MARGIN MATCH in row {j} ***")
                    for k, cell in enumerate(cells):
                        print(f"      Cell {k}: '{cell.get_text(strip=True)}'")
    else:
        print("No tables found on page.")
    
    # Test _find_table_row_value
    print("\n=== Testing _find_table_row_value ===")
    gm_value = scraper._find_table_row_value(soup, "Gross Profit Margin", column_index=1)
    print(f"_find_table_row_value for 'Gross Profit Margin' (col 1) returned: {gm_value}")
    
    # Try different column indices
    for col_idx in range(1, 4):
        gm_value = scraper._find_table_row_value(soup, "Gross Profit Margin", column_index=col_idx)
        print(f"_find_table_row_value for 'Gross Profit Margin' (col {col_idx}) returned: {gm_value}")
    
else:
    print("Failed to fetch Morningstar Key Metrics page.")

