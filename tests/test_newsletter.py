#!/usr/bin/env python3
"""
Test Script - Run newsletter generation locally for testing
"""

import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_feeds_only():
    """Test just the RSS feed aggregation"""
    from src.feed_aggregator import FeedAggregator
    
    print("Testing RSS feed aggregation...")
    aggregator = FeedAggregator('rss_feeds.json')
    articles = aggregator.fetch_all_feeds(days_back=7)
    aggregator.save_articles('output/test_articles.json')
    
    print(f"\n✓ Successfully fetched {len(articles)} articles")
    print("\nSample articles:")
    for i, article in enumerate(articles[:3]):
        print(f"\n{i+1}. {article['title']}")
        print(f"   Source: {article['source']}")
        print(f"   Category: {article['category']}")


def test_full_pipeline():
    """Test the complete newsletter generation pipeline"""
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set")
        print("Set it with: export ANTHROPIC_API_KEY='your-key'")
        return
    
    print("Running full newsletter generation pipeline...")
    print("This will use Claude API credits.\n")
    
    # Import main function
    import generate_newsletter
    result = generate_newsletter.main()
    
    if result == 0:
        print("\n✓ Full pipeline test successful!")
    else:
        print("\n✗ Pipeline test failed")
        sys.exit(1)


def main():
    print("="*70)
    print(" NEWSLETTER SYSTEM TEST")
    print("="*70)
    print("\nChoose test mode:")
    print("1. Test RSS feeds only (no API calls)")
    print("2. Test full pipeline (uses Claude API)")
    print("\nEnter choice (1 or 2): ", end='')
    
    choice = input().strip()
    
    if choice == '1':
        test_feeds_only()
    elif choice == '2':
        test_full_pipeline()
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)


if __name__ == '__main__':
    main()
