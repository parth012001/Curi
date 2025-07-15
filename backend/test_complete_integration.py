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

def test_conversational_memory():
    """Test session-based conversational memory with edge cases"""
    print("\n🧪 Testing Conversational Memory (Session-based)")
    print("=" * 60)
    
    data_processor = BeautyDataProcessor()
    data_processor.load_sample_data()
    llm_engine = LLMEngine()
    conversational_engine = ConversationalEngine(data_processor, llm_engine)

    # 1. Simple multi-turn follow-up
    history = [
        {"role": "user", "content": "Recommend a moisturizer for dry skin."},
        {"role": "assistant", "content": "Here are some moisturizers for dry skin..."},
        {"role": "user", "content": "What about for sensitive skin?"}
    ]
    followup_query = "What about for sensitive skin?"
    response = conversational_engine.get_conversational_response(followup_query, history=history)
    print("\n🔄 Multi-turn follow-up:")
    print(response['response'])
    assert any(word in response['response'].lower() for word in ["sensitive skin", "sensitive"]), "Follow-up context not used."

    # 2. Switch topic mid-session
    history2 = history + [
        {"role": "assistant", "content": response['response']},
        {"role": "user", "content": "Show me the best sunscreen for oily skin."}
    ]
    new_topic_query = "Show me the best sunscreen for oily skin."
    response2 = conversational_engine.get_conversational_response(new_topic_query, history=history2)
    print("\n🔄 Topic switch:")
    print(response2['response'])
    assert "sunscreen" in response2['response'].lower(), "Topic switch not handled."
    assert "oily skin" in response2['response'].lower(), "New context not recognized."

    # 3. Edge case: Empty history
    response3 = conversational_engine.get_conversational_response("Recommend a serum for anti-aging.", history=[])
    print("\n🔄 Empty history:")
    print(response3['response'])
    assert "serum" in response3['response'].lower(), "Serum not mentioned in response."
    assert "anti-aging" in response3['response'].lower(), "Anti-aging not mentioned."

    # 4. Edge case: Very long history (should only use last 6 messages)
    long_history = []
    for i in range(20):
        long_history.append({"role": "user", "content": f"Dummy message {i}"})
        long_history.append({"role": "assistant", "content": f"Dummy reply {i}"})
    long_history.append({"role": "user", "content": "Recommend a toner for redness."})
    response4 = conversational_engine.get_conversational_response("Recommend a toner for redness.", history=long_history)
    print("\n🔄 Very long history:")
    print(response4['response'])
    assert "toner" in response4['response'].lower(), "Toner not mentioned."
    assert "redness" in response4['response'].lower(), "Redness not mentioned."

    # 5. Edge case: Malformed history (should not crash)
    malformed_history = [
        {"role": "user", "content": "Recommend a cleanser."},
        {"role": "assistant"},  # Missing content
        {"role": "user", "content": None},  # None content
        "just a string",  # Not a dict
        12345  # Not a dict
    ]
    try:
        response5 = conversational_engine.get_conversational_response("What about for acne-prone skin?", history=malformed_history)
        print("\n🔄 Malformed history:")
        print(response5['response'])
        assert "acne" in response5['response'].lower(), "Acne context not handled."
    except Exception as e:
        print(f"[ERROR] Malformed history caused exception: {e}")
        assert False, "Malformed history should not crash the system."

    # 6. Abrupt topic change after follow-up
    abrupt_history = [
        {"role": "user", "content": "Recommend a moisturizer for dry skin."},
        {"role": "assistant", "content": "Here are some moisturizers for dry skin..."},
        {"role": "user", "content": "What about for sensitive skin?"},
        {"role": "assistant", "content": "Here are some for sensitive skin..."},
        {"role": "user", "content": "Show me a luxury serum for wrinkles."}
    ]
    abrupt_query = "Show me a luxury serum for wrinkles."
    response6 = conversational_engine.get_conversational_response(abrupt_query, history=abrupt_history)
    print("\n🔄 Abrupt topic change:")
    print(response6['response'])
    assert "serum" in response6['response'].lower(), "Serum not mentioned after abrupt change."
    assert "wrinkles" in response6['response'].lower(), "Wrinkles not mentioned."
    assert "luxury" in response6['response'].lower(), "Luxury not mentioned."

    print("\n✅ Conversational memory test passed!")

if __name__ == "__main__":
    # Test complete integration
    test_complete_integration()
    
    # Test caching performance
    test_caching_performance()
    
    # Test response quality
    test_response_quality()
    
    # Compare old vs new system
    compare_old_vs_new_system()
    
    # Test conversational memory
    test_conversational_memory() 