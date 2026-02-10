"""
HTML Formatter - Converts newsletter content to HTML for Mailchimp
With mortgagelab.ai branding - Dark Tech Theme
"""

from datetime import datetime
from typing import Dict
import re


class HTMLFormatter:
    # Brand colours - Dark Tech Theme
    BRAND_DARK_BG = "#0a0a1a"       # Outer background - deep dark navy
    BRAND_CONTENT_BG = "#141428"    # Content area - slightly lighter
    BRAND_TEXT = "#e8e8e8"          # Main body text - off-white
    BRAND_PURPLE = "#6000ff"        # Headings, links, accents (KEPT)
    BRAND_LILAC = "#cc99ff"         # Secondary accents, dividers (KEPT)
    BRAND_MUTED = "#999999"         # Footer/secondary text

    # Logo URL
    LOGO_URL = "https://raw.githubusercontent.com/pbrett44-sketch/mortgagelab-newsletter/main/mortgagelab-logo.png"

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
        """Convert markdown-style content to HTML with dark theme brand colours"""

        # Split into sections
        sections = content.split('---')

        html_parts = []

        for section in sections:
            section = section.strip()
            if not section:
                continue

            # Convert headings with brand purple
            section = re.sub(
                r'^## (.+)$',
                rf'<h2 style="color: {self.BRAND_PURPLE}; font-size: 20px; font-weight: 600; margin: 30px 0 15px 0; padding-bottom: 8px; border-bottom: 2px solid {self.BRAND_LILAC};">\1</h2>',
                section,
                flags=re.MULTILINE
            )
            section = re.sub(
                r'^\*\*(.+?)\*\*$',
                rf'<h3 style="color: {self.BRAND_TEXT}; font-size: 18px; font-weight: 600; margin: 20px 0 10px 0;">\1</h3>',
                section,
                flags=re.MULTILINE
            )

            # Convert bold text
            section = re.sub(
                r'\*\*(.+?)\*\*',
                rf'<strong style="color: {self.BRAND_TEXT}; font-weight: 600;">\1</strong>',
                section
            )

            # Convert links with brand purple
            section = re.sub(
                r'\[(.+?)\]\((.+?)\)',
                rf'<a href="\2" style="color: {self.BRAND_PURPLE}; text-decoration: none; font-weight: 500;">\1</a>',
                section
            )

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
                    formatted_paragraphs.append(
                        f'<p style="margin: 8px 0; padding-left: 15px; color: {self.BRAND_TEXT};">{para}</p>'
                    )
                else:
                    formatted_paragraphs.append(
                        f'<p style="margin: 10px 0; color: {self.BRAND_TEXT};">{para}</p>'
                    )

            html_parts.append('\n'.join(formatted_paragraphs))

        # Section divider with gradient from purple to lilac
        divider = f'''
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
    <tr>
        <td style="padding: 30px 0;">
            <div style="height: 2px; background: linear-gradient(to right, {self.BRAND_PURPLE}, {self.BRAND_LILAC}); border-radius: 2px;"></div>
        </td>
    </tr>
</table>
'''

        return divider.join(html_parts)

    def _build_html_template(self, content: str, date: str, issue_number: str) -> str:
        """Build complete HTML email template with dark tech theme"""

        html = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>mortgagelab.ai Weekly AI Newsletter</title>
    <!--[if mso]>
    <noscript>
        <xml>
            <o:OfficeDocumentSettings>
                <o:PixelsPerInch>96</o:PixelsPerInch>
            </o:OfficeDocumentSettings>
        </xml>
    </noscript>
    <![endif]-->
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: {self.BRAND_TEXT}; background-color: {self.BRAND_DARK_BG};">
    <!-- Outer wrapper with dark background -->
    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: {self.BRAND_DARK_BG};">
        <tr>
            <td align="center" style="padding: 20px 10px;">

                <!-- Inner content area -->
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="max-width: 600px; background-color: {self.BRAND_CONTENT_BG}; border-radius: 8px; overflow: hidden;">

                    <!-- Header with Logo -->
                    <tr>
                        <td align="center" style="padding: 30px 40px 20px 40px; border-bottom: 3px solid {self.BRAND_PURPLE}; background-color: {self.BRAND_CONTENT_BG};">
                            <img src="{self.LOGO_URL}" alt="mortgagelab.ai" width="180" height="180" style="display: block; width: 180px; height: auto; max-width: 180px; border: 0;">
                            <p style="margin: 15px 0 5px 0; font-size: 14px; color: {self.BRAND_TEXT};">Weekly AI Newsletter for the UK Mortgage Industry</p>
                            <p style="margin: 5px 0 0 0; font-size: 12px; color: {self.BRAND_MUTED};">Issue #{issue_number} &bull; {date}</p>
                        </td>
                    </tr>

                    <!-- Main Content -->
                    <tr>
                        <td style="padding: 30px 40px; background-color: {self.BRAND_CONTENT_BG};">
                            {content}
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td align="center" style="padding: 30px 40px; border-top: 2px solid {self.BRAND_LILAC}; background-color: {self.BRAND_CONTENT_BG};">
                            <p style="margin: 0 0 10px 0; font-size: 12px; color: {self.BRAND_MUTED};">You're receiving this because you subscribed to the mortgagelab.ai newsletter.</p>
                            <p style="margin: 0; font-size: 12px;">
                                <a href="*|UNSUB|*" style="color: {self.BRAND_PURPLE}; text-decoration: none;">Unsubscribe</a>
                                <span style="color: {self.BRAND_LILAC};"> | </span>
                                <a href="https://mortgagelab.ai" style="color: {self.BRAND_PURPLE}; text-decoration: none;">Visit mortgagelab.ai</a>
                            </p>
                        </td>
                    </tr>

                </table>
            </td>
        </tr>
    </table>
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
