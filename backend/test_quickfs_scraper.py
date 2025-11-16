"""
Test script for QuickFS scraper.

This tests the scraper and compares results with the actual QuickFS website.
Run this to verify the scraper is working correctly.
"""

from app.scrapers.quickfs import QuickFSScraper

def test_quickfs_roic_pltr():
    """Test ROIC for PLTR."""
    print("\n" + "="*50)
    print("TEST: QuickFS ROIC for PLTR")
    print("="*50)
    
    scraper = QuickFSScraper()
    
    print("Fetching page...")
    value = scraper.get_roic("PLTR")
    print(f"Scraper returned: {value}")
    
    if value is not None:
        print(f"✅ PASSED - Got value: {value}%")
        print("   Please verify on: https://quickfs.net/company/PLTR")
        print("   Check the ROIC value")
        return True
    else:
        print("❌ FAILED - Scraper returned None")
        print("   Possible reasons:")
        print("   - Rate limiting")
        print("   - URL structure changed")
        print("   - Need to check page structure")
        return False

if __name__ == "__main__":
    print("\n" + "="*50)
    print("QUICKFS SCRAPER TESTING")
    print("="*50)
    print("\nMake sure you can access QuickFS")
    print("Check the values on the website before running tests.")
    print("\nStarting tests...\n")
    
    results = []
    results.append(("PLTR ROIC", test_quickfs_roic_pltr()))
    
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
        print("\nNext step: Verify values match QuickFS website manually")
        print("Then integrate into API")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("Need to check URL or page structure")
    print("="*50 + "\n")

