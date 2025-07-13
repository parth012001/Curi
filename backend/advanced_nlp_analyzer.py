import spacy
import nltk
from textblob import TextBlob
from collections import Counter
import re
from typing import List, Dict, Any, Tuple
import pandas as pd

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class AdvancedNLPAnalyzer:
    def __init__(self):
        """Initialize advanced NLP analyzer"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("⚠️  spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
            
        # Beauty-specific entities and patterns
        self.beauty_entities = {
            'ingredients': [
                'vitamin c', 'hyaluronic acid', 'retinol', 'niacinamide', 'salicylic acid',
                'glycolic acid', 'peptides', 'ceramides', 'collagen', 'aloe vera',
                'tea tree oil', 'jojoba oil', 'argan oil', 'rosehip oil'
            ],
            'skin_types': [
                'oily skin', 'dry skin', 'combination skin', 'sensitive skin',
                'normal skin', 'acne-prone skin', 'mature skin'
            ],
            'concerns': [
                'acne', 'wrinkles', 'dark spots', 'hyperpigmentation', 'redness',
                'dryness', 'oiliness', 'pores', 'texture', 'aging'
            ],
            'effects': [
                'hydrating', 'matte', 'glowy', 'smooth', 'firm', 'brightening',
                'soothing', 'gentle', 'strong', 'harsh', 'irritating'
            ]
        }
        
    def analyze_reviews(self, reviews: List[Dict]) -> Dict[str, Any]:
        """
        Advanced analysis of product reviews
        """
        if not reviews:
            return self._empty_analysis()
            
        # Convert reviews to text
        review_texts = [review.get('text', '') + ' ' + review.get('title', '') for review in reviews]
        all_text = ' '.join(review_texts)
        
        analysis = {
            'sentiment_analysis': self._analyze_sentiment(review_texts),
            'entity_extraction': self._extract_entities(all_text),
            'skin_type_mentions': self._analyze_skin_type_mentions(all_text),
            'concern_analysis': self._analyze_concerns(all_text),
            'effect_analysis': self._analyze_effects(all_text),
            'price_sentiment': self._analyze_price_sentiment(all_text),
            'ingredient_mentions': self._extract_ingredients(all_text),
            'usage_patterns': self._analyze_usage_patterns(all_text),
            'overall_insights': []
        }
        
        # Generate insights
        analysis['overall_insights'] = self._generate_insights(analysis)
        
        return analysis
    
    def _analyze_sentiment(self, review_texts: List[str]) -> Dict[str, Any]:
        """Advanced sentiment analysis"""
        sentiments = []
        positive_phrases = []
        negative_phrases = []
        
        for text in review_texts:
            blob = TextBlob(text)
            sentiment_score = blob.sentiment.polarity
            
            # Extract positive and negative phrases
            for sentence in blob.sentences:
                if sentence.sentiment.polarity > 0.3:
                    positive_phrases.append(str(sentence))
                elif sentence.sentiment.polarity < -0.3:
                    negative_phrases.append(str(sentence))
            
            sentiments.append(sentiment_score)
        
        return {
            'average_sentiment': sum(sentiments) / len(sentiments) if sentiments else 0,
            'positive_phrases': positive_phrases[:3],  # Top 3 positive
            'negative_phrases': negative_phrases[:3],  # Top 3 negative
            'sentiment_distribution': {
                'positive': len([s for s in sentiments if s > 0.3]),
                'neutral': len([s for s in sentiments if -0.3 <= s <= 0.3]),
                'negative': len([s for s in sentiments if s < -0.3])
            }
        }
    
    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract beauty-specific entities"""
        if not self.nlp:
            return self._fallback_entity_extraction(text)
        
        doc = self.nlp(text.lower())
        entities = {
            'ingredients': [],
            'skin_types': [],
            'concerns': [],
            'effects': []
        }
        
        # Extract beauty-specific entities
        for entity_type, keywords in self.beauty_entities.items():
            for keyword in keywords:
                if keyword in text.lower():
                    entities[entity_type].append(keyword)
        
        # Remove duplicates
        for key in entities:
            entities[key] = list(set(entities[key]))
        
        return entities
    
    def _fallback_entity_extraction(self, text: str) -> Dict[str, List[str]]:
        """Fallback entity extraction without spaCy"""
        text_lower = text.lower()
        entities = {
            'ingredients': [],
            'skin_types': [],
            'concerns': [],
            'effects': []
        }
        
        for entity_type, keywords in self.beauty_entities.items():
            for keyword in keywords:
                if keyword in text_lower:
                    entities[entity_type].append(keyword)
        
        return entities
    
    def _analyze_skin_type_mentions(self, text: str) -> Dict[str, int]:
        """Analyze mentions of different skin types"""
        skin_mentions = {}
        text_lower = text.lower()
        
        for skin_type in self.beauty_entities['skin_types']:
            count = text_lower.count(skin_type)
            if count > 0:
                skin_mentions[skin_type] = count
        
        return skin_mentions
    
    def _analyze_concerns(self, text: str) -> Dict[str, int]:
        """Analyze mentions of skin concerns"""
        concern_mentions = {}
        text_lower = text.lower()
        
        for concern in self.beauty_entities['concerns']:
            count = text_lower.count(concern)
            if count > 0:
                concern_mentions[concern] = count
        
        return concern_mentions
    
    def _analyze_effects(self, text: str) -> Dict[str, int]:
        """Analyze mentions of product effects"""
        effect_mentions = {}
        text_lower = text.lower()
        
        for effect in self.beauty_entities['effects']:
            count = text_lower.count(effect)
            if count > 0:
                effect_mentions[effect] = count
        
        return effect_mentions
    
    def _extract_ingredients(self, text: str) -> List[str]:
        """Extract ingredient mentions"""
        text_lower = text.lower()
        ingredients = []
        
        for ingredient in self.beauty_entities['ingredients']:
            if ingredient in text_lower:
                ingredients.append(ingredient)
        
        return ingredients
    
    def _analyze_price_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze price-related sentiment"""
        price_patterns = {
            'expensive': r'\b(expensive|pricey|costly|overpriced)\b',
            'affordable': r'\b(affordable|cheap|inexpensive|budget)\b',
            'worth_it': r'\b(worth it|good value|justified)\b',
            'not_worth': r'\b(not worth|waste|overpriced)\b'
        }
        
        price_sentiment = {}
        text_lower = text.lower()
        
        for category, pattern in price_patterns.items():
            matches = re.findall(pattern, text_lower)
            price_sentiment[category] = len(matches)
        
        return price_sentiment
    
    def _analyze_usage_patterns(self, text: str) -> Dict[str, Any]:
        """Analyze usage patterns and timing"""
        usage_patterns = {
            'morning': r'\b(morning|am|day)\b',
            'evening': r'\b(evening|night|pm|bedtime)\b',
            'daily': r'\b(daily|everyday|regular)\b',
            'weekly': r'\b(weekly|once a week)\b',
            'results_time': r'\b(weeks?|months?|days?)\b'
        }
        
        usage_analysis = {}
        text_lower = text.lower()
        
        for pattern_name, pattern in usage_patterns.items():
            matches = re.findall(pattern, text_lower)
            usage_analysis[pattern_name] = len(matches)
        
        return usage_analysis
    
    def _generate_insights(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate user-friendly insights from analysis"""
        insights = []
        
        # Sentiment insights
        sentiment = analysis['sentiment_analysis']
        if sentiment['average_sentiment'] > 0.5:
            insights.append("⭐ Highly positive user sentiment")
        elif sentiment['average_sentiment'] > 0.2:
            insights.append("👍 Generally positive user feedback")
        elif sentiment['average_sentiment'] < -0.2:
            insights.append("⚠️ Mixed to negative user feedback")
        
        # Skin type insights
        skin_mentions = analysis['skin_type_mentions']
        if skin_mentions:
            top_skin_type = max(skin_mentions.items(), key=lambda x: x[1])
            insights.append(f"👥 Most mentioned for: {top_skin_type[0]} ({top_skin_type[1]} mentions)")
        
        # Effect insights
        effects = analysis['effect_analysis']
        if effects:
            top_effects = sorted(effects.items(), key=lambda x: x[1], reverse=True)[:3]
            effect_names = [effect[0] for effect in top_effects]
            insights.append(f"✨ Key effects: {', '.join(effect_names)}")
        
        # Ingredient insights
        ingredients = analysis['ingredient_mentions']
        if ingredients:
            insights.append(f"🧪 Contains: {', '.join(ingredients[:3])}")
        
        # Price insights
        price_sentiment = analysis['price_sentiment']
        if price_sentiment.get('worth_it', 0) > price_sentiment.get('not_worth', 0):
            insights.append("💰 Users say it's worth the price")
        elif price_sentiment.get('expensive', 0) > 0:
            insights.append("💸 Some users find it expensive")
        
        return insights
    
    def _empty_analysis(self) -> Dict[str, Any]:
        """Return empty analysis structure"""
        return {
            'sentiment_analysis': {'average_sentiment': 0, 'positive_phrases': [], 'negative_phrases': [], 'sentiment_distribution': {}},
            'entity_extraction': {'ingredients': [], 'skin_types': [], 'concerns': [], 'effects': []},
            'skin_type_mentions': {},
            'concern_analysis': {},
            'effect_analysis': {},
            'price_sentiment': {},
            'ingredient_mentions': [],
            'usage_patterns': {},
            'overall_insights': []
        } 