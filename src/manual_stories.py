"""
Manual Stories Fetcher - Pulls curated stories from Google Sheets
for the 'Also This Week' newsletter section
"""

import csv
import io
import urllib.request
from typing import List, Dict

# Google Sheet with manual stories (Headline, Summary, Link, Why It Matters)
SHEET_ID = "1O45AM3FnEVO9nOos3K5hHW9QLy6S6Gk7j7VhUK9CZd0"
SHEET_GID = "0"


def fetch_manual_stories() -> List[Dict]:
    """
    Fetch manually curated stories from the Google Sheet.

    Returns:
        List of story dicts with keys: headline, summary, link, why_it_matters
    """
    url = (
        f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
        f"/export?format=csv&gid={SHEET_GID}"
    )

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            # Follow redirects automatically
            raw = resp.read().decode('utf-8')
    except Exception as e:
        print(f"  Warning: Could not fetch manual stories sheet: {e}")
        return []

    reader = csv.DictReader(io.StringIO(raw))
    stories = []

    for row in reader:
        headline = (row.get('Headline') or '').strip()
        summary = (row.get('Summary') or '').strip()
        link = (row.get('Link') or '').strip()
        why = (row.get('Why It Matters') or '').strip()

        # Skip empty rows
        if not headline or not summary:
            continue

        stories.append({
            'headline': headline,
            'summary': summary,
            'link': link,
            'why_it_matters': why,
        })

    return stories


def format_as_markdown(stories: List[Dict]) -> str:
    """
    Format manual stories as markdown matching the newsletter content style,
    ready to be appended as an 'Also This Week' section.
    """
    if not stories:
        return ''

    parts = ['\n---\n\n## Also This Week\n']

    for story in stories:
        parts.append(f"\n**{story['headline']}**")
        parts.append(story['summary'])

        if story['why_it_matters']:
            parts.append(f"**Why it matters for UK mortgages:**")
            parts.append(story['why_it_matters'])

        if story['link']:
            parts.append(f"[Read more →]({story['link']})")

        parts.append('')  # blank line between stories

    return '\n'.join(parts)
