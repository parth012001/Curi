import openai
import json
import os
from typing import List, Dict, Any, Optional
import tiktoken
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class LLMEngine:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize LLM engine with OpenAI API"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
        else:
            print("⚠️  Warning: No OpenAI API key found. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        # Initialize tokenizer for cost estimation
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        
    def is_available(self) -> bool:
        """Check if LLM is available (API key is set)"""
        return bool(self.api_key)
    
    def enhance_query(self, user_query: str, product_context: List[Dict] = None) -> str:
        """
        Transform user query into optimized search terms using LLM
        """
        if not self.is_available():
            return user_query  # Fallback to original query
        
        try:
            # Create context with beauty product categories and terms
            beauty_context = """
            Beauty product categories: cleansers, moisturizers, serums, toners, masks, exfoliators, sunscreens, 
            eye creams, face oils, lip balms, body lotions, hair care, makeup, fragrances.
            
            Skin types: sensitive, oily, dry, combination, normal, acne-prone, mature.
            
            Common concerns: anti-aging, acne, wrinkles, dark spots, hyperpigmentation, redness, dryness, oiliness.
            
            Product forms: cream, gel, lotion, serum, oil, powder, spray, stick, mask, patch.
            """
            
            prompt = f"""
            You are a beauty product expert. Transform this user query into optimized search terms for finding beauty products.
            
            {beauty_context}
            
            User query: "{user_query}"
            
            Instructions:
            1. Identify the specific product type (cleanser, moisturizer, etc.)
            2. Extract skin type and concerns
            3. Add relevant beauty terms
            4. Make it specific and searchable
            5. Return only the enhanced search terms, no explanations
            
            Enhanced search terms:
            """
            
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a beauty product search expert. Provide concise, optimized search terms."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.3
            )
            
            enhanced_query = response.choices[0].message.content.strip()
            return enhanced_query
            
        except Exception as e:
            print(f"⚠️  LLM query enhancement failed: {e}")
            return user_query
    
    def analyze_product_match(self, user_query: str, product: Dict, reviews: List[Dict] = None) -> Dict[str, Any]:
        """
        Use LLM to analyze how well a product matches the user's query
        """
        if not self.is_available():
            return {"match_score": 0.5, "reasoning": "LLM not available"}
        
        try:
            # Prepare product information
            product_info = f"""
            Product: {product.get('title', '')}
            Brand: {product.get('store', '')}
            Category: {product.get('main_category', '')}
            Average Rating: {product.get('average_rating', 0)}/5
            Number of Reviews: {product.get('rating_number', 0)}
            """
            
            # Enhanced review analysis if available
            review_analysis = ""
            if reviews:
                # Import advanced NLP analyzer for review analysis
                try:
                    from advanced_nlp_analyzer import AdvancedNLPAnalyzer
                    nlp_analyzer = AdvancedNLPAnalyzer()
                    nlp_analysis = nlp_analyzer.analyze_reviews(reviews)
                    
                    # Add advanced NLP insights to the analysis
                    review_analysis = f"""
                    Advanced Review Analysis:
                    - Sentiment: {nlp_analysis['sentiment_analysis']['average_sentiment']:.2f}
                    - Skin Types Mentioned: {list(nlp_analysis['skin_type_mentions'].keys())}
                    - Key Effects: {list(nlp_analysis['effect_analysis'].keys())}
                    - Ingredients: {nlp_analysis['ingredient_mentions']}
                    - Price Sentiment: {nlp_analysis['price_sentiment']}
                    - Key Insights: {nlp_analysis['overall_insights']}
                    """
                except ImportError:
                    # Fallback to basic review analysis
                    review_texts = []
                    for review in reviews[:3]:
                        review_texts.append(f"Review: {review.get('title', '')} - {review.get('text', '')[:200]}...")
                    review_analysis = "\nSample Reviews:\n" + "\n".join(review_texts)
            
            prompt = f"""
            Analyze how well this beauty product matches the user's query.
            
            User Query: "{user_query}"
            
            Product Information:
            {product_info}
            
            {review_analysis}
            
            Rate the match from 0-10 and explain why. Consider:
            - Product type relevance
            - Skin type compatibility (based on review mentions)
            - User concerns addressed
            - Brand reputation
            - User reviews sentiment and insights
            - Ingredient effectiveness for the user's needs
            - Price-value relationship
            
            Return a JSON response with:
            - match_score (0-10)
            - reasoning (detailed explanation)
            - key_features (list of relevant features)
            - confidence_level (high/medium/low based on review data quality)
            """
            
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a beauty product expert. Analyze product matches objectively using advanced review insights."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.2
            )
            
            # Parse JSON response
            try:
                result = json.loads(response.choices[0].message.content.strip())
                return result
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return {
                    "match_score": 0.5,
                    "reasoning": "Analysis completed but parsing failed",
                    "key_features": [],
                    "confidence_level": "medium"
                }
                
        except Exception as e:
            print(f"⚠️  LLM product analysis failed: {e}")
            return {"match_score": 0.5, "reasoning": "Analysis failed", "key_features": [], "confidence_level": "low"}
    
    def generate_response(self, user_query: str, top_products: List[Dict], analysis_results: List[Dict], context: Optional[list] = None) -> Dict[str, Any]:
        """
        Generate a context-aware conversational response using LLM
        Returns a dict with response text and response type
        """
        if not self.is_available():
            fallback_response = self._generate_fallback_response(user_query, top_products)
            return {"response": fallback_response, "response_type": "new_recommendation"}
        
        try:
            # Analyze query type and context
            query_analysis = self._analyze_query_context(user_query, context)
            
            # Prepare product summaries
            product_summaries = []
            for i, (product, analysis) in enumerate(zip(top_products[:3], analysis_results[:3])):
                summary = f"""
                Product {i+1}: {product.get('title', '')}
                Brand: {product.get('store', '')}
                Rating: {product.get('average_rating', 0)}/5 ({product.get('rating_number', 0)} reviews)
                Match Score: {analysis.get('match_score', 0)}/10
                Reasoning: {analysis.get('reasoning', '')}
                """
                product_summaries.append(summary)

            # Add conversation context if provided
            context_str = ""
            if context and isinstance(context, list):
                context_lines = []
                for msg in context:
                    role = msg.get('role', 'user')
                    who = 'You' if role == 'user' else 'Curi'
                    content = msg.get('content', '')
                    context_lines.append(f"{who}: {content}")
                context_str = "\nPrevious conversation:\n" + "\n".join(context_lines)

            # Determine response type and generate appropriate prompt
            if query_analysis['is_followup_question']:
                prompt = f"""
                You are Curi, an intelligent beauty product research assistant. The user is asking a follow-up question about a previously recommended product.
                
                {context_str}
                User Query: "{user_query}"
                
                Available Product Information:
                {chr(10).join(product_summaries)}
                
                Instructions:
                1. Answer the specific question about the product (yes/no with explanation)
                2. If you don't have enough information, say so and offer to find alternatives
                3. Be direct and helpful
                4. Don't recommend new products unless specifically asked
                5. Keep it concise and conversational
                
                Response:
                """
                response_type = "followup_answer"
            else:
                prompt = f"""
                You are Curi, an intelligent beauty product research assistant. Generate a helpful, conversational response for a new product request.
                
                {context_str}
                User Query: "{user_query}"
                
                Top Products Found:
                {chr(10).join(product_summaries)}
                
                Instructions:
                1. Highlight the best match with reasoning
                2. Mention key benefits from reviews
                3. Be conversational and helpful
                4. Keep it concise but informative
                5. Provide full product details for new recommendations
                
                Response:
                """
                response_type = "new_recommendation"
            
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Curi, a friendly and knowledgeable beauty product assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            return {
                "response": response.choices[0].message.content.strip(),
                "response_type": response_type
            }
        
        except Exception as e:
            print(f"⚠️  LLM response generation failed: {e}")
            fallback_response = self._generate_fallback_response(user_query, top_products)
            return {"response": fallback_response, "response_type": "new_recommendation"}
    
    def _analyze_query_context(self, user_query: str, context: Optional[list] = None) -> Dict[str, Any]:
        """
        Analyze if the query is a follow-up question about a previously recommended product
        """
        query_lower = user_query.lower()
        
        # Keywords that indicate follow-up questions about products
        followup_keywords = [
            'this', 'that', 'it', 'the', 'would', 'could', 'should', 'is', 'does', 'can',
            'good for', 'suitable for', 'work as', 'act as', 'daily use', 'everyday use',
            'side effects', 'ingredients', 'price', 'cost', 'rating', 'reviews'
        ]
        
        # Check if query contains follow-up indicators
        has_followup_keywords = any(keyword in query_lower for keyword in followup_keywords)
        
        # Check if there's recent context about products
        has_product_context = False
        if context and isinstance(context, list):
            recent_messages = context[-4:]  # Check last 4 messages
            for msg in recent_messages:
                content = msg.get('content', '').lower()
                if any(word in content for word in ['recommend', 'product', 'shampoo', 'moisturizer', 'serum', 'foundation']):
                    has_product_context = True
                    break
        
        is_followup_question = has_followup_keywords and has_product_context
        
        return {
            "is_followup_question": is_followup_question,
            "has_followup_keywords": has_followup_keywords,
            "has_product_context": has_product_context
        }
    
    def _generate_fallback_response(self, user_query: str, top_products: List[Dict]) -> str:
        """Fallback response when LLM is not available"""
        if not top_products:
            return f"I understand you're looking for '{user_query}', but I couldn't find any relevant products. Could you try rephrasing your request?"
        
        top_product = top_products[0]
        response = f"I found some products related to '{user_query}'. "
        response += f"My top recommendation is {top_product.get('title', '')} by {top_product.get('store', 'Unknown')} "
        response += f"(rated {top_product.get('average_rating', 0):.1f}/5 by {top_product.get('rating_number', 0)} users). "
        response += "Would you like me to show you more details about this product?"
        
        return response
    
    def extract_user_preferences(self, user_query: str) -> Dict[str, Any]:
        """
        Extract user preferences and requirements from natural language query
        """
        if not self.is_available():
            return self._extract_preferences_fallback(user_query)
        
        try:
            prompt = f"""
            Extract user preferences from this beauty product query.
            
            Query: "{user_query}"
            
            Extract and return a JSON object with:
            - product_type: (cleanser, moisturizer, serum, etc.)
            - skin_type: (sensitive, oily, dry, combination, normal, acne-prone)
            - concerns: (anti-aging, acne, wrinkles, dark spots, etc.)
            - brand_preference: (specific brands mentioned)
            - price_range: (budget, affordable, luxury, premium)
            - effects: (gentle, strong, hydrating, matte, etc.)
            - usage_time: (morning, evening, daily, weekly)
            """
            
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Extract beauty product preferences accurately."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.1
            )
            
            try:
                preferences = json.loads(response.choices[0].message.content.strip())
                return preferences
            except json.JSONDecodeError:
                return self._extract_preferences_fallback(user_query)
                
        except Exception as e:
            print(f"⚠️  LLM preference extraction failed: {e}")
            return self._extract_preferences_fallback(user_query)
    
    def _extract_preferences_fallback(self, user_query: str) -> Dict[str, Any]:
        """Fallback preference extraction using basic keyword matching"""
        query_lower = user_query.lower()
        
        preferences = {
            "product_type": None,
            "skin_type": None,
            "concerns": [],
            "brand_preference": None,
            "price_range": None,
            "effects": [],
            "usage_time": None
        }
        
        # Basic keyword extraction (same as current system)
        product_types = ['cleanser', 'moisturizer', 'serum', 'toner', 'mask', 'exfoliator', 'sunscreen']
        skin_types = ['sensitive', 'oily', 'dry', 'combination', 'normal', 'acne-prone']
        
        for product_type in product_types:
            if product_type in query_lower:
                preferences["product_type"] = product_type
                break
        
        for skin_type in skin_types:
            if skin_type in query_lower:
                preferences["skin_type"] = skin_type
                break
        
        return preferences 