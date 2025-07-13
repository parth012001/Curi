#!/usr/bin/env python3
"""
Test script for Enhanced Review Analysis
Tests the integration of advanced NLP into the conversational engine
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from conversational_engine import ConversationalEngine
from data_processor import BeautyDataProcessor

def test_enhanced_review_analysis():
    """Test the enhanced review analysis with advanced NLP"""
    
    print("🧪 Testing Enhanced Review Analysis")
    print("=" * 50)
    
    # Initialize components
    print("🔄 Initializing components...")
    data_processor = BeautyDataProcessor()
    data_processor.load_sample_data()
    
    conversational_engine = ConversationalEngine(data_processor)
    print("✅ Components initialized")
    
    # Test query
    test_query = "foundation for oily skin"
    print(f"\n🔍 Testing query: '{test_query}'")
    
    # Get recommendations
    print("\n📋 Getting recommendations...")
    analysis = conversational_engine.get_smart_recommendations(test_query, top_k=3)
    
    # Display results
    print(f"\n📊 Found {len(analysis['recommendations'])} products")
    print("-" * 30)
    
    for i, product in enumerate(analysis['recommendations'], 1):
        print(f"\n🏷️  Product {i}: {product.get('title', 'Unknown')}")
        print(f"   Brand: {product.get('store', 'Unknown')}")
        print(f"   Rating: {product.get('average_rating', 0):.1f}/5 ({product.get('rating_number', 0)} reviews)")
        
        # Check if NLP analysis is available
        if 'nlp_analysis' in product:
            nlp_data = product['nlp_analysis']
            
            print(f"   📊 Sentiment: {nlp_data['sentiment_analysis']['average_sentiment']:.2f}")
            
            # Skin type mentions
            skin_mentions = nlp_data['skin_type_mentions']
            if skin_mentions:
                print(f"   👥 Skin Types: {list(skin_mentions.keys())}")
            
            # Effects
            effects = nlp_data['effect_analysis']
            if effects:
                top_effects = sorted(effects.items(), key=lambda x: x[1], reverse=True)[:3]
                effect_names = [effect[0] for effect in top_effects]
                print(f"   ✨ Key Effects: {', '.join(effect_names)}")
            
            # Ingredients
            ingredients = nlp_data['ingredient_mentions']
            if ingredients:
                print(f"   🧪 Ingredients: {', '.join(ingredients[:3])}")
            
            # Price sentiment
            price_sentiment = nlp_data['price_sentiment']
            if any(price_sentiment.values()):
                price_insights = []
                if price_sentiment.get('worth_it', 0) > 0:
                    price_insights.append("worth the price")
                if price_sentiment.get('expensive', 0) > 0:
                    price_insights.append("expensive")
                if price_sentiment.get('affordable', 0) > 0:
                    price_insights.append("affordable")
                if price_insights:
                    print(f"   💰 Price: {', '.join(price_insights)}")
        
        # Display insights
        insights = product.get('insights', [])
        if insights:
            print(f"   💡 Insights:")
            for insight in insights[:3]:  # Show top 3 insights
                print(f"      • {insight}")
        else:
            print(f"   ⚠️  No insights available")
    
    print("\n" + "=" * 50)
    print("✅ Enhanced Review Analysis Test Complete!")
    
    return analysis

def test_caching_performance():
    """Test that caching is working correctly"""
    
    print("\n🔄 Testing Caching Performance")
    print("=" * 30)
    
    # Initialize components
    data_processor = BeautyDataProcessor()
    data_processor.load_sample_data()
    conversational_engine = ConversationalEngine(data_processor)
    
    # Test the same query twice to check caching
    test_query = "moisturizer for dry skin"
    
    print(f"🔍 Running query: '{test_query}' (first time)")
    analysis1 = conversational_engine.get_smart_recommendations(test_query, top_k=2)
    
    print(f"🔍 Running query: '{test_query}' (second time - should use cache)")
    analysis2 = conversational_engine.get_smart_recommendations(test_query, top_k=2)
    
    print(f"📋 Cache size: {len(conversational_engine.nlp_cache)}")
    print("✅ Caching test complete!")

def compare_old_vs_new_analysis():
    """Compare old simple analysis vs new advanced NLP analysis"""
    
    print("\n🔄 Comparison: Old vs New Analysis")
    print("=" * 40)
    
    # Sample review data
    sample_reviews = [
        {
            "title": "Great for oily skin!",
            "text": "This foundation is amazing for my oily skin. It keeps me matte all day and doesn't break me out. Contains hyaluronic acid which is great for hydration. A bit expensive but worth it for the results.",
            "rating": 5
        },
        {
            "title": "Good but expensive",
            "text": "The product works well and gives a nice finish. It's gentle on my sensitive skin and doesn't cause irritation. However, it's quite expensive for the amount you get. Would recommend for combination skin types.",
            "rating": 4
        }
    ]
    
    # Old simple analysis (simulated)
    old_themes = ['gentle', 'effective', 'hydrating', 'expensive', 'oily']
    old_found = [theme for theme in old_themes if theme in ' '.join([r['text'] for r in sample_reviews]).lower()]
    
    # New advanced analysis
    from advanced_nlp_analyzer import AdvancedNLPAnalyzer
    analyzer = AdvancedNLPAnalyzer()
    new_analysis = analyzer.analyze_reviews(sample_reviews)
    
    print(f"📝 Sample Reviews: {len(sample_reviews)} reviews")
    print(f"\n🔍 Old Simple Analysis:")
    print(f"   Found themes: {old_found}")
    
    print(f"\n🧠 New Advanced NLP Analysis:")
    print(f"   Sentiment: {new_analysis['sentiment_analysis']['average_sentiment']:.2f}")
    print(f"   Skin types: {list(new_analysis['skin_type_mentions'].keys())}")
    print(f"   Effects: {list(new_analysis['effect_analysis'].keys())}")
    print(f"   Ingredients: {new_analysis['ingredient_mentions']}")
    print(f"   Price sentiment: {new_analysis['price_sentiment']}")
    print(f"   Insights: {new_analysis['overall_insights']}")
    
    print(f"\n📈 Improvement:")
    print(f"   Old: {len(old_found)} simple themes")
    print(f"   New: {len(new_analysis['overall_insights'])} rich insights")
    print(f"   Enhancement: {len(new_analysis['overall_insights']) - len(old_found)}x more detailed")

if __name__ == "__main__":
    # Test enhanced review analysis
    test_enhanced_review_analysis()
    
    # Test caching performance
    test_caching_performance()
    
    # Compare old vs new analysis
    compare_old_vs_new_analysis() 