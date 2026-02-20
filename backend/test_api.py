#!/usr/bin/env python3
"""
Test script for the backend API
Run this to verify your API is working locally
"""

import requests
import json

API_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint."""
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"✅ Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_chat():
    """Test chat endpoint."""
    print("\nTesting /chat endpoint...")
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={"message": "What is LangGraph?"},
            timeout=30
        )
        print(f"✅ Status: {response.status_code}")
        result = response.json()
        print(f"   Response: {result.get('response', '')[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Backend API Test")
    print("=" * 60)
    print(f"API URL: {API_URL}")
    print("\nMake sure your backend is running:")
    print("  uvicorn main:app --reload")
    print()
    
    health_ok = test_health()
    chat_ok = test_chat()
    
    print("\n" + "=" * 60)
    if health_ok and chat_ok:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed. Check your backend.")
    print("=" * 60)

