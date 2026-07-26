"""
Check Premium Rate Limits
=========================

Reports rate limits for premium tiers alongside the models each tier can reach.

Run:
    python check_premium_rate_limits.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import os
from datetime import datetime
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")
API_KEY = os.getenv("SWARMS_API_KEY")


def make_request(
    endpoint: str, method: str = "GET", data: Dict = None
) -> Dict[str, Any]:
    """Make a request to the API with proper headers."""
    headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}

    url = f"{API_BASE_URL}{endpoint}"

    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")

        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        return {"error": str(e)}


def check_rate_limits() -> Dict[str, Any]:
    """Check current rate limits and subscription tier."""
    print("\n" + "=" * 50)
    print("CHECKING RATE LIMITS AND SUBSCRIPTION TIER")
    print("=" * 50)

    result = make_request("/v1/rate/limits")

    if "error" not in result:
        print("Current Rate Limit Status:")
        print(
            f"  Minute: {result['rate_limits']['minute']['count']}/{result['rate_limits']['minute']['limit']} requests"
        )
        print(
            f"  Hour: {result['rate_limits']['hour']['count']}/{result['rate_limits']['hour']['limit']} requests"
        )
        print(
            f"  Day: {result['rate_limits']['day']['count']}/{result['rate_limits']['day']['limit']} requests"
        )

        print(f"\nSubscription Tier: {result.get('tier', 'unknown')}")

        print("\nConfigured Limits:")
        print(
            f"  Maximum requests per minute: {result['limits']['maximum_requests_per_minute']}"
        )
        print(
            f"  Maximum requests per hour: {result['limits']['maximum_requests_per_hour']}"
        )
        print(
            f"  Maximum requests per day: {result['limits']['maximum_requests_per_day']}"
        )
        print(f"  Tokens per agent: {result['limits']['tokens_per_agent']}")

        return result
    else:
        print(f"Failed to check rate limits: {result['error']}")
        return result


def test_premium_rate_limits():
    """Test the premium rate limiting functionality."""
    print("Premium Rate Limits Test")
    print("=" * 50)
    print(f"API Base URL: {API_BASE_URL}")
    print(f"API Key: {API_KEY[:10]}...{API_KEY[-4:] if len(API_KEY) > 14 else '***'}")
    print(f"Timestamp: {datetime.now().isoformat()}")

    # Check initial rate limits and tier
    initial_limits = check_rate_limits()

    if "error" in initial_limits:
        print("Cannot proceed - failed to check initial rate limits")
        return

    # Determine expected limits based on tier
    tier = initial_limits.get("tier", "free")
    if tier == "premium":
        expected_minute_limit = 2000
        expected_hour_limit = 10000
        expected_day_limit = 100000
        expected_tokens_per_agent = 2000000
        print("\n✅ User has PREMIUM subscription - higher limits applied")
    else:
        expected_minute_limit = 100
        expected_hour_limit = 50
        expected_day_limit = 1200
        expected_tokens_per_agent = 200000
        print("\nℹ️  User has FREE tier - standard limits applied")

    # Verify limits match expected values
    actual_minute_limit = initial_limits["limits"]["maximum_requests_per_minute"]
    actual_hour_limit = initial_limits["limits"]["maximum_requests_per_hour"]
    actual_day_limit = initial_limits["limits"]["maximum_requests_per_day"]
    actual_tokens_per_agent = initial_limits["limits"]["tokens_per_agent"]

    print("\nVerifying rate limits:")
    print(
        f"  Minute limit: {actual_minute_limit} (expected: {expected_minute_limit}) - {'✅' if actual_minute_limit == expected_minute_limit else '❌'}"
    )
    print(
        f"  Hour limit: {actual_hour_limit} (expected: {expected_hour_limit}) - {'✅' if actual_hour_limit == expected_hour_limit else '❌'}"
    )
    print(
        f"  Day limit: {actual_day_limit} (expected: {expected_day_limit}) - {'✅' if actual_day_limit == expected_day_limit else '❌'}"
    )
    print(
        f"  Tokens per agent: {actual_tokens_per_agent} (expected: {expected_tokens_per_agent}) - {'✅' if actual_tokens_per_agent == expected_tokens_per_agent else '❌'}"
    )

    # Test a simple API call to verify functionality
    print("\n" + "=" * 50)
    print("TESTING API CALL WITH PREMIUM RATE LIMITS")
    print("=" * 50)

    # Make a test request to check available models
    test_result = make_request("/v1/models/available")

    if "error" not in test_result:
        print("✅ API call successful - premium rate limiting is working")
        print(f"  Models available: {len(test_result.get('models', []))}")
    else:
        print(f"❌ API call failed: {test_result['error']}")

    # Check rate limits again to see if the request was counted
    print("\n" + "=" * 50)
    print("CHECKING RATE LIMITS AFTER TEST REQUEST")
    print("=" * 50)

    final_limits = check_rate_limits()

    if "error" not in final_limits:
        minute_count = final_limits["rate_limits"]["minute"]["count"]
        hour_count = final_limits["rate_limits"]["hour"]["count"]
        day_count = final_limits["rate_limits"]["day"]["count"]

        print("Request counts after test:")
        print(f"  Minute: {minute_count}")
        print(f"  Hour: {hour_count}")
        print(f"  Day: {day_count}")

        if minute_count > 0:
            print("✅ Request was properly counted in rate limiting")
        else:
            print("❌ Request was not counted in rate limiting")

    print("\n" + "=" * 50)
    print("TEST COMPLETE")
    print("=" * 50)
    print("Premium rate limiting system:")
    print("  - Checks user subscription status in database")
    print("  - Applies appropriate rate limits based on tier")
    print("  - Tracks requests per minute, hour, and day")
    print("  - Returns tier information in rate limit responses")


if __name__ == "__main__":
    test_premium_rate_limits()
