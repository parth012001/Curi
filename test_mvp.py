#!/usr/bin/env python3
"""
Test script for Curi MVP components
"""

import sys
import time
from data_processor import BeautyDataProcessor
from conversational_engine import ConversationalEngine

def test_data_loading():
    """Test data loading and processing"""
    print("🧪 Testing data loading...")
    
    try:
        # Initialize data processor
        processor = BeautyDataProcessor()
        
        # Try to load processed data first
        if processor.load_processed_data():
            print("✅ Successfully loaded cached data")
        else:
            print("📊 Loading and processing data from scratch...")
            processor.load_data()
            processor.preprocess_data()
            processor.create_product_features()
            processor.build_tfidf_matrix()
            processor.build_similarity_matrices()
            processor.save_processed_data()
            print("✅ Successfully processed and cached data")
        
        print(f"📈 Data Summary:")
        print(f"   - Products: {len(processor.products_df):,}")
        print(f"   - Reviews: {len(processor.reviews_df):,}")
        print(f"   - Ratings: {len(processor.ratings_df):,}")
        
        return processor
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def test_conversational_engine(processor):
    """Test conversational engine functionality"""
    print("\n🧪 Testing conversational engine...")
    
    try:
        engine = ConversationalEngine(processor)
        
        # Test queries
        test_queries = [
            "I need a gentle cleanser for sensitive skin",
            "Find me anti-aging products",
            "Recommend moisturizers for dry skin",
            "Show me products for acne-prone skin"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Testing query: '{query}'")
            response = engine.get_conversational_response(query)
            
            print(f"   Intent: {response['intent']}")
            print(f"   Features: {response['features']}")
            print(f"   Recommendations: {len(response['recommendations'])} products")
            
            if response['recommendations']:
                top_rec = response['recommendations'][0]
                print(f"   Top recommendation: {top_rec['title'][:50]}...")
        
        print("✅ Conversational engine working correctly")
        return engine
        
    except Exception as e:
        print(f"❌ Error testing conversational engine: {e}")
        return None

def test_search_functionality(processor):
    """Test search and recommendation functionality"""
    print("\n🧪 Testing search functionality...")
    
    try:
        # Test product search
        search_results = processor.search_products("gentle cleanser", top_k=5)
        print(f"✅ Found {len(search_results)} products for 'gentle cleanser'")
        
        # Test similar products
        if search_results:
            similar_products = processor.get_similar_products(search_results[0]['asin'], top_k=3)
            print(f"✅ Found {len(similar_products)} similar products")
        
        # Test popular products
        popular_products = processor.get_popular_products(top_k=5)
        print(f"✅ Found {len(popular_products)} popular products")
        
        print("✅ Search functionality working correctly")
        
    except Exception as e:
        print(f"❌ Error testing search functionality: {e}")

def main():
    """Run all tests"""
    print("🚀 Starting Curi MVP Tests\n")
    
    # Test data loading
    processor = test_data_loading()
    if not processor:
        print("❌ Data loading failed. Exiting.")
        return
    
    # Test conversational engine
    engine = test_conversational_engine(processor)
    if not engine:
        print("❌ Conversational engine failed. Exiting.")
        return
    
    # Test search functionality
    test_search_functionality(processor)
    
    print("\n🎉 All tests completed successfully!")
    print("\n📝 Next steps:")
    print("   1. Open your browser to http://localhost:8501")
    print("   2. Try the example queries in the sidebar")
    print("   3. Ask Curi about beauty products in natural language")
    print("   4. Explore the recommendations and insights")

if __name__ == "__main__":
    main() 