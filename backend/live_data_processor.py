"""
Live Data Processor - Integration with existing Curi system
Replaces static data loading with live Best Buy API + caching
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import asyncio
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json

from data_sources import UnifiedDataSource, ProductData
from cache_manager import CacheManager

class LiveDataProcessor:
    """
    Enhanced data processor that combines live API data with your existing
    recommendation algorithms and NLP processing
    """
    
    def __init__(self, bestbuy_api_key: str, rapidapi_key: str = None):
        # Initialize data sources
        self.data_source = UnifiedDataSource(bestbuy_api_key, rapidapi_key)
        self.cache = CacheManager()
        
        # Initialize existing components
        self.products_df = None
        self.reviews_df = None
        self.ratings_df = None
        self.product_similarity_matrix = None
        self.tfidf_matrix = None
        self.tfidf_vectorizer = None
        
        # Live data management
        self.last_update = None
        self.update_interval = timedelta(hours=6)  # Refresh every 6 hours
        self.popular_queries = [
            "laptop", "phone", "headphones", "tablet", "smartwatch", 
            "gaming", "camera", "speaker", "tv", "fitness tracker"
        ]
        
        # Initialize with some cached data if available
        self._load_cached_base_data()
    
    async def initialize_with_live_data(self, force_refresh: bool = False):
        """Initialize system with live data from Best Buy API"""
        if not force_refresh and self.last_update and (datetime.now() - self.last_update) < self.update_interval:
            print("📊 Using cached data (still fresh)")
            return
        
        print("🔄 Initializing with live Best Buy data...")
        
        # Pre-populate cache with popular categories
        await self._prefetch_popular_categories()
        
        # Build product dataframe from cached data
        await self._build_dataframes_from_cache()
        
        # Create features and similarity matrices
        self._create_product_features()
        self._build_tfidf_matrix()
        
        self.last_update = datetime.now()
        print("✅ Live data initialization complete!")
    
    async def _prefetch_popular_categories(self):
        """Pre-fetch popular product categories to build base dataset"""
        print("📦 Pre-fetching popular product categories...")
        
        all_products = []
        for query in self.popular_queries:
            try:
                products = await self.data_source.search_products(query, limit=100)
                all_products.extend(products)
                print(f"  ✅ {query}: {len(products)} products")
            except Exception as e:
                print(f"  ⚠️ {query}: Error - {e}")
        
        print(f"📊 Pre-fetched {len(all_products)} total products")
        return all_products
    
    async def _build_dataframes_from_cache(self):
        """Build pandas dataframes from cached product data"""
        print("🏗️ Building dataframes from cached data...")
        
        # Get all cached products
        cached_products = self._get_all_cached_products()
        
        if not cached_products:
            print("⚠️ No cached products found, using minimal dataset")
            self.products_df = pd.DataFrame()
            self.reviews_df = pd.DataFrame()
            self.ratings_df = pd.DataFrame()
            return
        
        # Convert to pandas DataFrame
        products_data = []
        reviews_data = []
        
        for product in cached_products:
            # Product data
            product_dict = {
                'parent_asin': product.sku,
                'asin': product.sku,
                'title': product.title,
                'store': product.brand,
                'main_category': product.category,
                'average_rating': product.rating,
                'rating_number': product.review_count,
                'price': product.price,
                'description': product.description,
                'image': product.images[0] if product.images else '',
                'url': product.url,
                'source': product.source,
                'last_updated': product.last_updated
            }
            products_data.append(product_dict)
            
            # Generate synthetic review data for compatibility
            if product.review_count > 0:
                review_dict = {
                    'asin': product.sku,
                    'parent_asin': product.sku,
                    'user_id': f'user_{product.sku}',
                    'rating': product.rating,
                    'text': product.description[:500] if product.description else 'Great product!',
                    'title': f'Review for {product.title[:50]}',
                    'timestamp': product.last_updated,
                    'helpful_vote': 0,
                    'verified_purchase': True,
                    'product_title': product.title,
                    'store': product.brand,
                    'main_category': product.category
                }
                reviews_data.append(review_dict)
        
        self.products_df = pd.DataFrame(products_data)
        self.reviews_df = pd.DataFrame(reviews_data)
        
        # Create ratings dataframe
        if not self.reviews_df.empty:
            self.ratings_df = self.reviews_df[['user_id', 'asin', 'rating', 'timestamp']].copy()
            self.ratings_df.columns = ['UserId', 'ProductId', 'Rating', 'Timestamp']
        else:
            self.ratings_df = pd.DataFrame(columns=['UserId', 'ProductId', 'Rating', 'Timestamp'])
        
        print(f"📊 Built dataframes: {len(self.products_df)} products, {len(self.reviews_df)} reviews")
    
    def _get_all_cached_products(self) -> List[ProductData]:
        """Retrieve all cached products from cache storage"""
        cached_products = []
        
        # This is a simplified approach - in production you might want to
        # maintain an index of all cached product keys
        try:
            # Get cached search results for popular queries
            for query in self.popular_queries:
                for limit in [50, 100]:
                    cache_key = f"search_{query}_{limit}"
                    cached_data = self.cache.get('search_results', cache_key)
                    
                    if cached_data:
                        for item in cached_data:
                            item['last_updated'] = datetime.fromisoformat(item['last_updated'])
                            cached_products.append(ProductData(**item))
        except Exception as e:
            print(f"Error retrieving cached products: {e}")
        
        # Remove duplicates
        seen_skus = set()
        unique_products = []
        for product in cached_products:
            if product.sku not in seen_skus:
                seen_skus.add(product.sku)
                unique_products.append(product)
        
        return unique_products
    
    def _load_cached_base_data(self):
        """Load any existing cached base data"""
        try:
            # Try to load from cache
            cached_df = self.cache.get('processed_data', 'products_df')
            if cached_df:
                self.products_df = pd.DataFrame(cached_df)
                print("📂 Loaded cached products dataframe")
        except Exception as e:
            print(f"No cached base data found: {e}")
    
    async def search_products_live(self, query: str, top_k: int = 50) -> List[Dict]:
        """Search products using live API with intelligent caching"""
        try:
            # Get live results
            products = await self.data_source.search_products(query, limit=top_k)
            
            # Convert to format expected by existing system
            results = []
            for product in products:
                result = {
                    'asin': product.sku,
                    'title': product.title,
                    'store': product.brand,
                    'main_category': product.category,
                    'average_rating': product.rating,
                    'rating_number': product.review_count,
                    'price': product.price,
                    'similarity_score': 1.0,  # Live results get high relevance
                    'description': product.description,
                    'source': product.source,
                    'url': product.url,
                    'images': product.images
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            print(f"Live search error: {e}")
            # Fallback to cached/existing search
            return self.search_products_fallback(query, top_k)
    
    def search_products_fallback(self, query: str, top_k: int = 50) -> List[Dict]:
        """Fallback search using cached data and existing algorithms"""
        if self.products_df is None or self.products_df.empty:
            return []
        
        # Use existing TF-IDF search on cached data
        return self._tfidf_search(query, top_k)
    
    def _tfidf_search(self, query: str, top_k: int) -> List[Dict]:
        """TF-IDF based search on cached product data"""
        if self.tfidf_vectorizer is None or self.tfidf_matrix is None:
            return []
        
        try:
            # Transform query
            query_vec = self.tfidf_vectorizer.transform([query])
            
            # Calculate similarities
            similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
            
            # Get top results
            top_indices = similarities.argsort()[-top_k:][::-1]
            
            results = []
            for idx in top_indices:
                if similarities[idx] > 0:
                    product = self.products_df.iloc[idx]
                    result = {
                        'asin': product.get('asin', ''),
                        'title': product.get('title', ''),
                        'store': product.get('store', ''),
                        'main_category': product.get('main_category', ''),
                        'average_rating': product.get('average_rating', 0),
                        'rating_number': product.get('rating_number', 0),
                        'price': product.get('price', 0),
                        'similarity_score': similarities[idx],
                        'description': product.get('description', ''),
                        'source': 'cached'
                    }
                    results.append(result)
            
            return results
            
        except Exception as e:
            print(f"TF-IDF search error: {e}")
            return []
    
    def _create_product_features(self):
        """Create product features (existing algorithm)"""
        if self.products_df is None or self.products_df.empty:
            print("⚠️ No products data to create features from")
            return
        
        print("🔧 Creating product features...")
        
        # Clean and prepare data
        self.products_df = self.products_df.dropna(subset=['title'])
        self.products_df['title'] = self.products_df['title'].astype(str)
        self.products_df['description'] = self.products_df['description'].fillna('').astype(str)
        
        # Combine title and description for feature extraction
        self.products_df['combined_text'] = (
            self.products_df['title'] + ' ' + 
            self.products_df['description'] + ' ' + 
            self.products_df['store'].fillna('') + ' ' +
            self.products_df['main_category'].fillna('')
        )
        
        print("✅ Product features created")
    
    def _build_tfidf_matrix(self):
        """Build TF-IDF matrix for similarity search"""
        if self.products_df is None or self.products_df.empty:
            print("⚠️ No products data to build TF-IDF matrix")
            return
        
        print("🔧 Building TF-IDF matrix...")
        
        try:
            # Create TF-IDF vectorizer
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=10000,
                stop_words='english',
                lowercase=True,
                ngram_range=(1, 2)
            )
            
            # Fit and transform the combined text
            text_data = self.products_df['combined_text'].fillna('')
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(text_data)
            
            print(f"✅ TF-IDF matrix built: {self.tfidf_matrix.shape}")
            
        except Exception as e:
            print(f"Error building TF-IDF matrix: {e}")
    
    async def get_product_by_asin(self, asin: str) -> Optional[Dict]:
        """Get product details by ASIN (checks live API first)"""
        # Try live API first
        try:
            product = await self.data_source.get_product_details(asin)
            if product:
                return {
                    'asin': product.sku,
                    'title': product.title,
                    'store': product.brand,
                    'main_category': product.category,
                    'average_rating': product.rating,
                    'rating_number': product.review_count,
                    'price': product.price,
                    'description': product.description,
                    'url': product.url,
                    'images': product.images,
                    'source': product.source
                }
        except Exception as e:
            print(f"Live API error for {asin}: {e}")
        
        # Fallback to cached data
        if self.products_df is not None and not self.products_df.empty:
            product_row = self.products_df[self.products_df['asin'] == asin]
            if not product_row.empty:
                return product_row.iloc[0].to_dict()
        
        return None
    
    def get_reviews_by_asin(self, asin: str, limit: int = 5) -> pd.DataFrame:
        """Get reviews for a product"""
        if self.reviews_df is None or self.reviews_df.empty:
            return pd.DataFrame()
        
        product_reviews = self.reviews_df[self.reviews_df['asin'] == asin].head(limit)
        return product_reviews
    
    def get_performance_stats(self) -> Dict:
        """Get system performance statistics"""
        stats = self.data_source.get_performance_stats()
        cache_stats = self.cache.get_cache_stats()
        
        return {
            **stats,
            **cache_stats,
            'products_cached': len(self.products_df) if self.products_df is not None else 0,
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'cache_valid': self.last_update and (datetime.now() - self.last_update) < self.update_interval
        }
    
    async def refresh_cache(self):
        """Manually refresh the cache with latest data"""
        print("🔄 Manually refreshing cache...")
        await self.initialize_with_live_data(force_refresh=True)
    
    def cleanup_old_cache(self):
        """Clean up old cache entries"""
        return self.cache.cleanup_expired()

# Compatibility layer - makes this a drop-in replacement
class BeautyDataProcessor(LiveDataProcessor):
    """Drop-in replacement for existing BeautyDataProcessor"""
    
    def __init__(self, bestbuy_api_key: str = None, rapidapi_key: str = None):
        if not bestbuy_api_key:
            bestbuy_api_key = os.getenv('BESTBUY_API_KEY')
        
        if not bestbuy_api_key:
            # Fallback to static data if no API key
            print("⚠️ No Best Buy API key found, falling back to static data")
            self._init_static_fallback()
            return
        
        super().__init__(bestbuy_api_key, rapidapi_key)
    
    def _init_static_fallback(self):
        """Initialize with static data as fallback"""
        # Initialize empty dataframes
        self.products_df = pd.DataFrame()
        self.reviews_df = pd.DataFrame()
        self.ratings_df = pd.DataFrame()
        self.product_similarity_matrix = None
        self.tfidf_matrix = None
        self.tfidf_vectorizer = None
    
    def load_sample_data(self):
        """Legacy method - now loads live data"""
        asyncio.run(self.initialize_with_live_data())
    
    def search_products(self, query: str, top_k: int = 50) -> List[Dict]:
        """Legacy method - now uses live search"""
        return asyncio.run(self.search_products_live(query, top_k))

# Example usage
async def main():
    """Example usage of the live data processor"""
    # Initialize with Best Buy API key
    bestbuy_key = os.getenv('BESTBUY_API_KEY')
    if not bestbuy_key:
        print("Please set BESTBUY_API_KEY environment variable")
        return
    
    processor = LiveDataProcessor(bestbuy_key)
    
    # Initialize with live data
    await processor.initialize_with_live_data()
    
    # Test search
    results = await processor.search_products_live("gaming laptop", top_k=5)
    print(f"Found {len(results)} gaming laptops")
    
    for product in results:
        print(f"- {product['title']} (${product['price']}) - {product['source']}")
    
    # Performance stats
    stats = processor.get_performance_stats()
    print(f"\nPerformance: {stats}")

if __name__ == "__main__":
    asyncio.run(main())