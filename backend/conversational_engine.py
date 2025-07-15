import re
import nltk
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
from llm_engine import LLMEngine
from advanced_nlp_analyzer import AdvancedNLPAnalyzer

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class ConversationalEngine:
    def __init__(self, data_processor, llm_engine=None):
        self.data_processor = data_processor
        self.llm_engine = llm_engine or LLMEngine()
        self.nlp_analyzer = AdvancedNLPAnalyzer()
        self.stop_words = set(stopwords.words('english'))
        
        # Define beauty-related keywords and categories
        self.beauty_keywords = {
            'skin_type': ['sensitive', 'oily', 'dry', 'combination', 'normal', 'acne-prone'],
            'product_type': ['cleanser', 'moisturizer', 'serum', 'toner', 'mask', 'exfoliator', 'sunscreen'],
            'concern': ['anti-aging', 'acne', 'wrinkles', 'dark spots', 'hyperpigmentation', 'redness'],
            'brand': ['cerave', 'neutrogena', 'la roche-posay', 'the ordinary', 'paula\'s choice'],
            'price': ['budget', 'affordable', 'expensive', 'luxury', 'premium'],
            'effect': ['gentle', 'strong', 'harsh', 'soothing', 'hydrating', 'matte']
        }
        
    def extract_intent(self, query):
        """Extract user intent from natural language query"""
        query_lower = query.lower()
        
        # Define intent patterns
        intent_patterns = {
            'search': r'\b(find|search|look for|recommend|suggest)\b',
            'compare': r'\b(compare|vs|versus|difference between)\b',
            'review': r'\b(review|opinion|experience|thoughts)\b',
            'price': r'\b(price|cost|budget|affordable|expensive)\b',
            'specific': r'\b(specific|particular|exact)\b'
        }
        
        for intent, pattern in intent_patterns.items():
            if re.search(pattern, query_lower):
                return intent
                
        return 'search'  # Default intent
        
    def extract_features(self, query):
        """Extract product features and preferences from query"""
        # Use LLM for better feature extraction if available
        if self.llm_engine.is_available():
            preferences = self.llm_engine.extract_user_preferences(query)
            return self._convert_preferences_to_features(preferences)
        
        # Fallback to original keyword-based extraction
        return self._extract_features_keyword_based(query)
    
    def _convert_preferences_to_features(self, preferences):
        """Convert LLM preferences to features format"""
        features = {}
        
        if preferences.get('product_type'):
            features['product_type'] = preferences['product_type']
        
        if preferences.get('skin_type'):
            features['skin_type'] = preferences['skin_type']
        
        if preferences.get('concerns'):
            features['concerns'] = preferences['concerns']
        
        if preferences.get('brand_preference'):
            features['brands'] = [preferences['brand_preference']]
        
        if preferences.get('price_range'):
            features['price_range'] = preferences['price_range']
        
        if preferences.get('effects'):
            features['effects'] = preferences['effects']
        
        return features
    
    def _extract_features_keyword_based(self, query):
        """Original keyword-based feature extraction"""
        query_lower = query.lower()
        extracted_features = {}
        
        # Extract skin type
        for skin_type in self.beauty_keywords['skin_type']:
            if skin_type in query_lower:
                extracted_features['skin_type'] = skin_type
                break
                
        # Extract product type
        for product_type in self.beauty_keywords['product_type']:
            if product_type in query_lower:
                extracted_features['product_type'] = product_type
                break
                
        # Extract concerns
        concerns = []
        for concern in self.beauty_keywords['concern']:
            if concern in query_lower:
                concerns.append(concern)
        if concerns:
            extracted_features['concerns'] = concerns
            
        # Extract brand preferences
        brands = []
        for brand in self.beauty_keywords['brand']:
            if brand in query_lower:
                brands.append(brand)
        if brands:
            extracted_features['brands'] = brands
            
        # Extract price preferences
        for price_term in self.beauty_keywords['price']:
            if price_term in query_lower:
                extracted_features['price_range'] = price_term
                break
                
        # Extract effects
        effects = []
        for effect in self.beauty_keywords['effect']:
            if effect in query_lower:
                effects.append(effect)
        if effects:
            extracted_features['effects'] = effects
            
        return extracted_features
        
    def enhance_query(self, query, features):
        """Enhance the search query based on extracted features"""
        # Use LLM for query enhancement if available
        if self.llm_engine.is_available():
            return self.llm_engine.enhance_query(query)
        
        # Fallback to original enhancement
        enhanced_terms = []
        
        # Add skin type context
        if 'skin_type' in features:
            enhanced_terms.append(f"{features['skin_type']} skin")
            
        # Add product type
        if 'product_type' in features:
            enhanced_terms.append(features['product_type'])
            
        # Add concerns
        if 'concerns' in features:
            for concern in features['concerns']:
                enhanced_terms.append(concern)
                
        # Add effects
        if 'effects' in features:
            for effect in features['effects']:
                enhanced_terms.append(effect)
                
        # Combine original query with enhanced terms
        enhanced_query = query + ' ' + ' '.join(enhanced_terms)
        return enhanced_query
        
    def get_smart_recommendations(self, query, top_k=10):
        """Get intelligent recommendations based on natural language query"""
        # Extract intent and features
        intent = self.extract_intent(query)
        features = self.extract_features(query)
        
        # Enhance query
        enhanced_query = self.enhance_query(query, features)
        
        # Get base search results
        search_results = self.data_processor.search_products(enhanced_query, top_k=top_k)
        
        # Apply additional filtering based on features
        filtered_results = self.apply_feature_filters(search_results, features)
        
        # Use LLM to analyze and rank products if available
        if self.llm_engine.is_available():
            analysis_results = []
            for result in filtered_results[:5]:  # Analyze top 5 for efficiency
                # Get product details and reviews
                product = self.data_processor.get_product_by_asin(result['asin'])
                reviews = self.data_processor.get_reviews_by_asin(result['asin'], limit=3)
                
                if product is not None:
                    analysis = self.llm_engine.analyze_product_match(query, product, reviews.to_dict('records') if not reviews.empty else None)
                    
                    # Normalize match score from 0-10 to 0-1 scale
                    if 'match_score' in analysis:
                        # Convert from 0-10 scale to 0-1 scale
                        raw_score = analysis['match_score']
                        if isinstance(raw_score, (int, float)):
                            # Ensure score is within 0-10 range first
                            raw_score = max(0, min(10, raw_score))
                            # Convert to 0-1 scale
                            analysis['match_score'] = raw_score / 10.0
                        else:
                            analysis['match_score'] = 0.5  # Default if invalid
                    
                    analysis_results.append(analysis)
                    result['llm_analysis'] = analysis
                else:
                    analysis_results.append({"match_score": 0.5, "reasoning": "Product not found"})
            
            # Sort by LLM match score if available
            if analysis_results:
                filtered_results = sorted(filtered_results, 
                                       key=lambda x: x.get('llm_analysis', {}).get('match_score', 0), 
                                       reverse=True)
        
        # Add user insights and reviews
        enriched_results = self.enrich_with_insights(filtered_results)
        
        return {
            'query': query,
            'intent': intent,
            'features': features,
            'recommendations': enriched_results,
            'enhanced_query': enhanced_query
        }
        
    def apply_feature_filters(self, results, features):
        """Apply additional filtering based on extracted features"""
        if not features:
            return results
            
        filtered_results = []
        
        for result in results:
            product = self.data_processor.get_product_by_asin(result['asin'])
            if product is None:
                continue
                
            # Check brand preferences
            if 'brands' in features:
                product_brand = product.get('store', '').lower() if isinstance(product, dict) else str(product['store']).lower()
                if not any(brand in product_brand for brand in features['brands']):
                    continue
                    
            # Check price range (if we had price data)
            if 'price_range' in features:
                # This would require price data in the product metadata
                pass
                
            filtered_results.append(result)
            
        return filtered_results if filtered_results else results
        
    def enrich_with_insights(self, results):
        """Add user insights and reviews to recommendations using advanced NLP"""
        enriched_results = []
        
        for result in results:
            # Get reviews for this product
            reviews = self.data_processor.get_reviews_by_asin(result['asin'], limit=5)
            
            # Use advanced NLP analysis
            if not reviews.empty:
                review_data = reviews.to_dict('records')
                nlp_analysis = self.nlp_analyzer.analyze_reviews(review_data)
                
                # Add to result
                enriched_result = result.copy()
                enriched_result['insights'] = nlp_analysis['overall_insights']
                enriched_result['review_count'] = len(reviews)
                enriched_result['nlp_analysis'] = nlp_analysis
            else:
                # No reviews available
                enriched_result = result.copy()
                enriched_result['insights'] = []
                enriched_result['review_count'] = 0
                enriched_result['nlp_analysis'] = self.nlp_analyzer._empty_analysis()
            
            enriched_results.append(enriched_result)
            
        return enriched_results
        
    def extract_review_insights(self, reviews):
        """Extract key insights from reviews using advanced NLP"""
        if reviews.empty:
            return []
        
        # Use advanced NLP analyzer
        review_data = reviews.to_dict('records')
        nlp_analysis = self.nlp_analyzer.analyze_reviews(review_data)
        
        return nlp_analysis['overall_insights']
        
    def extract_themes(self, text):
        """Extract common themes from text using advanced NLP"""
        # This method is now deprecated in favor of advanced NLP
        # Keeping for backward compatibility
        return []
        
    def get_conversational_response(self, query, history=None):
        """Generate a conversational response with recommendations, using session-based memory if history is provided"""
        # Use the last N messages for context
        context_messages = []
        if history and isinstance(history, list):
            context_messages = history[-6:]  # Use last 6 messages for context

        analysis = self.get_smart_recommendations(query)

        # Generate natural language response
        if self.llm_engine.is_available():
            # Use LLM for response generation
            top_products = analysis['recommendations'][:3]  # Top 3 products
            analysis_results = [product.get('llm_analysis', {}) for product in top_products]
            llm_response = self.llm_engine.generate_response(query, top_products, analysis_results, context=context_messages)
            
            # Handle new response format
            if isinstance(llm_response, dict):
                response_text = llm_response.get('response', '')
                response_type = llm_response.get('response_type', 'new_recommendation')
            else:
                # Backward compatibility for old format
                response_text = llm_response
                response_type = 'new_recommendation'
        else:
            # Use fallback response generation
            response_text = self.generate_response(analysis)
            response_type = 'new_recommendation'

        return {
            'response': response_text,
            'response_type': response_type,
            'recommendations': analysis['recommendations'],
            'intent': analysis['intent'],
            'features': analysis['features'],
            'enhanced_query': analysis.get('enhanced_query', query)
        }
        
    def generate_response(self, analysis):
        """Generate a natural language response (fallback)"""
        query = analysis['query']
        intent = analysis['intent']
        features = analysis['features']
        recommendations = analysis['recommendations']
        
        # Start with acknowledgment and context
        response = f"I found some beauty products related to '{query}'. "
        
        # Add context based on extracted features
        if features.get('skin_type'):
            response += f"I've focused on products suitable for {features['skin_type']} skin. "
            
        if features.get('product_type'):
            response += f"I'm showing you the best {features['product_type']} options. "
            
        if features.get('concerns'):
            concerns = ', '.join(features['concerns'])
            response += f"I've considered your concerns about {concerns}. "
            
        # Add recommendation count and highlight top choice
        if recommendations:
            response += f"I found {len(recommendations)} options for you. "
            
            top_rec = recommendations[0]
            
            # Check if we have LLM analysis for the top product
            if 'llm_analysis' in top_rec and top_rec['llm_analysis']:
                match_score = top_rec['llm_analysis'].get('match_score', 0)
                reasoning = top_rec['llm_analysis'].get('reasoning', '')
                
                # Only recommend if match score is reasonable
                if match_score > 0.6:  # 60% or higher
                    response += f"My top recommendation is **{top_rec['title']}** by {top_rec['store']}. "
                    response += f"This product has a rating of {top_rec['average_rating']:.1f}/5 from {top_rec['rating_number']} users. "
                    
                    if reasoning:
                        response += f"Here's why this matches your needs: {reasoning} "
                else:
                    response += f"I found some related products, though they may not be perfect matches for your specific needs. "
                    response += f"The top result is {top_rec['title']} by {top_rec['store']} "
                    response += f"(rated {top_rec['average_rating']:.1f}/5 by {top_rec['rating_number']} users). "
            else:
                # No LLM analysis available
                response += f"My top recommendation is **{top_rec['title']}** by {top_rec['store']}. "
                response += f"This product has a rating of {top_rec['average_rating']:.1f}/5 from {top_rec['rating_number']} users. "
            
            # Add insights if available
            if 'insights' in top_rec and top_rec['insights']:
                response += f"Key feedback from users: {top_rec['insights'][0]} "
                
            response += "I've included other options below for you to compare."
        else:
            response += "I couldn't find exact matches, but I've included some related products that might interest you."
        
        return response 