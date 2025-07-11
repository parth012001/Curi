#!/usr/bin/env python3
"""
Script to create a smaller sample dataset for testing the MVP
Extracts first 10,000 products and their corresponding reviews
"""

import json
import pandas as pd
from collections import defaultdict

def create_sample_dataset():
    """Create a smaller dataset with first 10,000 products and their reviews"""
    
    print("📊 Creating sample dataset...")
    
    # Step 1: Load and process product metadata
    print("Loading product metadata...")
    products_data = []
    product_asins = set()
    
    with open('meta_All_Beauty.jsonl', 'r') as f:
        for i, line in enumerate(f):
            if i >= 10000:  # Stop after 10,000 products
                break
            product = json.loads(line)
            products_data.append(product)
            product_asins.add(product['parent_asin'])
    
    # Save sample product metadata
    print(f"Saving {len(products_data)} products to meta_sample.jsonl...")
    with open('meta_sample.jsonl', 'w') as f:
        for product in products_data:
            f.write(json.dumps(product) + '\n')
    
    # Step 2: Extract corresponding reviews
    print("Extracting corresponding reviews...")
    reviews_data = []
    review_count = 0
    
    with open('All_Beauty.jsonl', 'r') as f:
        for line in f:
            review = json.loads(line)
            # Only include reviews for products in our sample
            if review['asin'] in product_asins:
                reviews_data.append(review)
                review_count += 1
                
                # Optional: limit total reviews to avoid memory issues
                if review_count >= 50000:  # Max 50k reviews
                    break
    
    # Save sample reviews
    print(f"Saving {len(reviews_data)} reviews to reviews_sample.jsonl...")
    with open('reviews_sample.jsonl', 'w') as f:
        for review in reviews_data:
            f.write(json.dumps(review) + '\n')
    
    # Step 3: Create sample ratings CSV
    print("Creating sample ratings CSV...")
    ratings_data = []
    for review in reviews_data:
        ratings_data.append({
            'UserId': review['user_id'],
            'ProductId': review['asin'],
            'Rating': review['rating'],
            'Timestamp': review['timestamp']
        })
    
    ratings_df = pd.DataFrame(ratings_data)
    ratings_df.to_csv('ratings_sample.csv', index=False)
    
    # Step 4: Print statistics
    print("\n📈 Sample Dataset Statistics:")
    print(f"Products: {len(products_data):,}")
    print(f"Reviews: {len(reviews_data):,}")
    print(f"Ratings: {len(ratings_data):,}")
    
    # Count unique users
    unique_users = len(set(review['user_id'] for review in reviews_data))
    print(f"Unique Users: {unique_users:,}")
    
    # Show some product examples
    print("\n📦 Sample Products:")
    for i, product in enumerate(products_data[:5]):
        print(f"  {i+1}. {product['title'][:60]}...")
        print(f"     Brand: {product.get('store', 'Unknown')}")
        print(f"     Rating: {product.get('average_rating', 'N/A')}/5")
        print()
    
    # Show review distribution
    review_counts = defaultdict(int)
    for review in reviews_data:
        review_counts[review['asin']] += 1
    
    avg_reviews = sum(review_counts.values()) / len(review_counts) if review_counts else 0
    print(f"Average reviews per product: {avg_reviews:.1f}")
    print(f"Products with reviews: {len(review_counts)}")
    
    print("\n✅ Sample dataset created successfully!")
    print("Files created:")
    print("  - meta_sample.jsonl (product metadata)")
    print("  - reviews_sample.jsonl (reviews)")
    print("  - ratings_sample.csv (ratings)")
    
    return len(products_data), len(reviews_data), len(ratings_data)

if __name__ == "__main__":
    create_sample_dataset() 