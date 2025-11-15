"""
Test script for Finviz scraper.

This tests the scraper and compares results with the actual Finviz website.
Run this to verify the scraper is working correctly.
"""

from app.scrapers.finviz import FinvizScraper

def test_gross_margin_pltr():
    """Test Gross Margin for PLTR."""
    print("\n" + "="*50)
    print("TEST: Finviz Gross Margin for PLTR")
    print("="*50)
    
    scraper = FinvizScraper()
    value = scraper.get_gross_margin("PLTR")
    
    print(f"Scraper returned: {value}")
    print(f"Expected: 80.81 (from Finviz website)")
    
    if value is not None:
        # Allow small tolerance for rounding
        if abs(value - 80.81) < 0.1:
            print("✅ PASSED - Value matches Finviz website")
            return True
        else:
            print(f"❌ FAILED - Value {value} does not match expected 80.81")
            print("   Please verify on: https://finviz.com/quote.ashx?t=PLTR")
            return False
    else:
        print("❌ FAILED - Scraper returned None")
        print("   Please check:")
        print("   1. Internet connection")
        print("   2. Finviz website is accessible")
        print("   3. HTML structure hasn't changed")
        return False

def test_gross_margin_nvda():
    """Test Gross Margin for NVDA."""
    print("\n" + "="*50)
    print("TEST: Finviz Gross Margin for NVDA")
    print("="*50)
    
    scraper = FinvizScraper()
    value = scraper.get_gross_margin("NVDA")
    
    print(f"Scraper returned: {value}")
    
    if value is not None:
        print(f"✅ PASSED - Got value: {value}%")
        print("   Please verify on: https://finviz.com/quote.ashx?t=NVDA")
        return True
    else:
        print("❌ FAILED - Scraper returned None")
        return False

if __name__ == "__main__":
    print("\n" + "="*50)
    print("FINVIZ SCRAPER TESTING")
    print("="*50)
    print("\nMake sure you can access: https://finviz.com/quote.ashx?t=PLTR")
    print("Check the Gross Margin value on the website before running tests.")
    print("\nPress Enter to start tests...")
    input()
    
    results = []
    results.append(("PLTR Gross Margin", test_gross_margin_pltr()))
    results.append(("NVDA Gross Margin", test_gross_margin_nvda()))
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    print("\n" + "="*50)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("\nNext step: Verify values match Finviz website manually")
        print("Then integrate into API")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("Fix scraper before integrating into API")
    print("="*50 + "\n")

