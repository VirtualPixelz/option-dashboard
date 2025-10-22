#!/usr/bin/env python3
"""
Test script for Tradier API access
Tests sandbox API connectivity and basic endpoints
"""

import os
import requests
import json
from datetime import datetime

# Tradier API Configuration
TRADIER_API_KEY = os.environ.get('TRADIER_API_KEY')
SANDBOX_BASE_URL = 'https://sandbox.tradier.com/v1'

def test_user_profile():
    """Test user profile endpoint"""
    print("\n" + "="*60)
    print("Testing User Profile Endpoint")
    print("="*60)

    url = f"{SANDBOX_BASE_URL}/user/profile"
    headers = {
        'Authorization': f'Bearer {TRADIER_API_KEY}',
        'Accept': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("✓ SUCCESS: User profile retrieved")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"✗ FAILED: {response.text}")
            return False
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        return False

def test_market_quotes():
    """Test market quotes endpoint"""
    print("\n" + "="*60)
    print("Testing Market Quotes Endpoint (SPY)")
    print("="*60)

    url = f"{SANDBOX_BASE_URL}/markets/quotes"
    headers = {
        'Authorization': f'Bearer {TRADIER_API_KEY}',
        'Accept': 'application/json'
    }
    params = {
        'symbols': 'SPY,AAPL'
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("✓ SUCCESS: Market quotes retrieved")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"✗ FAILED: {response.text}")
            return False
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        return False

def test_options_chains():
    """Test options chains endpoint"""
    print("\n" + "="*60)
    print("Testing Options Chains Endpoint (SPY)")
    print("="*60)

    url = f"{SANDBOX_BASE_URL}/markets/options/chains"
    headers = {
        'Authorization': f'Bearer {TRADIER_API_KEY}',
        'Accept': 'application/json'
    }
    params = {
        'symbol': 'SPY',
        'expiration': '2024-12-31'  # You may need to adjust this date
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("✓ SUCCESS: Options chain retrieved")
            # Limit output for readability
            if 'options' in data and 'option' in data['options']:
                options = data['options']['option']
                print(f"Found {len(options) if isinstance(options, list) else 1} options")
                print("First 3 options:")
                if isinstance(options, list):
                    print(json.dumps(options[:3], indent=2))
                else:
                    print(json.dumps(options, indent=2))
            else:
                print(json.dumps(data, indent=2))
            return True
        else:
            print(f"✗ FAILED: {response.text}")
            return False
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        return False

def test_options_expirations():
    """Test options expirations endpoint"""
    print("\n" + "="*60)
    print("Testing Options Expirations Endpoint (SPY)")
    print("="*60)

    url = f"{SANDBOX_BASE_URL}/markets/options/expirations"
    headers = {
        'Authorization': f'Bearer {TRADIER_API_KEY}',
        'Accept': 'application/json'
    }
    params = {
        'symbol': 'SPY'
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("✓ SUCCESS: Options expirations retrieved")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"✗ FAILED: {response.text}")
            return False
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        return False

def main():
    """Run all API tests"""
    print("\n" + "="*60)
    print("TRADIER API SANDBOX TEST")
    print("="*60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Key: {TRADIER_API_KEY[:10]}..." if TRADIER_API_KEY else "API Key: NOT FOUND")
    print(f"Base URL: {SANDBOX_BASE_URL}")

    if not TRADIER_API_KEY:
        print("\n✗ ERROR: TRADIER_API_KEY environment variable not set")
        return

    results = []

    # Run all tests
    results.append(("User Profile", test_user_profile()))
    results.append(("Market Quotes", test_market_quotes()))
    results.append(("Options Expirations", test_options_expirations()))
    results.append(("Options Chains", test_options_chains()))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! Tradier API access is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the output above for details.")

if __name__ == "__main__":
    main()
