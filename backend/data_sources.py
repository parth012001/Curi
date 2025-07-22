"""
Multi-source data integration system for live product data
Combines Best Buy API with multiple fallback sources to ensure reliability
"""

import requests
import time
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import os
from cache_manager import CacheManager

@dataclass
class ProductData:
    """Standardized product data structure"""
    sku: str
    title: str
    brand: str
    price: float
    sale_price: Optional[float]
    category: str
    description: str
    rating: float
    review_count: int
    availability: str
    images: List[str]
    specifications: Dict[str, Any]
    url: str
    source: str  # 'bestbuy', 'rapidapi', 'backup'
    last_updated: datetime

class RateLimiter:
    """Smart rate limiter with burst capacity and backoff"""
    
    def __init__(self, max_requests: int = 5, time_window: int = 1, burst_capacity: int = 10):
        self.max_requests = max_requests
        self.time_window = time_window
        self.burst_capacity = burst_capacity
        self.requests = []
        self.burst_count = 0
        self.last_reset = time.time()
    
    async def acquire(self):
        """Acquire permission to make a request"""
        now = time.time()
        
        # Reset burst capacity every minute
        if now - self.last_reset > 60:
            self.burst_count = 0
            self.last_reset = now
        
        # Remove old requests outside time window
        self.requests = [req_time for req_time in self.requests if now - req_time < self.time_window]
        
        # Check if we can make a request
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return
        
        # Check burst capacity
        if self.burst_count < self.burst_capacity:
            wait_time = self.time_window - (now - self.requests[0]) + 0.1
            if wait_time > 0:
                await asyncio.sleep(wait_time)
            self.burst_count += 1
            self.requests.append(time.time())
            return
        
        # Calculate wait time
        wait_time = self.time_window - (now - self.requests[0]) + 0.1
        if wait_time > 0:
            await asyncio.sleep(wait_time)
        
        self.requests.append(time.time())

class BestBuyAPI:
    """Best Buy API integration with smart rate limiting"""
    
    def __init__(self, api_key: str, cache_manager: CacheManager):
        self.api_key = api_key
        self.base_url = "https://api.bestbuy.com/v1"
        self.cache = cache_manager
        self.rate_limiter = RateLimiter(max_requests=4, time_window=1)  # Conservative: 4/sec
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def search_products(self, query: str, limit: int = 50) -> List[ProductData]:
        """Search products with caching and rate limiting"""
        cache_key = f"search_{query}_{limit}"
        
        # Try cache first
        cached_data = self.cache.get('search_results', cache_key)
        if cached_data:
            return [ProductData(**item) for item in cached_data]
        
        await self.rate_limiter.acquire()
        
        try:
            # Build search URL with filters for electronics/tech products
            params = {
                'apikey': self.api_key,
                'format': 'json',
                'q': query,
                'limit': limit,
                'sort': 'customerReviewAverage.dsc',
                'facet': 'customerReviewAverage,gt,3.5',  # Only products with good ratings
                'show': 'sku,name,regularPrice,salePrice,categoryPath,longDescription,customerReviewAverage,customerReviewCount,image,url,manufacturer,details'
            }
            
            url = f"{self.base_url}/products"
            
            async with self.session.get(url, params=params) as response:
                if response.status == 429:
                    # Rate limited - wait and retry
                    await asyncio.sleep(2)
                    return await self.search_products(query, limit)
                
                response.raise_for_status()
                data = await response.json()
                
                products = []
                for item in data.get('products', []):
                    try:
                        product = self._parse_bestbuy_product(item)
                        products.append(product)
                    except Exception as e:
                        print(f"Error parsing product: {e}")
                        continue
                
                # Cache the results
                cache_data = [product.__dict__ for product in products]
                for product in cache_data:
                    product['last_updated'] = product['last_updated'].isoformat()
                
                self.cache.set('search_results', cache_key, cache_data)
                
                return products
        
        except Exception as e:
            print(f"Best Buy API error: {e}")
            return []
    
    async def get_product_details(self, sku: str) -> Optional[ProductData]:
        """Get detailed product information"""
        # Try cache first
        cached_data = self.cache.get('product_details', sku)
        if cached_data:
            cached_data['last_updated'] = datetime.fromisoformat(cached_data['last_updated'])
            return ProductData(**cached_data)
        
        await self.rate_limiter.acquire()
        
        try:
            params = {
                'apikey': self.api_key,
                'format': 'json',
                'show': 'all'
            }
            
            url = f"{self.base_url}/products/{sku}"
            
            async with self.session.get(url, params=params) as response:
                if response.status == 404:
                    return None
                
                if response.status == 429:
                    await asyncio.sleep(2)
                    return await self.get_product_details(sku)
                
                response.raise_for_status()
                data = await response.json()
                
                product = self._parse_bestbuy_product(data)
                
                # Cache the result
                cache_data = product.__dict__.copy()
                cache_data['last_updated'] = cache_data['last_updated'].isoformat()
                self.cache.set('product_details', sku, cache_data)
                
                return product
        
        except Exception as e:
            print(f"Error getting product details: {e}")
            return None
    
    def _parse_bestbuy_product(self, item: Dict) -> ProductData:
        """Parse Best Buy API response to standardized format"""
        return ProductData(
            sku=str(item.get('sku', '')),
            title=item.get('name', ''),
            brand=item.get('manufacturer', ''),
            price=float(item.get('regularPrice', 0)),
            sale_price=float(item.get('salePrice', 0)) if item.get('salePrice') else None,
            category=item.get('categoryPath', [])[-1]['name'] if item.get('categoryPath') else '',
            description=item.get('longDescription', ''),
            rating=float(item.get('customerReviewAverage', 0)),
            review_count=int(item.get('customerReviewCount', 0)),
            availability=item.get('onlineAvailability', False),
            images=[item.get('image', '')] if item.get('image') else [],
            specifications=item.get('details', {}),
            url=item.get('url', ''),
            source='bestbuy',
            last_updated=datetime.now()
        )

