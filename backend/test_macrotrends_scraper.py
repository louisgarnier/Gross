"""
Test script for Macrotrends scraper.

This tests the scraper and compares results with the actual Macrotrends website.
Run this to verify the scraper is working correctly.
"""

from app.scrapers.macrotrends import MacrotrendsScraper

def test_macrotrends_gross_margin_pltr():
    """Test Gross Margin for PLTR."""
    print("\n" + "="*50)
    print("TEST: Macrotrends Gross Margin for PLTR")
    print("="*50)
    
    scraper = MacrotrendsScraper()
    
    # First, let's inspect the page structure
    print("Fetching page...")
    soup = scraper._get_metric_page("PLTR", "gross-margin")
    
    if soup:
        print("✅ Page fetched successfully")
        
        # Try to find the value
        value = scraper.get_gross_margin("PLTR")
        print(f"Scraper returned: {value}")
        
        if value is not None:
            print(f"✅ PASSED - Got value: {value}%")
            print("   Please verify on: https://www.macrotrends.net/stocks/charts/PLTR/palantir/gross-margin")
            print("   Check the most recent year's Gross Margin value")
            return True
        else:
            print("❌ FAILED - Scraper returned None")
            print("   Need to inspect page structure to find correct selector")
            return False
    else:
        print("❌ FAILED - Could not fetch page")
        return False

if __name__ == "__main__":
    print("\n" + "="*50)
    print("MACROTRENDS SCRAPER TESTING")
    print("="*50)
    print("\nMake sure you can access Macrotrends")
    print("Check the values on the website before running tests.")
    print("\nStarting tests...\n")
    
    results = []
    results.append(("PLTR Gross Margin", test_macrotrends_gross_margin_pltr()))
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("\nNext step: Verify values match Macrotrends website manually")
        print("Then integrate into API")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("Need to inspect page structure and fix scraper")
    print("="*50 + "\n")

