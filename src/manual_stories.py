"""
Manual Stories Loader - Fetches manually added stories from a Google Sheet
Published as CSV. Paul just types stories into the Google Sheet and
this module picks them up automatically on the next newsletter run.
"""

import csv
import io
import os
import requests
from typing import List, Dict


def load_manual_stories(sheet_csv_url: str = None) -> List[Dict]:
    """
    Fetch manual stories from a published Google Sheet (CSV format).

    The Google Sheet should have these column headers (Row 1):
        Headline | Summary | Link | Why It Matters

    Paul just fills in rows beneath those headers. Empty rows are ignored.
    If the sheet is empty (no data rows), returns an empty list and the
    newsletter runs with just the automated Top 5 as normal.

    Args:
        sheet_csv_url: The published CSV URL of the Google Sheet.
                       Falls back to GOOGLE_SHEET_CSV_URL env var.

    Returns:
        List of story dictionaries ready to merge into the newsletter.
    """
    # Get the URL from argument or environment variable
    url = sheet_csv_url or os.getenv('GOOGLE_SHEET_CSV_URL', '')

    if not url:
        print("No Google Sheet URL configured. Skipping manual stories.")
        return []

    print("Checking Google Sheet for manual stories...")

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"  Could not fetch Google Sheet: {e}")
        print("  Continuing without manual stories.")
        return []

    # Parse the CSV content
    content = response.text
    reader = csv.DictReader(io.StringIO(content))

    stories = []
    for row in reader:
        # Normalise column names (strip whitespace, lowercase for matching)
        cleaned = {k.strip().lower(): v.strip() for k, v in row.items() if k and v}

        # Extract fields - be flexible with column naming
        headline = cleaned.get('headline', '') or cleaned.get('title', '')
        summary = cleaned.get('summary', '') or cleaned.get('content', '') or cleaned.get('description', '')
        link = cleaned.get('link', '') or cleaned.get('url', '')
        why_it_matters = (
            cleaned.get('why it matters', '') or
            cleaned.get('why_it_matters', '') or
            cleaned.get('why it matters for uk mortgages', '') or
            cleaned.get('matters', '')
        )

        # Skip rows where headline is empty (probably a blank row)
        if not headline:
            continue

        story = {
            'headline': headline,
            'summary': summary,
            'link': link,
            'why_it_matters': why_it_matters,
            'is_manual': True  # Flag so the system knows this was added by Paul
        }
        stories.append(story)

    if stories:
        print(f"  Found {len(stories)} manual story/stories from Google Sheet:")
        for i, s in enumerate(stories):
            print(f"    {i+1}. {s['headline'][:60]}...")
    else:
        print("  Google Sheet is empty. No manual stories this week.")

    return stories


def format_manual_stories_for_prompt(manual_stories: List[Dict]) -> str:
    """
    Format manual stories into text that can be appended to the
    newsletter content. These stories are already written by Paul,
    so Claude just needs to format them consistently with the rest
    of the newsletter (not rewrite them).

    Args:
        manual_stories: List of manual story dicts from load_manual_stories()

    Returns:
        Formatted text block to append to newsletter content.
    """
    if not manual_stories:
        return ""

    parts = []
    parts.append("\n\n---\n\n## Also This Week\n")

    for story in manual_stories:
        part = f"\n**{story['headline']}**\n"
        if story['summary']:
            part += f"{story['summary']}\n"
        if story['why_it_matters']:
            part += f"**Why it matters for UK mortgages:**\n{story['why_it_matters']}\n"
        if story['link']:
            part += f"[Read more \u2192]({story['link']})\n"
        parts.append(part)

    return "\n".join(parts)


if __name__ == '__main__':
    # Quick test - set GOOGLE_SHEET_CSV_URL env var and run this file
    stories = load_manual_stories()
    if stories:
        print("\nFormatted output:")
        print(format_manual_stories_for_prompt(stories))
    else:
        print("\nNo stories found. Make sure GOOGLE_SHEET_CSV_URL is set.")
