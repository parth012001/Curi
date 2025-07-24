#!/usr/bin/env python3
"""
Debug script for Best Buy API connection
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables from root directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

def test_bestbuy_api():
    """Test Best Buy API with various endpoints"""
    api_key = os.getenv('BESTBUY_API_KEY')
    print(f"🔑 API Key: {api_key[:10]}..." if api_key else "❌ No API key found")
    
    if not api_key:
        print("Please set BESTBUY_API_KEY in your .env file")
        return
    
    # Test 1: Simple health check
    print("\n🔍 Test 1: API Health Check")
    try:
        url = f"https://api.bestbuy.com/v1/products?apikey={api_key}&format=json&pageSize=1"
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Working! Found {data.get('total', 0)} total products")
        elif response.status_code == 403:
            print("❌ 403 Forbidden - Possible causes:")
            print("  - Invalid API key")
            print("  - Rate limiting exceeded")
            print("  - API key not approved for Best Buy API")
            print(f"  - Response: {response.text}")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    # Test 2: Simple search
    print("\n🔍 Test 2: Simple Product Search")
    try:
        # Simpler search without complex filters
        url = f"https://api.bestbuy.com/v1/products(search=laptop)?apikey={api_key}&format=json&pageSize=3"
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            print(f"✅ Search Working! Found {len(products)} laptops")
            
            if products:
                sample = products[0]
                print(f"Sample: {sample.get('name', 'N/A')}")
        else:
            print(f"❌ Search failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Search error: {e}")
    
    # Test 3: Categories endpoint (less restrictive)
    print("\n🔍 Test 3: Categories Endpoint")
    try:
        url = f"https://api.bestbuy.com/v1/categories?apikey={api_key}&format=json&pageSize=5"
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            categories = data.get('categories', [])
            print(f"✅ Categories Working! Found {len(categories)} categories")
        else:
            print(f"❌ Categories failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Categories error: {e}")
    
    # Test 4: Stores endpoint (basic access test)
    print("\n🔍 Test 4: Stores Endpoint")
    try:
        url = f"https://api.bestbuy.com/v1/stores?apikey={api_key}&format=json&pageSize=1"
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Stores endpoint accessible")
        else:
            print(f"❌ Stores failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Stores error: {e}")

if __name__ == "__main__":
    test_bestbuy_api()