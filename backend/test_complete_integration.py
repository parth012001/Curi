#!/usr/bin/env python3
"""
Test script for Complete Advanced NLP Integration
Tests all three steps: Review Analysis, LLM Analysis, and Response Generation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from conversational_engine import ConversationalEngine
from data_processor import BeautyDataProcessor
from llm_engine import LLMEngine

def test_complete_integration():
    """Test the complete integration of advanced NLP into the recommendation system"""
    
    print("🧪 Testing Complete Advanced NLP Integration")
    print("=" * 60)
    
    # Initialize components
    print("🔄 Initializing components...")
    data_processor = BeautyDataProcessor()
    data_processor.load_sample_data()
    
    llm_engine = LLMEngine()
    conversational_engine = ConversationalEngine(data_processor, llm_engine)
    print("✅ Components initialized")
    
    # Test queries
    test_queries = [
        "foundation for oily skin",
        "moisturizer for dry skin",
        "serum for anti-aging"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"🔍 Testing Query: '{query}'")
        print(f"{'='*60}")
        
        # Get conversational response
        response = conversational_engine.get_conversational_response(query)
        
        # Display results
        print(f"\n💬 Generated Response:")
        print(f"   {response['response']}")
        
        print(f"\n📊 Technical Analysis:")
        print(f"   Intent: {response['intent']}")
        print(f"   Features: {response['features']}")
        print(f"   Products Found: {len(response['recommendations'])}")
        
        # Display product details
        for i, product in enumerate(response['recommendations'][:3], 1):
            print(f"\n🏷️  Product {i}: {product.get('title', 'Unknown')}")
            print(f"   Brand: {product.get('store', 'Unknown')}")
            print(f"   Rating: {product.get('average_rating', 0):.1f}/5 ({product.get('rating_number', 0)} reviews)")
            
            # NLP Analysis
            if 'nlp_analysis' in product:
                nlp_data = product['nlp_analysis']
                print(f"   📊 Sentiment: {nlp_data['sentiment_analysis']['average_sentiment']:.2f}")
                
                skin_mentions = nlp_data['skin_type_mentions']
                if skin_mentions:
                    print(f"   👥 Skin Types: {list(skin_mentions.keys())}")
                
                effects = nlp_data['effect_analysis']
                if effects:
                    print(f"   ✨ Effects: {list(effects.keys())}")
                
                ingredients = nlp_data['ingredient_mentions']
                if ingredients:
                    print(f"   🧪 Ingredients: {ingredients}")
                
                price_sentiment = nlp_data['price_sentiment']
                if any(price_sentiment.values()):
                    print(f"   💰 Price: {price_sentiment}")
            
            # LLM Analysis
            if 'llm_analysis' in product:
                llm_data = product['llm_analysis']
                print(f"   🎯 Match Score: {llm_data.get('match_score', 0):.1%}")
                print(f"   🧠 Confidence: {llm_data.get('confidence_level', 'unknown')}")
                print(f"   👥 Skin Match: {llm_data.get('skin_type_match', 'unknown')}")
                print(f"   💰 Price Rec: {llm_data.get('price_recommendation', 'unknown')}")
            
            # Insights
            insights = product.get('insights', [])
            if insights:
                print(f"   💡 Insights:")
                for insight in insights[:2]:
                    print(f"      • {insight}")
    
    print(f"\n{'='*60}")
    print("✅ Complete Integration Test Complete!")
    
    return response

def test_caching_performance():
    """Test caching performance across the complete system"""
    
    print("\n🔄 Testing Caching Performance")
    print("=" * 40)
    
    # Initialize components
    data_processor = BeautyDataProcessor()
    data_processor.load_sample_data()
    conversational_engine = ConversationalEngine(data_processor)
    
    # Test the same query multiple times
    test_query = "foundation for oily skin"
    
    print(f"🔍 Running query: '{test_query}' (first time)")
    response1 = conversational_engine.get_conversational_response(test_query)
    
    print(f"🔍 Running query: '{test_query}' (second time - should use cache)")
    response2 = conversational_engine.get_conversational_response(test_query)
    
    print(f"🔍 Running query: '{test_query}' (third time - should use cache)")
    response3 = conversational_engine.get_conversational_response(test_query)
    
    print(f"📋 Cache size: {len(conversational_engine.nlp_cache)}")
    print("✅ Caching performance test complete!")

def test_response_quality():
    """Test the quality of generated responses"""
    
    print("\n🧪 Testing Response Quality")
    print("=" * 35)
    
    # Initialize components
    data_processor = BeautyDataProcessor()
    data_processor.load_sample_data()
    conversational_engine = ConversationalEngine(data_processor)
    
    # Test different query types
    test_queries = [
        "foundation for oily skin",
        "moisturizer for sensitive skin",
        "serum for anti-aging"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        
        response = conversational_engine.get_conversational_response(query)
        
        print(f"💬 Response: {response['response'][:200]}...")
        
        # Analyze response quality
        response_text = response['response']
        
        # Check for specific elements
        has_product_mention = any(word in response_text.lower() for word in ['recommendation', 'product', 'foundation', 'moisturizer', 'serum'])
        has_rating_mention = 'rating' in response_text.lower() or 'stars' in response_text.lower()
        has_insight_mention = any(word in response_text.lower() for word in ['users', 'love', 'benefits', 'contains', 'worth'])
        
        print(f"   ✅ Product Mention: {has_product_mention}")
        print(f"   ✅ Rating Mention: {has_rating_mention}")
        print(f"   ✅ Insight Mention: {has_insight_mention}")
        
        # Count products found
        product_count = len(response['recommendations'])
        print(f"   📊 Products Found: {product_count}")

def compare_old_vs_new_system():
    """Compare old system vs new advanced NLP system"""
    
    print("\n🔄 Comparison: Old vs New System")
    print("=" * 40)
    
    # Sample data for comparison
    sample_query = "foundation for oily skin"
    
    print(f"📝 Query: '{sample_query}'")
    
    # Old system (simulated)
    old_response = "I found some beauty products related to 'foundation for oily skin'. I'll focus on products suitable for oily skin. I'm searching for foundation options. I found 3 great options for you. My top recommendation is Test Foundation by Test Brand (rated 4.2/5 by 150 users). Users say: 👍 Users love: gentle, effective"
    
    # New system (actual)
    data_processor = BeautyDataProcessor()
    data_processor.load_sample_data()
    conversational_engine = ConversationalEngine(data_processor)
    
    new_response = conversational_engine.get_conversational_response(sample_query)
    
    print(f"\n🔍 Old System Response:")
    print(f"   {old_response}")
    
    print(f"\n🧠 New System Response:")
    print(f"   {new_response['response']}")
    
    print(f"\n📈 Improvements:")
    print(f"   Old: Basic keyword matching")
    print(f"   New: Advanced NLP + LLM analysis")
    print(f"   Old: Simple insights")
    print(f"   New: Rich insights with sentiment, skin types, effects, ingredients")
    print(f"   Old: Generic responses")
    print(f"   New: Personalized, specific responses")

if __name__ == "__main__":
    # Test complete integration
    test_complete_integration()
    
    # Test caching performance
    test_caching_performance()
    
    # Test response quality
    test_response_quality()
    
    # Compare old vs new system
    compare_old_vs_new_system() 