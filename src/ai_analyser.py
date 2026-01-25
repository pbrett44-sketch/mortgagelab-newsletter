"""
AI Analyzer - Uses Claude API to score and rank articles
"""

import os
import json
from typing import List, Dict
from anthropic import Anthropic
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.claude_prompts import RELEVANCE_ANALYSIS_PROMPT


class AIAnalyzer:
    def __init__(self, api_key: str):
        """Initialize Claude API client"""
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"
    
    def analyze_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        Analyze all articles for relevance to UK mortgage industry
        
        Args:
            articles: List of article dictionaries
            
        Returns:
            Articles with added relevance scores
        """
        analyzed_articles = []
        
        for i, article in enumerate(articles):
            print(f"Analyzing article {i+1}/{len(articles)}: {article['title'][:60]}...")
            
            try:
                scores = self._analyze_single_article(article)
                article.update(scores)
                analyzed_articles.append(article)
            except Exception as e:
                print(f"  Error analyzing article: {str(e)}")
                # Add default low scores for failed analysis
                article.update({
                    'relevance_score': 1,
                    'mortgage_relevance': 1,
                    'ai_focus': 1,
                    'uk_applicability': 1,
                    'timeliness': 1,
                    'reasoning': 'Analysis failed',
                    'mortgage_angle': 'Not analyzed'
                })
                analyzed_articles.append(article)
        
        return analyzed_articles
    
    def _analyze_single_article(self, article: Dict) -> Dict:
        """Use Claude to analyze a single article"""
        
        # Prepare the prompt
        prompt = RELEVANCE_ANALYSIS_PROMPT.format(
            title=article['title'],
            source=article['source'],
            content=article['full_text'][:1000]  # Limit content length
        )
        
        # Call Claude API
        message = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Parse JSON response
        response_text = message.content[0].text.strip()
        
        # Handle potential JSON formatting issues
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0].strip()
        
        scores = json.loads(response_text)
        
        print(f"  Score: {scores['relevance_score']}/10 - {scores['reasoning'][:60]}...")
        
        return scores
    
    def rank_articles(self, articles: List[Dict], top_n: int = 5) -> List[Dict]:
        """
        Rank articles by relevance score and return top N
        
        Args:
            articles: List of analyzed articles
            top_n: Number of top articles to return
            
        Returns:
            Top N articles sorted by relevance
        """
        # Sort by relevance_score descending
        sorted_articles = sorted(
            articles, 
            key=lambda x: x.get('relevance_score', 0), 
            reverse=True
        )
        
        top_articles = sorted_articles[:top_n]
        
        print(f"\nTop {top_n} articles selected:")
        for i, article in enumerate(top_articles):
            print(f"{i+1}. [{article['relevance_score']}/10] {article['title'][:70]}")
        
        return top_articles
    
    def save_analysis(self, articles: List[Dict], output_path: str):
        """Save analyzed articles to JSON"""
        output_data = {
            'analyzed_at': json.dumps(None),  # Will be set when called
            'article_count': len(articles),
            'articles': articles
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved analysis of {len(articles)} articles to {output_path}")


if __name__ == '__main__':
    # Test the analyzer
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        exit(1)
    
    # Load sample articles
    with open('../output/articles_raw.json', 'r') as f:
        data = json.load(f)
        articles = data['articles'][:3]  # Test with first 3
    
    analyzer = AIAnalyzer(api_key)
    analyzed = analyzer.analyze_articles(articles)
    top_5 = analyzer.rank_articles(analyzed, top_n=5)
    analyzer.save_analysis(analyzed, '../output/articles_analyzed.json')
