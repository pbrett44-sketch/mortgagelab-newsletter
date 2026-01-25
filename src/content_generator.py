"""
Content Generator - Creates newsletter content using Claude API
"""

import os
import json
from typing import List, Dict
from anthropic import Anthropic
from datetime import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.claude_prompts import NEWSLETTER_GENERATION_PROMPT


class ContentGenerator:
    def __init__(self, api_key: str):
        """Initialize Claude API client"""
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"
    
    def generate_newsletter(self, top_articles: List[Dict]) -> str:
        """
        Generate complete newsletter content from top 5 articles
        
        Args:
            top_articles: List of top 5 ranked articles
            
        Returns:
            Complete newsletter content as plain text
        """
        print("Generating newsletter content with Claude...")
        
        # Prepare articles JSON for prompt
        articles_data = []
        for i, article in enumerate(top_articles[:5]):
            articles_data.append({
                'number': i + 1,
                'title': article['title'],
                'source': article['source'],
                'link': article['link'],
                'summary': article['summary'],
                'mortgage_angle': article.get('mortgage_angle', ''),
                'full_text': article['full_text'][:500]
            })
        
        articles_json = json.dumps(articles_data, indent=2)
        
        # Create prompt
        prompt = NEWSLETTER_GENERATION_PROMPT.format(
            articles_json=articles_json
        )
        
        # Call Claude API
        message = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        newsletter_content = message.content[0].text.strip()
        
        print("✓ Newsletter content generated successfully")
        
        return newsletter_content
    
    def save_newsletter(self, content: str, output_path: str):
        """Save newsletter content to file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Saved newsletter to {output_path}")


if __name__ == '__main__':
    # Test the generator
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        exit(1)
    
    # Load analyzed articles
    with open('../output/articles_analyzed.json', 'r') as f:
        data = json.load(f)
        articles = data['articles'][:5]
    
    generator = ContentGenerator(api_key)
    newsletter = generator.generate_newsletter(articles)
    generator.save_newsletter(newsletter, '../output/newsletter_content.txt')
    print("\n" + "="*70)
    print(newsletter)
