#!/usr/bin/env python3
"""
Test script for Enhanced LLM Analysis
Tests the integration of advanced NLP insights into LLM analysis
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from conversational_engine import ConversationalEngine
from data_processor import BeautyDataProcessor
from llm_engine import LLMEngine

def test_enhanced_llm_analysis():
    """Test the enhanced LLM analysis with advanced NLP insights"""
    
    print("🧪 Testing Enhanced LLM Analysis")
    print("=" * 50)
    
    # Initialize components
    print("🔄 Initializing components...")
    data_processor = BeautyDataProcessor()
    data_processor.load_sample_data()
    
    llm_engine = LLMEngine()
    conversational_engine = ConversationalEngine(data_processor, llm_engine)
    print("✅ Components initialized")
    
    # Test query
    test_query = "foundation for oily skin"
    print(f"\n🔍 Testing query: '{test_query}'")
    
    # Get recommendations with enhanced LLM analysis
    print("\n📋 Getting recommendations with enhanced LLM analysis...")
    analysis = conversational_engine.get_smart_recommendations(test_query, top_k=3)
    
    # Display results
    print(f"\n📊 Found {len(analysis['recommendations'])} products")
    print("-" * 30)
    
    for i, product in enumerate(analysis['recommendations'], 1):
        print(f"\n🏷️  Product {i}: {product.get('title', 'Unknown')}")
        print(f"   Brand: {product.get('store', 'Unknown')}")
        print(f"   Rating: {product.get('average_rating', 0):.1f}/5 ({product.get('rating_number', 0)} reviews)")
        
        # Check if LLM analysis is available
        if 'llm_analysis' in product:
            llm_data = product['llm_analysis']
            
            print(f"   🎯 Match Score: {llm_data.get('match_score', 0):.1%}")
            print(f"   🧠 Confidence: {llm_data.get('confidence_level', 'unknown')}")
            print(f"   👥 Skin Type Match: {llm_data.get('skin_type_match', 'unknown')}")
            print(f"   💰 Price Recommendation: {llm_data.get('price_recommendation', 'unknown')}")
            
            # Display reasoning
            reasoning = llm_data.get('reasoning', '')
            if reasoning:
                print(f"   💭 Reasoning: {reasoning[:200]}...")
            
            # Display key features
            key_features = llm_data.get('key_features', [])
            if key_features:
                print(f"   ✨ Key Features: {', '.join(key_features[:3])}")
        
        # Display NLP insights
        if 'nlp_analysis' in product:
            nlp_data = product['nlp_analysis']
            insights = nlp_data.get('overall_insights', [])
            if insights:
                print(f"   💡 NLP Insights:")
                for insight in insights[:2]:  # Show top 2 insights
                    print(f"      • {insight}")
    
    print("\n" + "=" * 50)
    print("✅ Enhanced LLM Analysis Test Complete!")
    
    return analysis

def test_llm_analysis_quality():
    """Test the quality of LLM analysis with different query types"""
    
    print("\n🧪 Testing LLM Analysis Quality")
    print("=" * 40)
    
    # Initialize components
    data_processor = BeautyDataProcessor()
    data_processor.load_sample_data()
    llm_engine = LLMEngine()
    
    # Test different query types
    test_queries = [
        "moisturizer for dry skin",
        "serum for anti-aging",
        "cleanser for sensitive skin"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing: '{query}'")
        
        # Get a sample product for analysis
        search_results = data_processor.search_products(query, top_k=1)
        if search_results:
            product = data_processor.get_product_by_asin(search_results[0]['asin'])
            reviews = data_processor.get_reviews_by_asin(search_results[0]['asin'], limit=3)
            
            if product is not None:
                # Test LLM analysis
                analysis = llm_engine.analyze_product_match(
                    query, 
                    product.to_dict() if hasattr(product, 'to_dict') else dict(product),
                    reviews.to_dict('records') if not reviews.empty else None
                )
                
                print(f"   📊 Match Score: {analysis.get('match_score', 0):.1%}")
                print(f"   🧠 Confidence: {analysis.get('confidence_level', 'unknown')}")
                print(f"   👥 Skin Match: {analysis.get('skin_type_match', 'unknown')}")
                print(f"   💰 Price: {analysis.get('price_recommendation', 'unknown')}")
                
                reasoning = analysis.get('reasoning', '')
                if reasoning:
                    print(f"   💭 Reasoning: {reasoning[:150]}...")
            else:
                print(f"   ⚠️  No product found for analysis")

def compare_old_vs_enhanced_llm():
    """Compare old LLM analysis vs enhanced LLM analysis"""
    
    print("\n🔄 Comparison: Old vs Enhanced LLM Analysis")
    print("=" * 50)
    
    # Sample data
    sample_product = {
        'title': 'Test Foundation for Oily Skin',
        'store': 'Test Brand',
        'main_category': 'Makeup',
        'average_rating': 4.2,
        'rating_number': 150
    }
    
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
    
    test_query = "foundation for oily skin"
    
    # Initialize LLM engine
    llm_engine = LLMEngine()
    
    print(f"📝 Product: {sample_product['title']}")
    print(f"🔍 Query: '{test_query}'")
    print(f"📊 Reviews: {len(sample_reviews)} reviews")
    
    # Test enhanced LLM analysis
    print(f"\n🧠 Enhanced LLM Analysis:")
    enhanced_analysis = llm_engine.analyze_product_match(test_query, sample_product, sample_reviews)
    
    print(f"   Match Score: {enhanced_analysis.get('match_score', 0):.1%}")
    print(f"   Confidence: {enhanced_analysis.get('confidence_level', 'unknown')}")
    print(f"   Skin Match: {enhanced_analysis.get('skin_type_match', 'unknown')}")
    print(f"   Price Rec: {enhanced_analysis.get('price_recommendation', 'unknown')}")
    
    reasoning = enhanced_analysis.get('reasoning', '')
    if reasoning:
        print(f"   Reasoning: {reasoning[:200]}...")
    
    key_features = enhanced_analysis.get('key_features', [])
    if key_features:
        print(f"   Features: {', '.join(key_features)}")

if __name__ == "__main__":
    # Test enhanced LLM analysis
    test_enhanced_llm_analysis()
    
    # Test LLM analysis quality
    test_llm_analysis_quality()
    
    # Compare old vs enhanced
    compare_old_vs_enhanced_llm() 