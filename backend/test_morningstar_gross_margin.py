"""
Test script for Morningstar Gross Margin scraper.

This tests the scraper and compares results with the actual Morningstar website.
Run this to verify the scraper is working correctly.
"""

from app.scrapers.morningstar import MorningstarScraper

def test_morningstar_gross_margin_pltr():
    """Test Gross Margin for PLTR."""
    print("\n" + "="*50)
    print("TEST: Morningstar Gross Margin for PLTR")
    print("="*50)
    
    scraper = MorningstarScraper()
    
    print("Fetching page...")
    value = scraper.get_gross_margin("PLTR")
    print(f"Scraper returned: {value}")
    
    if value is not None:
        print(f"✅ PASSED - Got value: {value}%")
        print("   Please verify on: https://www.morningstar.com/stocks/xnas/PLTR/quote")
        print("   Check the Gross Margin value")
        return True
    else:
        print("❌ FAILED - Scraper returned None")
        print("   Possible reasons:")
        print("   - Rate limiting")
        print("   - URL structure changed")
        print("   - Need to check page structure")
        return False

def test_morningstar_gross_margin_nvda():
    """Test Gross Margin for NVDA."""
    print("\n" + "="*50)
    print("TEST: Morningstar Gross Margin for NVDA")
    print("="*50)
    
    scraper = MorningstarScraper()
    
    print("Fetching page...")
    value = scraper.get_gross_margin("NVDA")
    print(f"Scraper returned: {value}")
    
    if value is not None:
        print(f"✅ PASSED - Got value: {value}%")
        print("   Please verify on: https://www.morningstar.com/stocks/xnas/NVDA/quote")
        print("   Check the Gross Margin value")
        return True
    else:
        print("❌ FAILED - Scraper returned None")
        return False

if __name__ == "__main__":
    print("\n" + "="*50)
    print("MORNINGSTAR GROSS MARGIN TESTING")
    print("="*50)
    print("\nMake sure you can access Morningstar")
    print("Check the values on the website before running tests.")
    print("\nStarting tests...\n")
    
    results = []
    results.append(("PLTR Gross Margin", test_morningstar_gross_margin_pltr()))
    results.append(("NVDA Gross Margin", test_morningstar_gross_margin_nvda()))
    
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
        print("\nNext step: Verify values match Morningstar website manually")
        print("Then integrate into API")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("Need to check URL or page structure")
    print("="*50 + "\n")

