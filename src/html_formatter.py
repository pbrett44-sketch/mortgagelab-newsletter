"""
HTML Formatter - Converts newsletter content to HTML for Mailchimp.
With mortgagelab.ai branding.
"""
from datetime import datetime
from typing import Dict
import re


class HTMLFormatter:
      """Formats newsletter content as HTML with mortgagelab.ai branding."""

    BRAND_BLACK = "#000000"
    BRAND_WHITE = "#ffffff"
    BRAND_PURPLE = "#6000ff"
    BRAND_LILAC = "#cc99ff"
    LOGO_URL = "https://raw.githubusercontent.com/pbrett44-sketch/mortgagelab-newsletter/main/mortgagelab-logo.png"

    def __init__(self, template_path=None):
              """Initialize with optional custom template."""
              self.template_path = template_path

    def format_newsletter(self, content, metadata=None):
              """Convert plain text newsletter to HTML formatted for Mailchimp."""
              if not metadata:
                            metadata = {}
                        date_str = metadata.get("date", datetime.now().strftime("%B %d, %Y"))
        issue_num = metadata.get("issue_number", "1")
        html_content = self._convert_to_html(content)
        return self._build_html_template(html_content, date_str, issue_num)

    def _convert_to_html(self, content):
              """Convert markdown-style content to HTML with brand colours."""
        sections = content.split("---")
        html_parts = []
        for section in sections:
                      section = section.strip()
                      if not section:
                                        continue
                                    section = re.sub(
                                                      r"^## (.+)$",
                                                      r'<h2 style="color:#6000ff;font-size:20px;font-weight:600;margin:30px 0 15px 0;padding-bottom:8px;border-bottom:2px solid #cc99ff;">\1</h2>',
                                                      section,
                                                      flags=re.MULTILINE,
                                    )
            section = re.sub(
                              r"^\*\*(.+?)\*\*$",
                              r'<h3 style="color:#000000;font-size:18px;font-weight:600;margin:20px 0 10px 0;">\1</h3>',
                              section,
                              flags=re.MULTILINE,
            )
            section = re.sub(
                              r"\*\*(.+?)\*\*",
                              r'<strong style="color:#000000;font-weight:600;">\1</strong>',
                              section,
            )
            section = re.sub(
                              r"\[(.+?)\]\((.+?)\)",
                              r'<a href="\2" style="color:#6000ff;text-decoration:none;font-weight:500;">\1</a>',
                              section,
            )
            paragraphs = section.split("\n\n")
            formatted = []
            for para in paragraphs:
                              para = para.strip()
                              if not para:
                                                    continue
                                                if para.startswith("<h2") or para.startswith("<h3"):
                                                                      formatted.append(para)
elif re.match(r"^[A-D]\)", para):
                    formatted.append(f'<p style="margin:8px 0;padding-left:15px;color:#000000;">{para}</p>')
else:
                    formatted.append(f'<p style="margin:10px 0;color:#000000;">{para}</p>')
            html_parts.append("\n".join(formatted))
        divider = '<table role="presentation" width="100%"><tr><td style="padding:30px 0;"><div style="height:2px;background:linear-gradient(to right,#6000ff,#cc99ff);"></div></td></tr></table>'
        return divider.join(html_parts)

    def _build_html_template(self, content, date, issue_number):
              """Build complete HTML email template with mortgagelab.ai branding."""
        return f"""<!DOCTYPE html>
        <html lang="en-GB">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width,initial-scale=1.0">
        <title>mortgagelab.ai Weekly AI Newsletter</title>
        </head>
        <body style="margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;line-height:1.6;color:#000000;background-color:#ffffff;">
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color:#ffffff;">
        <tr>
        <td align="center" style="padding:20px 10px;">
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="max-width:600px;background-color:#ffffff;">
        <tr>
        <td align="center" style="padding:30px 40px 20px 40px;border-bottom:3px solid #6000ff;">
        <img src="{self.LOGO_URL}" alt="mortgagelab.ai" width="180" style="display:block;width:180px;height:auto;border:0;">
        <p style="margin:15px 0 5px 0;font-size:14px;color:#000000;">Weekly AI Newsletter for the UK Mortgage Industry</p>
        <p style="margin:5px 0 0 0;font-size:12px;color:#666666;">Issue #{issue_number} - {date}</p>
        </td>
        </tr>
        <tr>
        <td style="padding:30px 40px;">
        {content}
        </td>
        </tr>
        <tr>
        <td align="center" style="padding:30px 40px;border-top:2px solid #cc99ff;">
        <p style="margin:0 0 10px 0;font-size:12px;color:#666666;">You are receiving this because you subscribed to the mortgagelab.ai newsletter.</p>
        <p style="margin:0;font-size:12px;">
        <a href="*|UNSUB|*" style="color:#6000ff;text-decoration:none;">Unsubscribe</a>
        <span style="color:#cc99ff;"> | </span>
        <a href="https://mortgagelab.ai" style="color:#6000ff;text-decoration:none;">Visit mortgagelab.ai</a>
        </p>
        </td>
        </tr>
        </table>
        </td>
        </tr>
        </table>
        </body>
        </html>"""

            def save_html(self, html, output_path):
                    """Save HTML to file."""
                            with open(output_path, "w", encoding="utf-8") as f:
                                        f.write(html)
                                                print(f"Saved HTML newsletter to {output_path}")


                                                if __name__ == "__main__":
                                                    with open("../output/newsletter_content.txt", "r") as f:
                                                            content = f.read()
                                                                formatter = HTMLFormatter()
                                                                    html = formatter.format_newsletter(
                                                                            content,
                                                                                    metadata={"date": datetime.now().strftime("%B %d, %Y"), "issue_number": "1"},
                                                                                        )
                                                                                            formatter.save_html(html, "../output/newsletter.html")
                                                                                                print("HTML newsletter created successfully!")