class RapidAPIDataSource:
    """RapidAPI fallback data sources"""
    
    def __init__(self, api_key: str, cache_manager: CacheManager):
        self.api_key = api_key
        self.cache = cache_manager
        self.rate_limiter = RateLimiter(max_requests=10, time_window=1)
        self.session = None
        
        # Multiple RapidAPI endpoints for redundancy
        self.endpoints = [
            {
                'name': 'walmart_api',
                'url': 'https://walmart-api-by-speedapi.p.rapidapi.com',
                'search_path': '/products/search'
            },
            {
                'name': 'amazon_api',
                'url': 'https://amazon-api-by-speedapi.p.rapidapi.com',
                'search_path': '/search'
            },
            {
                'name': 'target_api',
                'url': 'https://target-api-by-speedapi.p.rapidapi.com',
                'search_path': '/search'
            }
        ]
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def search_products(self, query: str, limit: int = 20) -> List[ProductData]:
        """Search products across multiple RapidAPI sources"""
        all_products = []
        
        for endpoint in self.endpoints:
            try:
                products = await self._search_endpoint(endpoint, query, limit // len(self.endpoints))
                all_products.extend(products)
            except Exception as e:
                print(f"RapidAPI {endpoint['name']} error: {e}")
                continue
        
        return all_products[:limit]
    
    async def _search_endpoint(self, endpoint: Dict, query: str, limit: int) -> List[ProductData]:
        """Search a specific RapidAPI endpoint"""
        cache_key = f"{endpoint['name']}_{query}_{limit}"
        
        # Try cache first
        cached_data = self.cache.get('rapidapi_search', cache_key)
        if cached_data:
            return [ProductData(**item) for item in cached_data]
        
        await self.rate_limiter.acquire()
        
        headers = {
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': endpoint['url'].split('//')[1]
        }
        
        params = {
            'query': query,
            'limit': limit
        }
        
        try:
            url = f"{endpoint['url']}{endpoint['search_path']}"
            async with self.session.get(url, headers=headers, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                
                products = self._parse_rapidapi_response(data, endpoint['name'])
                
                # Cache results
                cache_data = [product.__dict__ for product in products]
                for product in cache_data:
                    product['last_updated'] = product['last_updated'].isoformat()
                
                self.cache.set('rapidapi_search', cache_key, cache_data)
                
                return products
        
        except Exception as e:
            print(f"RapidAPI endpoint {endpoint['name']} error: {e}")
            return []
    
    def _parse_rapidapi_response(self, data: Dict, source: str) -> List[ProductData]:
        """Parse RapidAPI response to standardized format"""
        products = []
        items = data.get('results', data.get('products', data.get('items', [])))
        
        for item in items:
            try:
                product = ProductData(
                    sku=str(item.get('id', item.get('asin', item.get('sku', '')))),
                    title=item.get('title', item.get('name', '')),
                    brand=item.get('brand', item.get('manufacturer', '')),
                    price=float(item.get('price', item.get('regularPrice', 0))),
                    sale_price=float(item.get('salePrice', 0)) if item.get('salePrice') else None,
                    category=item.get('category', ''),
                    description=item.get('description', ''),
                    rating=float(item.get('rating', item.get('averageRating', 0))),
                    review_count=int(item.get('reviewCount', item.get('ratingsTotal', 0))),
                    availability=item.get('availability', True),
                    images=item.get('images', [item.get('image')] if item.get('image') else []),
                    specifications=item.get('specifications', {}),
                    url=item.get('url', ''),
                    source=f'rapidapi_{source}',
                    last_updated=datetime.now()
                )
                products.append(product)
            except Exception as e:
                print(f"Error parsing RapidAPI item: {e}")
                continue
        
        return products

class UnifiedDataSource:
    """Unified data source that combines Best Buy + RapidAPI + caching"""
    
    def __init__(self, bestbuy_api_key: str, rapidapi_key: str = None):
        self.cache = CacheManager()
        self.bestbuy_api_key = bestbuy_api_key
        self.rapidapi_key = rapidapi_key
        
        # Performance tracking
        self.stats = {
            'bestbuy_calls': 0,
            'rapidapi_calls': 0,
            'cache_hits': 0,
            'total_requests': 0
        }
    
    async def search_products(self, query: str, limit: int = 50) -> List[ProductData]:
        """Unified product search with fallback sources"""
        self.stats['total_requests'] += 1
        all_products = []
        
        # Primary: Best Buy API
        try:
            async with BestBuyAPI(self.bestbuy_api_key, self.cache) as bestbuy:
                bestbuy_products = await bestbuy.search_products(query, limit)
                all_products.extend(bestbuy_products)
                self.stats['bestbuy_calls'] += 1
                print(f"✅ Best Buy API: Found {len(bestbuy_products)} products")
        except Exception as e:
            print(f"⚠️ Best Buy API failed: {e}")
        
        # Fallback: RapidAPI sources (if we didn't get enough results)
        if len(all_products) < limit and self.rapidapi_key:
            try:
                async with RapidAPIDataSource(self.rapidapi_key, self.cache) as rapidapi:
                    rapidapi_products = await rapidapi.search_products(query, limit - len(all_products))
                    all_products.extend(rapidapi_products)
                    self.stats['rapidapi_calls'] += 1
                    print(f"✅ RapidAPI: Found {len(rapidapi_products)} products")
            except Exception as e:
                print(f"⚠️ RapidAPI failed: {e}")
        
        # Remove duplicates and sort by relevance
        unique_products = self._deduplicate_products(all_products)
        
        return unique_products[:limit]
    
    async def get_product_details(self, sku: str, source: str = 'bestbuy') -> Optional[ProductData]:
        """Get detailed product information"""
        if source == 'bestbuy':
            async with BestBuyAPI(self.bestbuy_api_key, self.cache) as bestbuy:
                return await bestbuy.get_product_details(sku)
        
        # Add RapidAPI product details if needed
        return None
    
    def _deduplicate_products(self, products: List[ProductData]) -> List[ProductData]:
        """Remove duplicate products based on title similarity"""
        seen_titles = set()
        unique_products = []
        
        for product in products:
            # Simple deduplication by title (you could make this more sophisticated)
            title_key = product.title.lower().replace(' ', '')[:50]
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_products.append(product)
        
        # Sort by rating and review count
        unique_products.sort(key=lambda p: (p.rating * p.review_count), reverse=True)
        
        return unique_products
    
    def get_performance_stats(self) -> Dict:
        """Get performance statistics"""
        cache_stats = self.cache.get_cache_stats()
        
        return {
            **self.stats,
            **cache_stats,
            'cache_hit_rate': self.stats['cache_hits'] / max(self.stats['total_requests'], 1)
        }
    
    def cleanup_cache(self) -> int:
        """Clean up expired cache entries"""
        return self.cache.cleanup_expired()

# Example usage and testing
async def test_data_sources():
    """Test the unified data source system"""
    # You'll need to set these environment variables
    bestbuy_key = os.getenv('BESTBUY_API_KEY')
    rapidapi_key = os.getenv('RAPIDAPI_KEY')
    
    if not bestbuy_key:
        print("⚠️ BESTBUY_API_KEY not found in environment")
        return
    
    unified_source = UnifiedDataSource(bestbuy_key, rapidapi_key)
    
    # Test search
    print("🔍 Testing product search...")
    products = await unified_source.search_products("laptop", limit=10)
    
    print(f"Found {len(products)} products:")
    for product in products[:3]:
        print(f"- {product.title} (${product.price}) - {product.source}")
    
    # Performance stats
    stats = unified_source.get_performance_stats()
    print(f"\nPerformance Stats: {stats}")

if __name__ == "__main__":
    asyncio.run(test_data_sources())