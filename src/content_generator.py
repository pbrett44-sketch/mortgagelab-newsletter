"""
Content Generator - Creates newsletter content using Claude API
"""

import os
import json
import re
import unicodedata
from typing import List, Dict
from anthropic import Anthropic
from datetime import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.claude_prompts import NEWSLETTER_GENERATION_PROMPT


def sanitise_unicode(text: str) -> str:
    """
    Replace problematic unicode characters with ASCII-safe equivalents.
    Email clients (especially mobile) often mangle unicode, producing
    garbled block characters. This function catches anything Claude
    generates despite being told to use ASCII only.
    """
    replacements = {
        '\u2192': '->',   # right arrow
        '\u2190': '<-',   # left arrow
        '\u2194': '<->',  # left-right arrow
        '\u2013': '-',    # en dash
        '\u2014': '-',    # em dash
        '\u2018': "'",    # left single quote
        '\u2019': "'",    # right single quote
        '\u201c': '"',    # left double quote
        '\u201d': '"',    # right double quote
        '\u2026': '...',  # ellipsis
        '\u2022': '-',    # bullet
        '\u00a0': ' ',    # non-breaking space
        '\u200b': '',     # zero-width space
        '\u200c': '',     # zero-width non-joiner
        '\u200d': '',     # zero-width joiner
        '\ufeff': '',     # BOM
        '\u2023': '-',    # triangular bullet
        '\u25aa': '-',    # small black square
        '\u25cf': '-',    # black circle
        '\u2713': '[x]',  # check mark
        '\u2717': '[ ]',  # cross mark
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Strip any remaining emoji (Unicode blocks for emoji)
    emoji_pattern = re.compile(
        "[\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"   # misc symbols & pictographs
        "\U0001F680-\U0001F6FF"   # transport & map
        "\U0001F1E0-\U0001F1FF"   # flags
        "\U00002702-\U000027B0"   # dingbats
        "\U0001F900-\U0001F9FF"   # supplemental symbols
        "\U0001FA00-\U0001FA6F"   # chess symbols
        "\U0001FA70-\U0001FAFF"   # symbols extended-A
        "]+", flags=re.UNICODE
    )
    text = emoji_pattern.sub('', text)

    # Nuclear fallback: strip ALL remaining non-ASCII characters.
    # Mobile email clients render unsupported Unicode as black blocks.
    text = text.encode('ascii', 'ignore').decode('ascii')

    return text


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

        # Sanitise any unicode characters that slipped through
        newsletter_content = sanitise_unicode(newsletter_content)

        print("Newsletter content generated and sanitised successfully")

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
