#!/usr/bin/env python3
"""
Test script to demonstrate LLM integration capabilities
"""

from data_processor import BeautyDataProcessor
from conversational_engine import ConversationalEngine
from llm_engine import LLMEngine

def test_llm_integration():
    """Test LLM integration with sample queries"""
    
    print("🚀 Testing LLM Integration for Curi MVP\n")
    
    # Initialize components
    print("📊 Loading data...")
    data_processor = BeautyDataProcessor()
    
    # Try to load processed data
    if not data_processor.load_processed_data():
        print("❌ No processed data found. Please run the main test first.")
        return
    
    # Initialize conversational engine with LLM
    print("🤖 Initializing conversational engine with LLM...")
    llm_engine = LLMEngine()
    conversational_engine = ConversationalEngine(data_processor, llm_engine)
    
    # Test queries that should benefit from LLM
    test_queries = [
        "I need a morning cream for men which I can apply in the morning after shower before heading out",
        "Find me a gentle cleanser for sensitive skin that won't irritate",
        "I want an anti-aging serum for dry skin",
        "Recommend a moisturizer for acne-prone skin that won't break me out"
    ]
    
    print("\n🧪 Testing LLM Integration:")
    print("=" * 60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: '{query}'")
        print("-" * 40)
        
        # Get response with LLM
        response = conversational_engine.get_conversational_response(query)
        
        print(f"Enhanced Query: {response.get('enhanced_query', query)}")
        print(f"Intent: {response['intent']}")
        print(f"Features: {response['features']}")
        print(f"Response: {response['response'][:200]}...")
        
        if response['recommendations']:
            top_rec = response['recommendations'][0]
            print(f"Top Recommendation: {top_rec['title'][:60]}...")
            if 'llm_analysis' in top_rec:
                analysis = top_rec['llm_analysis']
                print(f"LLM Match Score: {analysis.get('match_score', 'N/A')}/10")
                print(f"LLM Reasoning: {analysis.get('reasoning', 'N/A')[:100]}...")
        
        print()
    
    # Test LLM availability
    print("\n🔍 LLM Status:")
    print(f"LLM Available: {llm_engine.is_available()}")
    if not llm_engine.is_available():
        print("⚠️  No OpenAI API key found. Set OPENAI_API_KEY environment variable.")
        print("   The system will work with fallback methods.")
    
    print("\n✅ LLM Integration Test Complete!")
    print("\n📝 Next Steps:")
    print("1. Set your OpenAI API key: export OPENAI_API_KEY='your-key-here'")
    print("2. Run this test again to see LLM-enhanced results")
    print("3. Launch the Streamlit app to try the enhanced experience")

if __name__ == "__main__":
    test_llm_integration() 