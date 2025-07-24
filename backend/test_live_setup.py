#!/usr/bin/env python3
"""
Test script for live Best Buy integration
Run this to verify your setup is working correctly
"""

import asyncio
import os
import json
import time
from dotenv import load_dotenv
from live_data_processor import LiveDataProcessor
from data_sources import UnifiedDataSource

# Load environment variables from root directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

async def test_setup():
    """Comprehensive test of the live data setup"""
    print("🧪 Testing Curi Live Data Integration")
    print("=" * 50)
    
    # Check environment variables
    print("\n1️⃣ Checking Environment Variables...")
    bestbuy_key = os.getenv('BESTBUY_API_KEY')
    rapidapi_key = os.getenv('RAPIDAPI_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    if not bestbuy_key:
        print("❌ BESTBUY_API_KEY not found!")
        print("💡 Set it in your .env file: BESTBUY_API_KEY=your_key_here")
        return False
    else:
        print(f"✅ Best Buy API Key: {bestbuy_key[:10]}...")
    
    if rapidapi_key:
        print(f"✅ RapidAPI Key: {rapidapi_key[:10]}...")
    else:
        print("⚠️ RapidAPI Key not found (optional)")
    
    if openai_key:
        print(f"✅ OpenAI Key: {openai_key[:10]}...")
    else:
        print("⚠️ OpenAI Key not found (optional)")
    
    # Test Redis connection
    print("\n2️⃣ Testing Cache System...")
    try:
        import redis
        redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)
        redis_client.ping()
        print("✅ Redis connected and working")
    except Exception as e:
        print(f"⚠️ Redis not available: {e}")
        print("💡 Cache will use SQLite + File storage (slower but works)")
    
    # Test data source
    print("\n3️⃣ Testing Best Buy API Connection...")
    try:
        data_source = UnifiedDataSource(bestbuy_key, rapidapi_key)
        
        # Simple search test
        start_time = time.time()
        products = await data_source.search_products("laptop", limit=5)
        end_time = time.time()
        
        if products:
            print(f"✅ Best Buy API working! Found {len(products)} products in {end_time - start_time:.2f}s")
            
            # Show sample product
            sample = products[0]
            print(f"   Sample: {sample.title[:50]}... (${sample.price})")
        else:
            print("❌ No products returned from Best Buy API")
            return False
            
    except Exception as e:
        print(f"❌ Best Buy API test failed: {e}")
        print("💡 Check your API key and internet connection")
        return False
    
    # Test live data processor
    print("\n4️⃣ Testing Live Data Processor...")
    try:
        processor = LiveDataProcessor(bestbuy_key, rapidapi_key)
        
        # Initialize with live data
        print("   Initializing with live data...")
        await processor.initialize_with_live_data()
        
        # Test search
        print("   Testing product search...")
        results = await processor.search_products_live("gaming laptop", top_k=3)
        
        if results:
            print(f"✅ Live search working! Found {len(results)} gaming laptops")
            for i, product in enumerate(results, 1):
                print(f"   {i}. {product['title'][:40]}... (${product['price']})")
        else:
            print("⚠️ No search results returned")
        
        # Test performance stats
        stats = processor.get_performance_stats()
        print(f"   📊 Performance: {stats.get('cache_hit_rate', 0):.2%} cache hit rate")
        
    except Exception as e:
        print(f"❌ Live Data Processor test failed: {e}")
        return False
    
    # Test cache performance
    print("\n5️⃣ Testing Cache Performance...")
    try:
        # Run same search twice to test caching
        start_time = time.time()
        await processor.search_products_live("smartphone", top_k=5)
        first_search_time = time.time() - start_time
        
        start_time = time.time()
        await processor.search_products_live("smartphone", top_k=5)  # Should be cached
        cached_search_time = time.time() - start_time
        
        print(f"   First search: {first_search_time:.2f}s")
        print(f"   Cached search: {cached_search_time:.2f}s")
        
        if cached_search_time < first_search_time * 0.5:
            print("✅ Caching is working effectively!")
        else:
            print("⚠️ Caching may not be optimal")
            
    except Exception as e:
        print(f"⚠️ Cache performance test failed: {e}")
    
    # Summary
    print("\n🎉 Test Summary")
    print("=" * 50)
    print("✅ All core systems are working!")
    print("\n📋 Next Steps:")
    print("1. Start your backend: python main.py")
    print("2. Start your frontend: npm run dev")
    print("3. Test the chat interface")
    print("\n💡 Tips:")
    print("- Monitor cache hit rates with: curl localhost:8000/admin/cache/stats")
    print("- Refresh cache manually with: curl -X POST localhost:8000/admin/cache/refresh")
    print("- Check system status with: curl localhost:8000/admin/system/status")
    
    return True

async def test_rate_limiting():
    """Test rate limiting behavior"""
    print("\n🔧 Testing Rate Limiting...")
    
    bestbuy_key = os.getenv('BESTBUY_API_KEY')
    if not bestbuy_key:
        print("❌ Need BESTBUY_API_KEY for rate limiting test")
        return
    
    data_source = UnifiedDataSource(bestbuy_key)
    
    # Make multiple rapid requests
    start_time = time.time()
    tasks = []
    
    for i in range(10):
        task = data_source.search_products(f"test query {i}", limit=1)
        tasks.append(task)
    
    await asyncio.gather(*tasks)
    end_time = time.time()
    
    total_time = end_time - start_time
    rate = 10 / total_time
    
    print(f"   Made 10 requests in {total_time:.2f}s")
    print(f"   Effective rate: {rate:.2f} req/sec")
    
    if rate <= 5:
        print("✅ Rate limiting is working correctly")
    else:
        print("⚠️ Rate limiting may need adjustment")

if __name__ == "__main__":
    print("🚀 Starting Curi Live Data Integration Tests")
    
    try:
        # Run main test
        success = asyncio.run(test_setup())
        
        if success:
            # Run optional rate limiting test
            print("\n" + "=" * 50)
            choice = input("Run rate limiting test? (y/N): ").lower()
            if choice in ['y', 'yes']:
                asyncio.run(test_rate_limiting())
        
        print("\n✨ Testing complete!")
        
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        print("💡 Check the setup guide: LIVE_DATA_SETUP.md")