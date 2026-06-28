"""
Manual Stories Loader - Fetches manually added stories from a Google Sheet
Published as CSV. Paul just types stories into the Google Sheet and
this module picks them up automatically on the next newsletter run.
"""

import csv
import io
import os
import re
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
                        part += f"[Read more ->]({story['link']})\n"
        parts.append(part)

    return "\n".join(parts)


# Section headers that mark the START of the Quiz / Weekend blocks. The manual
# "Also This Week" section must be inserted BEFORE the earliest of these, so it
# always sits directly after the Top Stories and ahead of the quiz and weekend
# trivia. Patterns are matched case-insensitively at the start of a line and
# cover the header variants Claude produces (with or without "SECTION n:",
# and bold "**...**" instead of an h2).
_QUIZ_WEEKEND_ANCHORS = [
    r'^[ \t]*#{1,6}[ \t]*SECTION[ \t]*2\b',          # ## SECTION 2: ...
    r"^[ \t]*#{1,6}[ \t]*.*This Week.?s Quiz",        # ## This Week's Quiz
    r'^[ \t]*#{1,6}[ \t]*Quiz\b',                     # ## Quiz
    r"^[ \t]*\*\*[ \t]*This Week.?s Quiz",            # **This Week's Quiz**
    r'^[ \t]*#{1,6}[ \t]*SECTION[ \t]*3\b',           # ## SECTION 3: ...
    r'^[ \t]*#{1,6}[ \t]*Something for the Weekend',  # ## Something for the Weekend
    r'^[ \t]*\*\*[ \t]*Something for the Weekend',    # **Something for the Weekend**
]


def insert_manual_section(newsletter_content: str, manual_section: str) -> str:
    """
    Insert the manual "Also This Week" block directly after the Top Stories and
    BEFORE the Quiz and Weekend sections, whatever header format the model used.

    Falls back to inserting before the Quiz Answer, and only as a last resort
    appends at the end - it never silently drops the section. Avoids doubling up
    the "---" divider that usually precedes the quiz.
    """
    if not manual_section.strip():
        return newsletter_content

    block = manual_section.strip()  # e.g. "---\n\n## Also This Week\n..."

    # Find the earliest quiz/weekend anchor.
    earliest = None
    for pattern in _QUIZ_WEEKEND_ANCHORS:
        match = re.search(pattern, newsletter_content,
                          re.IGNORECASE | re.MULTILINE)
        if match and (earliest is None or match.start() < earliest):
            earliest = match.start()

    # Last-resort anchors if no quiz/weekend header was found.
    if earliest is None:
        for pattern in [r'^[ \t]*#{1,6}[ \t]*.*Answer',
                        r'^[ \t]*\*\*[ \t]*Answer']:
            match = re.search(pattern, newsletter_content,
                              re.IGNORECASE | re.MULTILINE)
            if match and (earliest is None or match.start() < earliest):
                earliest = match.start()

    if earliest is None:
        # Nothing to anchor to - append rather than lose the section.
        return newsletter_content.rstrip() + "\n\n" + block + "\n"

    head = newsletter_content[:earliest]
    tail = newsletter_content[earliest:]
    # Drop any trailing "---" divider(s) on the head so we don't double them up
    # (block already starts with its own divider).
    head = re.sub(r'(?:\n[ \t]*-{3,}[ \t]*)+\s*$', '\n', head).rstrip()

    return head + "\n\n" + block + "\n\n---\n\n" + tail


if __name__ == '__main__':
    # Quick test - set GOOGLE_SHEET_CSV_URL env var and run this file
    stories = load_manual_stories()
    if stories:
        print("\nFormatted output:")
        print(format_manual_stories_for_prompt(stories))
    else:
        print("\nNo stories found. Make sure GOOGLE_SHEET_CSV_URL is set.")
