"""Debug Morningstar scraper with Selenium to see what's actually retrieved."""
from app.scrapers.morningstar import MorningstarScraper
from bs4 import BeautifulSoup

scraper = MorningstarScraper()

print("=== Testing Morningstar with Selenium for PLTR ===")
soup = scraper._get_key_metrics_page_selenium("PLTR")

if soup:
    print("\n--- Checking if 'Gross Profit Margin' is in page text ---")
    all_text = soup.get_text()
    if 'Gross Profit Margin' in all_text:
        print("✅ Found 'Gross Profit Margin' in page text!")
        
        # Find the line
        lines = all_text.split('\n')
        for i, line in enumerate(lines):
            if 'Gross Profit Margin' in line:
                print(f"Line {i}: {line}")
                # Print surrounding lines
                for j in range(max(0, i-2), min(len(lines), i+3)):
                    print(f"  {j}: {lines[j][:150]}")
    else:
        print("❌ 'Gross Profit Margin' NOT found in page text")
        print("\n--- Sample of page text (first 1000 chars) ---")
        print(all_text[:1000])
    
    print("\n--- Checking tables ---")
    tables = soup.find_all('table')
    print(f"Found {len(tables)} tables")
    for i, table in enumerate(tables):
        rows = table.find_all('tr')
        print(f"\nTable {i}: {len(rows)} rows")
        for j, row in enumerate(rows[:10]):
            cells = row.find_all(['td', 'th'])
            cell_texts = [cell.get_text(strip=True) for cell in cells]
            print(f"  Row {j}: {cell_texts[:5]}")
            if any('gross' in text.lower() or 'margin' in text.lower() for text in cell_texts):
                print(f"    *** FOUND GROSS/MARGIN in row {j} ***")
    
    # Test _find_table_row_value
    print("\n=== Testing _find_table_row_value ===")
    gm_value = scraper._find_table_row_value(soup, "Gross Profit Margin", column_index=1)
    print(f"Result: {gm_value}")
    
    # Try different variations
    for label in ["Gross Profit Margin", "Gross Profit Margin %", "Gross Margin"]:
        for col in range(1, 4):
            val = scraper._find_table_row_value(soup, label, column_index=col)
            if val is not None:
                print(f"Found with label '{label}', column {col}: {val}")
else:
    print("Failed to fetch page with Selenium")

