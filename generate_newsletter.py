#!/usr/bin/env python3
"""
Main Newsletter Generation Script
Orchestrates the entire newsletter creation process
Now supports manual stories from Google Sheet
"""
import os
import sys
from datetime import datetime
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from feed_aggregator import FeedAggregator
from ai_analyser import AIAnalyzer
from content_generator import ContentGenerator
from html_formatter import HTMLFormatter
from manual_stories import load_manual_stories, format_manual_stories_for_prompt

def main():
    """Main newsletter generation pipeline"""
    print("="*70)
    print(" MORTGAGELAB.AI NEWSLETTER GENERATOR")
    print("="*70)
    print(f"\nStarted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Check for API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set")
        print("Please set it with: export ANTHROPIC_API_KEY='your-api-key'")
        sys.exit(1)

    # Set up paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    feeds_config = os.path.join(base_dir, 'rss_feeds.json')
    output_dir = os.path.join(base_dir, 'output')

    # Create output directory if needed
    os.makedirs(output_dir, exist_ok=True)

    # Generate output filenames with date
    date_str = datetime.now().strftime('%Y-%m-%d')
    articles_raw_path = os.path.join(output_dir, f'articles_raw_{date_str}.json')
    articles_analyzed_path = os.path.join(output_dir, f'articles_analyzed_{date_str}.json')
    newsletter_content_path = os.path.join(output_dir, f'newsletter_content_{date_str}.txt')
    newsletter_html_path = os.path.join(output_dir, f'newsletter_{date_str}.html')

    try:
        # Step 1: Aggregate RSS Feeds
        print("\n" + "-"*70)
        print("STEP 1: Fetching RSS Feeds")
        print("-"*70)
        aggregator = FeedAggregator(feeds_config)
        articles = aggregator.fetch_all_feeds(days_back=7)
        aggregator.save_articles(articles_raw_path)

        if len(articles) == 0:
            print("\nERROR: No articles found. Check RSS feeds.")
            sys.exit(1)

        # Step 2: AI Analysis and Ranking
        print("\n" + "-"*70)
        print("STEP 2: Analysing Articles with Claude AI")
        print("-"*70)
        analyzer = AIAnalyzer(api_key)
        analyzed_articles = analyzer.analyze_articles(articles)
        top_5 = analyzer.rank_articles(analyzed_articles, top_n=5)
        analyzer.save_analysis(analyzed_articles, articles_analyzed_path)

        # Step 3: Check for Manual Stories from Google Sheet
        print("\n" + "-"*70)
        print("STEP 3: Checking for Manual Stories")
        print("-"*70)
        manual_stories = load_manual_stories()

        # Step 4: Generate Newsletter Content
        print("\n" + "-"*70)
        print("STEP 4: Generating Newsletter Content")
        print("-"*70)
        generator = ContentGenerator(api_key)
        newsletter_content = generator.generate_newsletter(top_5)

        # Append manual stories if any were found
        if manual_stories:
            print(f"  Appending {len(manual_stories)} manual story/stories...")
            manual_section = format_manual_stories_for_prompt(manual_stories)
            # Insert manual stories before the quiz section
            # Split at the quiz section and insert manual stories before it
            if '## This Week' in newsletter_content or '## SECTION 2' in newsletter_content:
                # Find where the quiz section starts
                for marker in ['## This Week', '## SECTION 2', '## Quiz']:
                    if marker in newsletter_content:
                        parts = newsletter_content.split(marker, 1)
                        newsletter_content = parts[0] + manual_section + "\n\n---\n\n" + marker + parts[1]
                        break
            else:
                # If we can't find the quiz marker, just append before the end
                newsletter_content += manual_section

        generator.save_newsletter(newsletter_content, newsletter_content_path)

        # Step 5: Format as HTML
        print("\n" + "-"*70)
        print("STEP 5: Converting to HTML for Mailchimp")
        print("-"*70)
        formatter = HTMLFormatter()

        # Calculate issue number
        import glob
        previous_newsletters = glob.glob(os.path.join(output_dir, 'newsletter_*.html'))
        issue_number = len(previous_newsletters) + 1

        html = formatter.format_newsletter(
            newsletter_content,
            metadata={
                'date': datetime.now().strftime('%B %d, %Y'),
                'issue_number': str(issue_number)
            }
        )
        formatter.save_html(html, newsletter_html_path)

        # Success!
        print("\n" + "="*70)
        print(" SUCCESS!")
        print("="*70)
        print(f"\nNewsletter generated successfully at: {datetime.now().strftime('%H:%M:%S')}")
        if manual_stories:
            print(f"  Includes {len(manual_stories)} manual story/stories from Google Sheet")
        print(f"\nOutput files:")
        print(f"  Raw articles: {articles_raw_path}")
        print(f"  Analysed articles: {articles_analyzed_path}")
        print(f"  Newsletter content: {newsletter_content_path}")
        print(f"  HTML newsletter: {newsletter_html_path}")
        print(f"\nReady for Mailchimp!")
        print("="*70)
        return 0

    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
