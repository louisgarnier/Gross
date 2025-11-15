"""
Test script for Phase 2 - API Contract & Mock Data.

This tests that the API is working and returning the correct data structure.
Run this after starting the backend server.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health check endpoint."""
    print("\n" + "="*50)
    print("TEST 1: Health Check")
    print("="*50)
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        if response.status_code == 200:
            print("✅ Health check PASSED")
            return True
        else:
            print("❌ Health check FAILED")
            return False
    except Exception as e:
        print(f"❌ Health check FAILED: {e}")
        print("   Make sure backend is running: uvicorn app.main:app --reload")
        return False

def test_pltr_api():
    """Test PLTR API endpoint."""
    print("\n" + "="*50)
    print("TEST 2: PLTR API Call")
    print("="*50)
    try:
        response = requests.get(f"{BASE_URL}/api/analyze/PLTR")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Ticker: {data.get('ticker')}")
        print(f"Overall Score: {data.get('overall_score')}/{data.get('max_score')}")
        print(f"Number of Ratios: {len(data.get('ratios', []))}")
        
        print("\nRatios:")
        for ratio in data.get('ratios', []):
            print(f"  - {ratio.get('metric')}: {ratio.get('consensus')} ({ratio.get('status')})")
        
        if response.status_code == 200 and data.get('ticker') == 'PLTR':
            print("\n✅ PLTR API call PASSED")
            return True
        else:
            print("\n❌ PLTR API call FAILED")
            return False
    except Exception as e:
        print(f"❌ PLTR API call FAILED: {e}")
        return False

def test_nvda_api():
    """Test NVDA API endpoint."""
    print("\n" + "="*50)
    print("TEST 3: NVDA API Call")
    print("="*50)
    try:
        response = requests.get(f"{BASE_URL}/api/analyze/NVDA")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Ticker: {data.get('ticker')}")
        print(f"Overall Score: {data.get('overall_score')}/{data.get('max_score')}")
        print(f"Number of Ratios: {len(data.get('ratios', []))}")
        
        print("\nRatios:")
        for ratio in data.get('ratios', []):
            print(f"  - {ratio.get('metric')}: {ratio.get('consensus')} ({ratio.get('status')})")
        
        if response.status_code == 200 and data.get('ticker') == 'NVDA':
            print("\n✅ NVDA API call PASSED")
            return True
        else:
            print("\n❌ NVDA API call FAILED")
            return False
    except Exception as e:
        print(f"❌ NVDA API call FAILED: {e}")
        return False

def test_data_structure():
    """Test that response matches the schema."""
    print("\n" + "="*50)
    print("TEST 4: Data Structure Validation")
    print("="*50)
    try:
        response = requests.get(f"{BASE_URL}/api/analyze/PLTR")
        data = response.json()
        
        # Check required fields
        required_fields = ['ticker', 'ratios', 'overall_score', 'max_score']
        missing = [field for field in required_fields if field not in data]
        
        if missing:
            print(f"❌ Missing required fields: {missing}")
            return False
        
        # Check ratios structure
        if not isinstance(data['ratios'], list) or len(data['ratios']) != 5:
            print(f"❌ Ratios should be a list of 5 items, got: {len(data.get('ratios', []))}")
            return False
        
        # Check each ratio has required fields
        for ratio in data['ratios']:
            ratio_fields = ['metric', 'values', 'consensus', 'target', 'status']
            missing = [field for field in ratio_fields if field not in ratio]
            if missing:
                print(f"❌ Ratio missing fields: {missing}")
                return False
        
        print("✅ Data structure is correct")
        return True
    except Exception as e:
        print(f"❌ Data structure validation FAILED: {e}")
        return False

def test_other_ticker():
    """Test API with another ticker (e.g., MSFT)."""
    print("\n" + "="*50)
    print("TEST 5: Other Ticker (MSFT)")
    print("="*50)
    try:
        response = requests.get(f"{BASE_URL}/api/analyze/MSFT")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Ticker: {data.get('ticker')}")
        print(f"Overall Score: {data.get('overall_score')}/{data.get('max_score')}")
        print(f"Number of Ratios: {len(data.get('ratios', []))}")
        
        if response.status_code == 200 and data.get('ticker') == 'MSFT':
            print("\n✅ MSFT API call PASSED")
            print("Note: Values are None until scrapers are built (this is expected)")
            return True
        else:
            print("\n❌ MSFT API call FAILED")
            return False
    except Exception as e:
        print(f"❌ MSFT API call FAILED: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*50)
    print("PHASE 2 API TESTING")
    print("="*50)
    print("\nMake sure backend is running:")
    print("  cd backend")
    print("  source venv/bin/activate")
    print("  uvicorn app.main:app --reload")
    print("\nPress Enter to start tests...")
    input()
    
    results = []
    results.append(("Health Check", test_health()))
    results.append(("PLTR API", test_pltr_api()))
    results.append(("NVDA API", test_nvda_api()))
    results.append(("Data Structure", test_data_structure()))
    results.append(("MSFT API", test_other_ticker()))
    
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
        print("🎉 ALL TESTS PASSED! Phase 2 API is working.")
    else:
        print("⚠️  SOME TESTS FAILED - Check errors above")
    print("="*50 + "\n")

