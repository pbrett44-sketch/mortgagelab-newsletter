"""
HTML Formatter - Converts newsletter content to HTML for Mailchimp
"""

from datetime import datetime
from typing import Dict
import re


class HTMLFormatter:
    def __init__(self, template_path: str = None):
        """Initialize with optional custom template"""
        self.template_path = template_path
    
    def format_newsletter(self, content: str, metadata: Dict = None) -> str:
        """
        Convert plain text newsletter to HTML formatted for Mailchimp
        
        Args:
            content: Plain text newsletter content
            metadata: Optional metadata (date, issue number, etc.)
            
        Returns:
            HTML formatted newsletter
        """
        if not metadata:
            metadata = {}
        
        # Get current date for header
        date_str = metadata.get('date', datetime.now().strftime('%B %d, %Y'))
        issue_num = metadata.get('issue_number', '1')
        
        # Convert content sections to HTML
        html_content = self._convert_to_html(content)
        
        # Build complete HTML
        html = self._build_html_template(html_content, date_str, issue_num)
        
        return html
    
    def _convert_to_html(self, content: str) -> str:
        """Convert markdown-style content to HTML"""
        
        # Split into sections
        sections = content.split('---')
        
        html_parts = []
        
        for section in sections:
            section = section.strip()
            if not section:
                continue
            
            # Convert headings
            section = re.sub(r'^## (.+)$', r'<h2 class="section-title">\1</h2>', section, flags=re.MULTILINE)
            section = re.sub(r'^\*\*(.+?)\*\*$', r'<h3 class="story-title">\1</h3>', section, flags=re.MULTILINE)
            
            # Convert bold text
            section = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', section)
            
            # Convert links
            section = re.sub(r'\[(.+?)\]', r'<a href="#" class="read-more">\1</a>', section)
            
            # Convert paragraphs
            paragraphs = section.split('\n\n')
            formatted_paragraphs = []
            
            for para in paragraphs:
                para = para.strip()
                if not para:
                    continue
                
                # Check if it's already a heading
                if para.startswith('<h2') or para.startswith('<h3'):
                    formatted_paragraphs.append(para)
                # Check if it's a list item (A), B), etc.)
                elif re.match(r'^[A-D]\)', para):
                    formatted_paragraphs.append(f'<p class="quiz-option">{para}</p>')
                else:
                    formatted_paragraphs.append(f'<p>{para}</p>')
            
            html_parts.append('\n'.join(formatted_paragraphs))
        
        return '<div class="newsletter-divider"></div>\n'.join(html_parts)
    
    def _build_html_template(self, content: str, date: str, issue_number: str) -> str:
        """Build complete HTML email template"""
        
        html = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>mortgagelab.ai Weekly AI Newsletter</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: #ffffff;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #0066cc;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .logo {{
            font-size: 28px;
            font-weight: 700;
            color: #0066cc;
            margin: 0;
        }}
        .tagline {{
            color: #666;
            font-size: 14px;
            margin: 5px 0 0 0;
        }}
        .date {{
            color: #999;
            font-size: 12px;
            margin: 10px 0 0 0;
        }}
        .section-title {{
            color: #0066cc;
            font-size: 20px;
            font-weight: 600;
            margin: 30px 0 15px 0;
            padding-bottom: 8px;
            border-bottom: 2px solid #eee;
        }}
        .story-title {{
            color: #222;
            font-size: 18px;
            font-weight: 600;
            margin: 20px 0 10px 0;
        }}
        p {{
            margin: 10px 0;
            color: #444;
        }}
        strong {{
            color: #222;
            font-weight: 600;
        }}
        .read-more {{
            color: #0066cc;
            text-decoration: none;
            font-weight: 500;
        }}
        .read-more:hover {{
            text-decoration: underline;
        }}
        .newsletter-divider {{
            height: 2px;
            background: linear-gradient(to right, #0066cc, #00ccff);
            margin: 30px 0;
            border-radius: 2px;
        }}
        .quiz-option {{
            margin: 8px 0;
            padding-left: 15px;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #999;
            font-size: 12px;
        }}
        .footer a {{
            color: #0066cc;
            text-decoration: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="logo">mortgagelab.ai</h1>
            <p class="tagline">Weekly AI Newsletter for the UK Mortgage Industry</p>
            <p class="date">Issue #{issue_number} • {date}</p>
        </div>
        
        {content}
        
        <div class="footer">
            <p>You're receiving this because you subscribed to the mortgagelab.ai newsletter.</p>
            <p><a href="*|UNSUB|*">Unsubscribe</a> | <a href="https://mortgagelab.ai">Visit mortgagelab.ai</a></p>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def save_html(self, html: str, output_path: str):
        """Save HTML to file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"Saved HTML newsletter to {output_path}")


if __name__ == '__main__':
    # Test the formatter
    with open('../output/newsletter_content.txt', 'r') as f:
        content = f.read()
    
    formatter = HTMLFormatter()
    html = formatter.format_newsletter(
        content,
        metadata={
            'date': datetime.now().strftime('%B %d, %Y'),
            'issue_number': '1'
        }
    )
    
    formatter.save_html(html, '../output/newsletter.html')
    print("HTML newsletter created successfully!")
