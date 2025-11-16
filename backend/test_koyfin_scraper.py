"""
Test script for Koyfin scraper.

This tests the scraper and compares results with the actual Koyfin website.
Run this to verify the scraper is working correctly.
"""

from app.scrapers.koyfin import KoyfinScraper

def test_koyfin_roic_pltr():
    """Test ROIC for PLTR."""
    print("\n" + "="*50)
    print("TEST: Koyfin ROIC for PLTR")
    print("="*50)
    
    scraper = KoyfinScraper()
    
    print("Fetching page...")
    value = scraper.get_roic("PLTR")
    print(f"Scraper returned: {value}")
    
    if value is not None:
        print(f"✅ PASSED - Got value: {value}%")
        print("   Please verify on: https://app.koyfin.com/company/PLTR/overview")
        print("   Check the ROIC value")
        return True
    else:
        print("❌ FAILED - Scraper returned None")
        print("   Possible reasons:")
        print("   - Rate limiting")
        print("   - URL structure changed")
        print("   - Need to check page structure")
        return False

def test_koyfin_roic_nvda():
    """Test ROIC for NVDA."""
    print("\n" + "="*50)
    print("TEST: Koyfin ROIC for NVDA")
    print("="*50)
    
    scraper = KoyfinScraper()
    
    print("Fetching page...")
    value = scraper.get_roic("NVDA")
    print(f"Scraper returned: {value}")
    
    if value is not None:
        print(f"✅ PASSED - Got value: {value}%")
        print("   Please verify on: https://app.koyfin.com/company/NVDA/overview")
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
    print("KOYFIN SCRAPER TESTING")
    print("="*50)
    print("\nMake sure you can access Koyfin")
    print("Check the values on the website before running tests.")
    print("\nStarting tests...\n")
    
    results = []
    results.append(("PLTR ROIC", test_koyfin_roic_pltr()))
    results.append(("NVDA ROIC", test_koyfin_roic_nvda()))
    
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
        print("\nNext step: Verify values match Koyfin website manually")
        print("Then integrate into API")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("Need to check URL or page structure")
    print("="*50 + "\n")

