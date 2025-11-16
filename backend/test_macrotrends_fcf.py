"""
Test script for Macrotrends FCF Margin scraper.
"""

from app.scrapers.macrotrends import MacrotrendsScraper

def test_macrotrends_fcf_margin_pltr():
    """Test FCF Margin for PLTR."""
    print("\n" + "="*50)
    print("TEST: Macrotrends FCF Margin for PLTR")
    print("="*50)
    
    scraper = MacrotrendsScraper()
    
    print("Fetching page...")
    value = scraper.get_fcf_margin("PLTR")
    print(f"Scraper returned: {value}")
    
    if value is not None:
        print(f"✅ PASSED - Got value: {value}%")
        print("   Please verify on: https://www.macrotrends.net/stocks/charts/PLTR/palantir/free-cash-flow-margin")
        print("   Check the most recent year's FCF Margin value")
        return True
    else:
        print("❌ FAILED - Scraper returned None")
        print("   Possible reasons:")
        print("   - Rate limiting (429 error)")
        print("   - URL structure changed")
        print("   - Need to check page structure")
        return False

if __name__ == "__main__":
    print("\n" + "="*50)
    print("MACROTRENDS FCF MARGIN TESTING")
    print("="*50)
    print("\nMake sure you can access Macrotrends")
    print("Check the values on the website before running tests.")
    print("\nStarting tests...\n")
    
    results = []
    results.append(("PLTR FCF Margin", test_macrotrends_fcf_margin_pltr()))
    
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
        print("Need to check URL or page structure")
    print("="*50 + "\n")

