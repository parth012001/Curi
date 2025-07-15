"""
FastAPI Backend for Curi - Beauty Product Research Assistant
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
import os
from dotenv import load_dotenv

# Import our existing modules
from data_processor import BeautyDataProcessor as DataProcessor
from conversational_engine import ConversationalEngine
from llm_engine import LLMEngine

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Curi API",
    description="Intelligent Beauty Product Research Assistant",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for initialized components
data_processor = None
conversational_engine = None
llm_engine = None

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = None
    history: Optional[List[Dict[str, Any]]] = None

class ChatResponse(BaseModel):
    response: str
    products: List[Dict[str, Any]]
    insights: List[str]
    confidence: float

class ProductInfo(BaseModel):
    asin: str
    title: str
    store: str
    main_category: str
    average_rating: float
    rating_number: int
    price: float
    similarity_score: float

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup"""
    global data_processor, conversational_engine, llm_engine
    
    try:
        print("🔄 Initializing Curi backend...")
        
        # Initialize data processor
        data_processor = DataProcessor()
        data_processor.load_sample_data()
        print("✅ Data processor initialized")
        
        # Initialize conversational engine
        conversational_engine = ConversationalEngine(data_processor)
        print("✅ Conversational engine initialized")
        
        # Initialize LLM engine
        try:
            llm_engine = LLMEngine()
            print("✅ LLM engine initialized")
        except Exception as e:
            print(f"⚠️ LLM engine not available: {e}")
            llm_engine = None
        
        print("🚀 Curi backend ready!")
        
    except Exception as e:
        print(f"❌ Error initializing backend: {e}")
        raise e

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Curi API - Intelligent Beauty Product Research Assistant",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "data_loaded": data_processor is not None,
        "llm_available": llm_engine is not None if llm_engine else False
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Main chat endpoint"""
    try:
        if not conversational_engine:
            raise HTTPException(status_code=500, detail="Conversational engine not initialized")
        
        # Process the query with conversation history
        response = conversational_engine.get_conversational_response(message.message, history=message.history)
        
        # Extract components
        chat_response = response.get('response', '')
        response_type = response.get('response_type', 'new_recommendation')
        products = response.get('recommendations', [])
        
        # Extract insights from products
        insights = []
        for product in products:
            if 'insights' in product:
                insights.extend(product['insights'])
        
        # Convert numpy types to native Python types for JSON serialization
        serializable_products = []
        for product in products:
            serializable_product = {}
            for key, value in product.items():
                if hasattr(value, 'item'):  # numpy type
                    serializable_product[key] = value.item()
                else:
                    serializable_product[key] = value
            serializable_products.append(serializable_product)
        
        # Conditionally show products based on response type
        # For follow-up questions, don't show product details again
        if response_type == 'followup_answer':
            # Only show products if the user specifically asked for alternatives
            if any(word in message.message.lower() for word in ['alternative', 'different', 'other', 'another', 'show me']):
                # Keep products for alternative requests
                pass
            else:
                # Hide products for simple follow-up questions
                serializable_products = []
                insights = []
        
        # Calculate confidence based on response quality and LLM analysis
        confidence = 0.3  # Base confidence - start lower
        
        # Boost confidence based on response type
        if response_type == 'followup_answer':
            confidence += 0.1  # Follow-up answers are more targeted
        
        # Boost confidence based on number of products (only for new recommendations)
        if response_type == 'new_recommendation' and len(serializable_products) > 0:
            confidence += 0.2
            
        # Boost confidence based on LLM analysis availability and quality
        llm_analyzed_count = sum(1 for p in serializable_products if p.get('llm_analysis'))
        if llm_analyzed_count > 0:
            # Check quality of LLM analysis
            high_quality_matches = sum(1 for p in serializable_products 
                                     if p.get('llm_analysis', {}).get('match_score', 0) > 0.7)
            if high_quality_matches > 0:
                confidence += 0.3  # High quality matches
            else:
                confidence += 0.1  # Low quality matches
        else:
            confidence += 0.05  # No LLM analysis available
            
        # Boost confidence based on insights quality
        if insights:
            confidence += 0.1
            
        # Boost confidence based on response length (indicates more detailed response)
        if len(chat_response) > 100:
            confidence += 0.05
            
        # Cap confidence at 0.9 (90%) - more realistic
        confidence = min(0.9, confidence)
        
        return ChatResponse(
            response=chat_response,
            products=serializable_products,
            insights=insights,
            confidence=confidence
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.get("/products/search")
async def search_products(query: str, limit: int = 10):
    """Search products endpoint"""
    try:
        if not data_processor:
            raise HTTPException(status_code=500, detail="Data processor not initialized")
        
        results = data_processor.search_products(query, top_k=limit)
        return {"products": results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching products: {str(e)}")

@app.get("/products/{asin}")
async def get_product(asin: str):
    """Get specific product details"""
    try:
        if not data_processor:
            raise HTTPException(status_code=500, detail="Data processor not initialized")
        
        product = data_processor.get_product_by_asin(asin)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        reviews = data_processor.get_reviews_by_asin(asin, limit=5)
        
        return {
            "product": product.to_dict() if hasattr(product, 'to_dict') else dict(product),
            "reviews": reviews.to_dict('records') if not reviews.empty else []
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting product: {str(e)}")

@app.get("/products/{asin}/similar")
async def get_similar_products(asin: str, limit: int = 5):
    """Get similar products"""
    try:
        if not data_processor:
            raise HTTPException(status_code=500, detail="Data processor not initialized")
        
        similar_products = data_processor.get_similar_products(asin, top_k=limit)
        return {"similar_products": similar_products}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting similar products: {str(e)}")

@app.get("/analytics/overview")
async def get_analytics_overview():
    """Get analytics overview"""
    try:
        if not data_processor:
            raise HTTPException(status_code=500, detail="Data processor not initialized")
        
        products_df = data_processor.products_df
        
        return {
            "total_products": len(products_df),
            "total_reviews": len(data_processor.reviews_df),
            "total_brands": products_df['store'].nunique(),
            "total_categories": products_df['main_category'].nunique(),
            "average_rating": float(products_df['average_rating'].mean()),
            "average_price": float(products_df['price'].mean()) if 'price' in products_df.columns else 0.0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting analytics: {str(e)}")

@app.get("/analytics/top-brands")
async def get_top_brands(limit: int = 10):
    """Get top brands by product count"""
    try:
        if not data_processor:
            raise HTTPException(status_code=500, detail="Data processor not initialized")
        
        top_brands = data_processor.products_df['store'].value_counts().head(limit)
        return {"top_brands": top_brands.to_dict()}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting top brands: {str(e)}")

@app.get("/analytics/top-categories")
async def get_top_categories(limit: int = 10):
    """Get top categories by product count"""
    try:
        if not data_processor:
            raise HTTPException(status_code=500, detail="Data processor not initialized")
        
        top_categories = data_processor.products_df['main_category'].value_counts().head(limit)
        return {"top_categories": top_categories.to_dict()}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting top categories: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 