#!/usr/bin/env python3
"""
Helper script to set up OpenAI API key
"""

import os
from dotenv import load_dotenv

def setup_api_key():
    """Guide user through setting up OpenAI API key"""
    
    print("🔑 OpenAI API Key Setup for Curi MVP")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found. Creating one...")
        create_env_file()
    
    # Load current .env
    load_dotenv()
    current_key = os.getenv('OPENAI_API_KEY')
    
    if current_key and current_key != 'your_openai_api_key_here':
        print("✅ OpenAI API key is already configured!")
        print(f"Current key: {current_key[:10]}...{current_key[-4:]}")
        return True
    
    print("\n📝 To use LLM features, you need an OpenAI API key:")
    print("1. Go to https://platform.openai.com/api-keys")
    print("2. Create a new API key")
    print("3. Copy the key")
    print("4. Replace 'your_openai_api_key_here' in the .env file with your actual key")
    
    print("\n🔧 Quick setup:")
    api_key = input("Enter your OpenAI API key (or press Enter to skip): ").strip()
    
    if api_key:
        update_env_file(api_key)
        print("✅ API key saved to .env file!")
        return True
    else:
        print("⚠️  No API key provided. LLM features will be disabled.")
        return False

def create_env_file():
    """Create a new .env file with template"""
    env_content = """# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Model Configuration
OPENAI_MODEL=gpt-3.5-turbo

# Optional: Cost Management
MAX_TOKENS_PER_REQUEST=400
TEMPERATURE=0.3

# Optional: App Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file")

def update_env_file(api_key):
    """Update .env file with actual API key"""
    try:
        with open('.env', 'r') as f:
            content = f.read()
        
        # Replace the placeholder with actual key
        content = content.replace('your_openai_api_key_here', api_key)
        
        with open('.env', 'w') as f:
            f.write(content)
            
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")

def test_api_key():
    """Test if the API key works"""
    from llm_engine import LLMEngine
    
    llm = LLMEngine()
    if llm.is_available():
        print("✅ API key is working!")
        return True
    else:
        print("❌ API key is not working. Please check your key.")
        return False

if __name__ == "__main__":
    setup_api_key()
    
    # Test the API key
    print("\n🧪 Testing API key...")
    test_api_key()
    
    print("\n📝 Next steps:")
    print("1. Run: python3 test_llm_integration.py")
    print("2. Run: streamlit run app.py")
    print("3. Try the enhanced conversational experience!") 