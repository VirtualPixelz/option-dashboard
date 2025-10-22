#!/usr/bin/env python3
"""
Detailed Tradier API test with comprehensive error reporting
"""

import os
import requests
import json

TRADIER_API_KEY = os.environ.get('TRADIER_API_KEY')

def test_api_detailed():
    """Test with detailed error reporting"""
    print("="*70)
    print("DETAILED TRADIER API TEST")
    print("="*70)
    print(f"API Key (first 15 chars): {TRADIER_API_KEY[:15]}...")
    print(f"API Key length: {len(TRADIER_API_KEY)}")
    print()

    # Test both sandbox and production URLs
    endpoints = [
        ("Sandbox User Profile", "https://sandbox.tradier.com/v1/user/profile"),
        ("Sandbox Market Data", "https://sandbox.tradier.com/v1/markets/quotes?symbols=SPY"),
        ("Production User Profile", "https://api.tradier.com/v1/user/profile"),
    ]

    for name, url in endpoints:
        print(f"\n{'='*70}")
        print(f"Testing: {name}")
        print(f"URL: {url}")
        print('-'*70)

        headers = {
            'Authorization': f'Bearer {TRADIER_API_KEY}',
            'Accept': 'application/json'
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)

            print(f"Status Code: {response.status_code}")
            print(f"Response Headers:")
            for key, value in response.headers.items():
                if key.lower() in ['content-type', 'x-ratelimit-limit', 'x-ratelimit-remaining', 'x-ratelimit-reset']:
                    print(f"  {key}: {value}")

            print(f"\nResponse Body:")
            try:
                data = response.json()
                print(json.dumps(data, indent=2))
            except:
                print(response.text)

            if response.status_code == 200:
                print(f"\n✓ SUCCESS")
            elif response.status_code == 401:
                print(f"\n✗ AUTHENTICATION FAILED - Invalid API key")
            elif response.status_code == 403:
                print(f"\n✗ FORBIDDEN - API key lacks permission for this endpoint")
            else:
                print(f"\n✗ FAILED")

        except requests.exceptions.Timeout:
            print("✗ ERROR: Request timed out")
        except requests.exceptions.RequestException as e:
            print(f"✗ ERROR: {str(e)}")
        except Exception as e:
            print(f"✗ UNEXPECTED ERROR: {str(e)}")

    # Additional diagnostics
    print("\n" + "="*70)
    print("DIAGNOSTICS")
    print("="*70)
    print(f"API Key format check:")
    print(f"  - Length: {len(TRADIER_API_KEY)} characters")
    print(f"  - Contains only alphanumeric: {TRADIER_API_KEY.isalnum()}")
    print(f"  - First char: {TRADIER_API_KEY[0]}")
    print(f"  - Last char: {TRADIER_API_KEY[-1]}")

    print("\nRecommendations:")
    print("1. Verify the API key is from Tradier's Sandbox (not production)")
    print("2. Check if the sandbox account is properly activated")
    print("3. Ensure the API key has market data permissions enabled")
    print("4. Try regenerating the API key in the Tradier dashboard")
    print("\nTradier Sandbox Dashboard: https://developer.tradier.com/user/sign_in")

if __name__ == "__main__":
    test_api_detailed()
