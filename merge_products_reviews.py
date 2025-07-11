#!/usr/bin/env python3
"""
Merge the first 10,000 products from meta_sample.jsonl with their reviews from reviews_sample.jsonl.
Output: products_with_reviews.jsonl
"""
import json
from collections import defaultdict

def main():
    # Step 1: Load reviews and index by asin
    print("Loading reviews...")
    reviews_by_asin = defaultdict(list)
    with open('reviews_sample.jsonl', 'r') as f:
        for line in f:
            review = json.loads(line)
            reviews_by_asin[review['asin']].append(review)
    print(f"Loaded reviews for {len(reviews_by_asin)} products.")

    # Step 2: Merge with product metadata
    print("Merging products with reviews...")
    count = 0
    with open('meta_sample.jsonl', 'r') as fin, open('products_with_reviews.jsonl', 'w') as fout:
        for line in fin:
            if count >= 10000:
                break
            product = json.loads(line)
            asin = product['parent_asin']
            product_reviews = reviews_by_asin.get(asin, [])
            product['reviews'] = product_reviews
            fout.write(json.dumps(product) + '\n')
            count += 1
            if count % 1000 == 0:
                print(f"Processed {count} products...")
    print(f"Done! Merged {count} products into products_with_reviews.jsonl.")

if __name__ == "__main__":
    main() 