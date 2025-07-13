#!/usr/bin/env python3
"""
Test script for Advanced NLP Analyzer
Demonstrates the improved review analysis capabilities
"""

import json
from advanced_nlp_analyzer import AdvancedNLPAnalyzer

def test_advanced_nlp():
    """Test the advanced NLP analyzer with sample reviews"""
    
    # Sample reviews for testing
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
        },
        {
            "title": "Not worth the price",
            "text": "This product is way too expensive for what it does. It's gentle and doesn't irritate my skin, but the results are minimal. I've been using it for weeks and see no improvement in my acne. Save your money.",
            "rating": 2
        },
        {
            "title": "Perfect for my skin type",
            "text": "I have combination skin and this product is perfect. It's hydrating where I need it and mattifying where I'm oily. Contains vitamin C which is great for brightening. Highly recommend!",
            "rating": 5
        },
        {
            "title": "Mixed feelings",
            "text": "The texture is nice and it applies smoothly. It's gentle on my sensitive skin which is good. However, it's quite pricey and I'm not sure if the results justify the cost. Good for dry skin types.",
            "rating": 3
        }
    ]
    
    print("🧪 Testing Advanced NLP Analyzer")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = AdvancedNLPAnalyzer()
    
    # Analyze reviews
    analysis = analyzer.analyze_reviews(sample_reviews)
    
    # Display results
    print("\n📊 Analysis Results:")
    print("-" * 30)
    
    # Sentiment Analysis
    sentiment = analysis['sentiment_analysis']
    print(f"📈 Average Sentiment: {sentiment['average_sentiment']:.2f}")
    print(f"😊 Positive Reviews: {sentiment['sentiment_distribution']['positive']}")
    print(f"😐 Neutral Reviews: {sentiment['sentiment_distribution']['neutral']}")
    print(f"😞 Negative Reviews: {sentiment['sentiment_distribution']['negative']}")
    
    # Entity Extraction
    entities = analysis['entity_extraction']
    print(f"\n🏷️  Extracted Entities:")
    print(f"   Ingredients: {entities['ingredients']}")
    print(f"   Skin Types: {entities['skin_types']}")
    print(f"   Concerns: {entities['concerns']}")
    print(f"   Effects: {entities['effects']}")
    
    # Skin Type Analysis
    skin_mentions = analysis['skin_type_mentions']
    if skin_mentions:
        print(f"\n👥 Skin Type Mentions:")
        for skin_type, count in skin_mentions.items():
            print(f"   {skin_type}: {count} mentions")
    
    # Effect Analysis
    effects = analysis['effect_analysis']
    if effects:
        print(f"\n✨ Effect Analysis:")
        for effect, count in effects.items():
            print(f"   {effect}: {count} mentions")
    
    # Price Sentiment
    price_sentiment = analysis['price_sentiment']
    if any(price_sentiment.values()):
        print(f"\n💰 Price Sentiment:")
        for category, count in price_sentiment.items():
            if count > 0:
                print(f"   {category}: {count} mentions")
    
    # Usage Patterns
    usage = analysis['usage_patterns']
    if any(usage.values()):
        print(f"\n⏰ Usage Patterns:")
        for pattern, count in usage.items():
            if count > 0:
                print(f"   {pattern}: {count} mentions")
    
    # Generated Insights
    insights = analysis['overall_insights']
    print(f"\n💡 Generated Insights:")
    for insight in insights:
        print(f"   • {insight}")
    
    print("\n" + "=" * 50)
    print("✅ Advanced NLP Analysis Complete!")
    
    return analysis

def compare_with_simple_analysis():
    """Compare advanced NLP with simple keyword matching"""
    
    print("\n🔄 Comparison: Advanced NLP vs Simple Analysis")
    print("=" * 50)
    
    # Sample review text
    review_text = "This foundation is amazing for my oily skin. It keeps me matte all day and contains hyaluronic acid. A bit expensive but worth it."
    
    # Simple analysis (current method)
    simple_themes = ['gentle', 'effective', 'hydrating', 'expensive', 'oily']
    simple_found = [theme for theme in simple_themes if theme in review_text.lower()]
    
    # Advanced analysis
    analyzer = AdvancedNLPAnalyzer()
    advanced_analysis = analyzer.analyze_reviews([{"title": "", "text": review_text}])
    
    print(f"\n📝 Review: {review_text}")
    print(f"\n🔍 Simple Analysis:")
    print(f"   Found themes: {simple_found}")
    
    print(f"\n🧠 Advanced NLP Analysis:")
    print(f"   Sentiment: {advanced_analysis['sentiment_analysis']['average_sentiment']:.2f}")
    print(f"   Skin types: {advanced_analysis['skin_type_mentions']}")
    print(f"   Effects: {advanced_analysis['effect_analysis']}")
    print(f"   Price sentiment: {advanced_analysis['price_sentiment']}")
    print(f"   Insights: {advanced_analysis['overall_insights']}")

if __name__ == "__main__":
    # Test advanced NLP
    test_advanced_nlp()
    
    # Compare with simple analysis
    compare_with_simple_analysis() 