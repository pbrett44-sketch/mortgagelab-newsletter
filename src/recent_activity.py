"""
Recent Activity Loader - Fetches Mortgage Lab's own news (podcasts out or
coming up, events we're attending) from the "Recent Activity" tab of the
same Google Sheet that holds the manual stories. Paul types a row per item
and this module picks them up on the next newsletter run.
"""

import csv
import io
import os
import requests
from typing import List, Dict
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

from html_formatter import HTMLFormatter

# gid of the "Recent Activity" tab in the Newsletter Manual Stories sheet
# (added 22 Oct 2026). The sheet URL itself stays in the GOOGLE_SHEET_CSV_URL
# secret; only the tab id lives here.
ACTIVITY_TAB_GID = '257547497'

SECTION_TITLE = 'Recent Activity from Mortgage Lab'


def activity_csv_url(stories_csv_url: str) -> str:
    """Point the manual-stories CSV URL at the Recent Activity tab instead."""
    parts = urlsplit(stories_csv_url)
    query = dict(parse_qsl(parts.query))
    query['gid'] = ACTIVITY_TAB_GID
    if '/pub' in parts.path:
        # "Publish to web" links export every tab unless told otherwise
        query['single'] = 'true'
    return urlunsplit(parts._replace(query=urlencode(query), fragment=''))


def load_recent_activity(sheet_csv_url: str = None) -> List[Dict]:
    """
    Fetch Recent Activity rows from the Google Sheet (CSV format).

    The tab has these column headers (Row 1):
        Type | Title | Date | Details | Link

    Only Title is required. Rows appear in the newsletter in sheet order.
    If the tab is empty, returns an empty list and the section is left out.

    Args:
        sheet_csv_url: CSV URL of the Recent Activity tab. Falls back to
                       ACTIVITY_SHEET_CSV_URL, then to GOOGLE_SHEET_CSV_URL
                       pointed at the Recent Activity tab.
    """
    url = sheet_csv_url or os.getenv('ACTIVITY_SHEET_CSV_URL', '')
    if not url and os.getenv('GOOGLE_SHEET_CSV_URL'):
        url = activity_csv_url(os.getenv('GOOGLE_SHEET_CSV_URL'))

    if not url:
        print("No Google Sheet URL configured. Skipping Recent Activity.")
        return []

    print("Checking Google Sheet for Recent Activity...")

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"  Could not fetch Recent Activity tab: {e}")
        print("  Continuing without Recent Activity.")
        return []

    # Decode as UTF-8 explicitly, same reason as manual_stories.py
    content = response.content.decode('utf-8', errors='replace')
    reader = csv.DictReader(io.StringIO(content))

    items = []
    for row in reader:
        cleaned = {k.strip().lower(): v.strip() for k, v in row.items() if k and v}

        title = cleaned.get('title', '') or cleaned.get('headline', '')
        if not title:
            continue

        items.append({
            'type': cleaned.get('type', '') or cleaned.get('category', ''),
            'title': title,
            'date': cleaned.get('date', '') or cleaned.get('when', ''),
            'details': (cleaned.get('details', '') or cleaned.get('description', '')
                        or cleaned.get('summary', '')),
            'link': cleaned.get('link', '') or cleaned.get('url', ''),
        })

    if items:
        print(f"  Found {len(items)} Recent Activity item(s):")
        for i, item in enumerate(items):
            print(f"    {i+1}. {item['title'][:60]}...")
    else:
        print("  Recent Activity tab is empty. Section left out this week.")

    return items


def format_recent_activity(items: List[Dict]) -> str:
    """
    Format Recent Activity items as a newsletter section, in the same
    markdown the rest of the newsletter uses. The Type | Date line is a small
    lilac label, written as inline HTML because the markdown has no style for it.

    Returns an empty string when there are no items.
    """
    if not items:
        return ""

    label_style = (f"font-size: 12px; font-weight: 600; letter-spacing: 1px; "
                   f"text-transform: uppercase; color: {HTMLFormatter.BRAND_LILAC};")

    parts = [f"\n\n---\n\n## {SECTION_TITLE}\n"]

    for item in items:
        part = f"\n**{item['title']}**\n"

        lines = []
        label = ' | '.join(x for x in (item['type'], item['date']) if x)
        if label:
            lines.append(f'<span style="{label_style}">{label}</span>')
        body = item['details']
        if item['link']:
            body = f"{body} [Find out more ->]({item['link']})".strip()
        if body:
            lines.append(body)

        if lines:
            part += "\n" + "<br>\n".join(lines) + "\n"
        parts.append(part)

    return "\n".join(parts)


if __name__ == '__main__':
    # Quick test - set GOOGLE_SHEET_CSV_URL env var and run this file
    found = load_recent_activity()
    if found:
        print("\nFormatted output:")
        print(format_recent_activity(found))
    else:
        print("\nNo Recent Activity found. Make sure GOOGLE_SHEET_CSV_URL is set.")
