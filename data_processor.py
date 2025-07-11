import pandas as pd
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import linear_kernel
import pickle
import os

class BeautyDataProcessor:
    def __init__(self):
        self.products_df = None
        self.reviews_df = None
        self.ratings_df = None
        self.product_similarity_matrix = None
        self.user_similarity_matrix = None
        self.tfidf_matrix = None
        self.tfidf_vectorizer = None
        
    def load_data(self):
        """Load all three data sources"""
        print("Loading product metadata...")
        # Load product metadata
        products_data = []
        
        # Try to load sample data first, fall back to full data
        try:
            with open('meta_sample.jsonl', 'r') as f:
                for line in f:
                    products_data.append(json.loads(line))
            print("Using sample dataset...")
        except FileNotFoundError:
            with open('meta_All_Beauty.jsonl', 'r') as f:
                for line in f:
                    products_data.append(json.loads(line))
            print("Using full dataset...")
            
        self.products_df = pd.DataFrame(products_data)
        
        print("Loading reviews and ratings...")
        # Load reviews (which contain ratings)
        reviews_data = []
        
        try:
            with open('reviews_sample.jsonl', 'r') as f:
                for line in f:
                    reviews_data.append(json.loads(line))
        except FileNotFoundError:
            with open('All_Beauty.jsonl', 'r') as f:
                for line in f:
                    reviews_data.append(json.loads(line))
                    
        self.reviews_df = pd.DataFrame(reviews_data)
        
        # Create ratings dataframe from reviews
        print("Creating ratings dataframe from reviews...")
        self.ratings_df = self.reviews_df[['user_id', 'asin', 'rating', 'timestamp']].copy()
        self.ratings_df.columns = ['UserId', 'ProductId', 'Rating', 'Timestamp']
        
        print(f"Loaded {len(self.products_df)} products, {len(self.reviews_df)} reviews, {len(self.ratings_df)} ratings")
        
    def preprocess_data(self):
        """Clean and prepare data for analysis"""
        print("Preprocessing data...")
        
        # Clean product data
        self.products_df = self.products_df.dropna(subset=['title', 'parent_asin'])
        self.products_df['title'] = self.products_df['title'].astype(str)
        self.products_df['average_rating'] = pd.to_numeric(self.products_df['average_rating'], errors='coerce')
        self.products_df['rating_number'] = pd.to_numeric(self.products_df['rating_number'], errors='coerce')
        
        # Clean reviews data
        self.reviews_df = self.reviews_df.dropna(subset=['text', 'title', 'asin'])
        self.reviews_df['text'] = self.reviews_df['text'].astype(str)
        self.reviews_df['title'] = self.reviews_df['title'].astype(str)
        
        # Clean ratings data
        self.ratings_df = self.ratings_df.dropna()
        
        print("Data preprocessing completed")
        
    def create_product_features(self):
        """Create comprehensive product features for similarity matching"""
        print("Creating product features...")
        
        # Combine product information
        self.products_df['combined_features'] = (
            self.products_df['title'].fillna('') + ' ' +
            self.products_df['store'].fillna('') + ' ' +
            self.products_df['main_category'].fillna('')
        )
        
        # Add details if available
        def extract_details(details):
            if isinstance(details, dict):
                return ' '.join([f"{k}: {v}" for k, v in details.items()])
            return ''
        
        self.products_df['details_text'] = self.products_df['details'].apply(extract_details)
        self.products_df['combined_features'] += ' ' + self.products_df['details_text']
        
        print("Product features created")
        
    def build_tfidf_matrix(self):
        """Build TF-IDF matrix for text-based similarity"""
        print("Building TF-IDF matrix...")
        
        # Combine all text features
        text_features = self.products_df['combined_features'].fillna('')
        
        # Create TF-IDF vectorizer
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2
        )
        
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(text_features)
        print(f"TF-IDF matrix shape: {self.tfidf_matrix.shape}")
        
    def build_similarity_matrices(self):
        """Build product and user similarity matrices"""
        print("Building similarity matrices...")
        
        # For MVP testing, skip the memory-intensive similarity matrices
        # These can be computed on-demand when needed
        print("Skipping similarity matrix building for MVP testing...")
        self.product_similarity_matrix = None
        self.user_similarity_matrix = None
        
        print("Similarity matrices skipped (will be computed on-demand)")
        
    def get_product_by_asin(self, asin):
        """Get product information by ASIN"""
        df = self.products_df[self.products_df['parent_asin'] == asin]
        if df.empty:
            return None
        return df.iloc[0]
        
    def get_reviews_by_asin(self, asin, limit=5):
        """Get reviews for a specific product"""
        product_reviews = self.reviews_df[self.reviews_df['asin'] == asin]
        return product_reviews.sort_values('helpful_vote', ascending=False).head(limit)
        
    def search_products(self, query, top_k=10):
        """Search products based on text query"""
        # Transform query using TF-IDF
        query_vector = self.tfidf_vectorizer.transform([query])
        
        # Calculate similarity with all products
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Get top matches
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0:
                product = self.products_df.iloc[idx]
                results.append({
                    'asin': product['parent_asin'],
                    'title': product['title'],
                    'store': product['store'],
                    'average_rating': product['average_rating'],
                    'rating_number': product['rating_number'],
                    'similarity_score': similarities[idx]
                })
        
        return results
        
    def get_similar_products(self, asin, top_k=5):
        """Get similar products based on product similarity"""
        # For MVP, return products with similar ratings and categories
        target_product = self.products_df[self.products_df['parent_asin'] == asin]
        if len(target_product) == 0:
            return []
            
        target_product = target_product.iloc[0]
        target_rating = target_product.get('average_rating', 0)
        target_store = target_product.get('store', '')
        
        # Find products with similar ratings and same brand
        similar_products = self.products_df[
            (self.products_df['parent_asin'] != asin) &
            (self.products_df['average_rating'] >= target_rating - 0.5) &
            (self.products_df['average_rating'] <= target_rating + 0.5)
        ].head(top_k)
        
        results = []
        for _, product in similar_products.iterrows():
            results.append({
                'asin': product['parent_asin'],
                'title': product['title'],
                'store': product['store'],
                'average_rating': product['average_rating'],
                'similarity_score': 0.8  # Placeholder
            })
        
        return results
        
    def get_user_recommendations(self, user_id, top_k=10):
        """Get personalized recommendations for a user"""
        # For MVP, return popular products with high ratings
        return self.get_popular_products(top_k)
        
    def get_popular_products(self, top_k=10):
        """Get most popular products based on rating count and average rating"""
        popular = self.products_df.nlargest(top_k, 'rating_number')
        return [{
            'asin': row['parent_asin'],
            'title': row['title'],
            'store': row['store'],
            'average_rating': row['average_rating'],
            'rating_number': row['rating_number']
        } for _, row in popular.iterrows()]
        
    def save_processed_data(self):
        """Save processed data for faster loading"""
        print("Saving processed data...")
        with open('processed_data.pkl', 'wb') as f:
            pickle.dump({
                'products_df': self.products_df,
                'reviews_df': self.reviews_df,
                'ratings_df': self.ratings_df,
                'product_similarity_matrix': self.product_similarity_matrix,
                'user_similarity_matrix': self.user_similarity_matrix,
                'tfidf_matrix': self.tfidf_matrix,
                'tfidf_vectorizer': self.tfidf_vectorizer
            }, f)
        print("Data saved successfully")
        
    def load_processed_data(self):
        """Load previously processed data"""
        if os.path.exists('processed_data.pkl'):
            print("Loading processed data...")
            with open('processed_data.pkl', 'rb') as f:
                data = pickle.load(f)
                self.products_df = data['products_df']
                self.reviews_df = data['reviews_df']
                self.ratings_df = data['ratings_df']
                self.product_similarity_matrix = data['product_similarity_matrix']
                self.user_similarity_matrix = data['user_similarity_matrix']
                self.tfidf_matrix = data['tfidf_matrix']
                self.tfidf_vectorizer = data['tfidf_vectorizer']
            print("Processed data loaded successfully")
            return True
        return False 