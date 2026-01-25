"""
RSS Feed Aggregator for Mortgagelab.ai Newsletter
Pulls news articles from mortgage and tech/AI sources
"""

import feedparser
import json
from datetime import datetime, timedelta
from typing import List, Dict
import requests
from bs4 import BeautifulSoup


class FeedAggregator:
    def __init__(self, feeds_config_path: str):
        """Initialize with RSS feeds configuration"""
        with open(feeds_config_path, 'r') as f:
            self.feeds_config = json.load(f)
        
        self.articles = []
    
    def fetch_all_feeds(self, days_back: int = 7) -> List[Dict]:
        """
        Fetch articles from all RSS feeds from the past N days
        
        Args:
            days_back: Number of days to look back for articles
            
        Returns:
            List of article dictionaries
        """
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        all_feeds = (
            self.feeds_config.get('mortgage_press', []) +
            self.feeds_config.get('tech_ai_news', []) +
            self.feeds_config.get('broadsheet_tech', [])
        )
        
        for feed in all_feeds:
            try:
                articles = self._fetch_feed(feed, cutoff_date)
                self.articles.extend(articles)
                print(f"✓ Fetched {len(articles)} articles from {feed['name']}")
            except Exception as e:
                print(f"✗ Error fetching {feed['name']}: {str(e)}")
        
        print(f"\nTotal articles collected: {len(self.articles)}")
        return self.articles
    
    def _fetch_feed(self, feed_config: Dict, cutoff_date: datetime) -> List[Dict]:
        """Fetch and parse a single RSS feed"""
        parsed_feed = feedparser.parse(feed_config['url'])
        articles = []
        
        for entry in parsed_feed.entries:
            # Parse publication date
            pub_date = self._parse_date(entry)
            
            # Only include recent articles
            if pub_date and pub_date < cutoff_date:
                continue
            
            # Extract article content
            content = self._extract_content(entry)
            
            article = {
                'title': entry.get('title', 'No title'),
                'link': entry.get('link', ''),
                'published': pub_date.isoformat() if pub_date else None,
                'source': feed_config['name'],
                'category': feed_config['category'],
                'summary': entry.get('summary', ''),
                'content': content,
                'full_text': f"{entry.get('title', '')}. {content}"
            }
            
            articles.append(article)
        
        return articles
    
    def _parse_date(self, entry) -> datetime:
        """Parse publication date from feed entry"""
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            return datetime(*entry.published_parsed[:6])
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            return datetime(*entry.updated_parsed[:6])
        else:
            return datetime.now()
    
    def _extract_content(self, entry) -> str:
        """Extract clean content from feed entry"""
        # Try different content fields
        content = ''
        
        if hasattr(entry, 'content') and entry.content:
            content = entry.content[0].value
        elif hasattr(entry, 'description'):
            content = entry.description
        elif hasattr(entry, 'summary'):
            content = entry.summary
        
        # Strip HTML tags
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            content = soup.get_text(separator=' ', strip=True)
        
        # Truncate to reasonable length (first 500 chars)
        return content[:500] if content else ''
    
    def save_articles(self, output_path: str):
        """Save collected articles to JSON file"""
        output_data = {
            'generated_at': datetime.now().isoformat(),
            'article_count': len(self.articles),
            'articles': self.articles
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(self.articles)} articles to {output_path}")


if __name__ == '__main__':
    # Test the aggregator
    aggregator = FeedAggregator('../rss_feeds.json')
    articles = aggregator.fetch_all_feeds(days_back=7)
    aggregator.save_articles('../output/articles_raw.json')
