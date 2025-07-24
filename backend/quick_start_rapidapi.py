#!/usr/bin/env python3
"""
Quick start script using RapidAPI as primary data source
This gets you live data immediately while troubleshooting Best Buy API
"""

import os
import asyncio
from dotenv import load_dotenv

# Load environment variables from root directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

async def setup_rapidapi_primary():
    """Set up system to use RapidAPI as primary data source"""
    print("🚀 Setting up Curi with RapidAPI as primary data source")
    print("=" * 60)
    
    # Check for RapidAPI key
    rapidapi_key = os.getenv('RAPIDAPI_KEY')
    
    if not rapidapi_key:
        print("❌ RapidAPI key not found!")
        print("\n💡 To get live data immediately:")
        print("1. Go to https://rapidapi.com/")
        print("2. Sign up for free account")
        print("3. Subscribe to these APIs (free tiers available):")
        print("   - Walmart API")
        print("   - Amazon API")
        print("   - Target API")
        print("4. Add RAPIDAPI_KEY to your .env file")
        print("\n📝 Example .env addition:")
        print("RAPIDAPI_KEY=your_rapidapi_key_here")
        return False
    
    print(f"✅ RapidAPI Key found: {rapidapi_key[:10]}...")
    
    # Test RapidAPI connection (simplified)
    print("\n🔍 Testing RapidAPI connection...")
    
    try:
        # Import and test the data source
        from data_sources import RapidAPIDataSource
        from cache_manager import CacheManager
        
        cache = CacheManager()
        rapidapi_source = RapidAPIDataSource(rapidapi_key, cache)
        
        # Test with a simple search
        async with rapidapi_source as source:
            products = await source.search_products("laptop", limit=5)
            
        if products:
            print(f"✅ RapidAPI working! Found {len(products)} products")
            print("Sample products:")
            for i, product in enumerate(products[:3], 1):
                print(f"  {i}. {product.title[:50]}... (${product.price})")
            return True
        else:
            print("⚠️ No products returned from RapidAPI")
            return False
            
    except Exception as e:
        print(f"❌ RapidAPI test failed: {e}")
        print("\n💡 This usually means:")
        print("1. Invalid API key")
        print("2. Need to subscribe to product APIs on RapidAPI")
        print("3. Rate limits exceeded")
        return False

async def test_system_with_rapidapi():
    """Test the full system with RapidAPI only"""
    print("\n🧪 Testing Full System with RapidAPI")
    print("=" * 40)
    
    try:
        from live_data_processor import LiveDataProcessor
        
        # Initialize with empty Best Buy key (will use RapidAPI only)
        rapidapi_key = os.getenv('RAPIDAPI_KEY')
        processor = LiveDataProcessor(bestbuy_api_key="", rapidapi_key=rapidapi_key)
        
        # Initialize with live data
        print("📦 Initializing with RapidAPI data...")
        await processor.initialize_with_live_data()
        
        # Test search
        print("🔍 Testing product search...")
        results = await processor.search_products_live("laptop", top_k=3)
        
        if results:
            print(f"✅ System working! Found {len(results)} laptops")
            for i, product in enumerate(results, 1):
                print(f"  {i}. {product['title'][:40]}... (${product['price']})")
        else:
            print("⚠️ No search results")
        
        # Get performance stats
        stats = processor.get_performance_stats()
        print(f"\n📊 Performance Stats:")
        print(f"  - RapidAPI calls: {stats.get('rapidapi_calls', 0)}")
        print(f"  - Cache hit rate: {stats.get('cache_hit_rate', 0):.1%}")
        print(f"  - Products cached: {stats.get('products_cached', 0)}")
        
        return True
        
    except Exception as e:
        print(f"❌ System test failed: {e}")
        return False

async def create_rapidapi_config():
    """Create configuration for RapidAPI-first setup"""
    print("\n⚙️ Creating RapidAPI-First Configuration")
    print("=" * 45)
    
    config = {
        "primary_source": "rapidapi",
        "fallback_source": "cache",
        "bestbuy_enabled": False,
        "cache_strategy": "aggressive",
        "prefetch_categories": [
            "laptop", "smartphone", "headphones", "tablet", 
            "smartwatch", "gaming", "camera", "speaker"
        ]
    }
    
    print("✅ Configuration created:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    return config

def show_next_steps():
    """Show next steps for the user"""
    print("\n🎯 Next Steps to Get Live")
    print("=" * 30)
    print("1. Set up RapidAPI key (if not done):")
    print("   - Go to https://rapidapi.com/")
    print("   - Subscribe to Walmart/Amazon/Target APIs")
    print("   - Add RAPIDAPI_KEY to .env")
    print()
    print("2. Start your backend:")
    print("   cd backend")
    print("   python main.py")
    print()
    print("3. Start your frontend:")
    print("   cd frontend")
    print("   npm run dev")
    print()
    print("4. Test the system:")
    print("   curl 'http://localhost:8000/products/search?query=laptop&limit=5'")
    print()
    print("5. Monitor performance:")
    print("   curl 'http://localhost:8000/admin/cache/stats'")
    print()
    print("🔧 Meanwhile, troubleshoot Best Buy API:")
    print("   - Check developer account for API key approval")
    print("   - Contact developer@bestbuy.com if needed")
    print("   - See BESTBUY_API_TROUBLESHOOTING.md for details")

async def main():
    """Main setup function"""
    try:
        # Test RapidAPI
        rapidapi_success = await setup_rapidapi_primary()
        
        if rapidapi_success:
            # Test full system
            system_success = await test_system_with_rapidapi()
            
            if system_success:
                # Create config
                await create_rapidapi_config()
                print("\n🎉 SUCCESS! Your system is ready with live data!")
            else:
                print("\n⚠️ RapidAPI works but system integration needs work")
        else:
            print("\n💡 Setting up with enhanced static data as fallback...")
            print("Your system will work with cached/static data while you set up live APIs")
        
        # Always show next steps
        show_next_steps()
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print("📖 Check the troubleshooting guide: BESTBUY_API_TROUBLESHOOTING.md")

if __name__ == "__main__":
    asyncio.run(main())