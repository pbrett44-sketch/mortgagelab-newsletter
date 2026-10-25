"""Build the Thursday newsletter reminder email as a visual report.

Reads HEADLINE, ACTIVITY, RUN_WORKFLOW_URL and SHEET_EDIT_URL from the
environment (the same values newsletter-reminder.yml puts in the Telegram
message) and prints a full HTML document on stdout. It goes through the HTML
email Zap (ZAPIER_HTML_EMAIL_WEBHOOK); the older ZAPIER_EMAIL_WEBHOOK Zap sends
plain text and shows this document as raw markup (tested 25 Oct 2026).

report_render.py next to this file is a copy of shared/report_render.py in the
bts-exec-team repo (spec: shared/visual-reports.md there). Refresh the copy when
that file changes.
"""

import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import report_render  # noqa: E402


def build_report(headline, activity, run_url, sheet_url, today):
    story_ok = bool(headline) and not headline.startswith("(")
    if story_ok:
        lead = f'This week\'s manual story is "{headline}". If that is right, run the newsletter.'
        story = {"text": headline, "tone": "ok"}
    else:
        lead = "The sheet has no manual story this week, or could not be read. Update it before you run the newsletter."
        story = {"text": headline or "(could not read the sheet)", "tone": "bad"}

    lines = [l.strip() for l in (activity or "").splitlines() if l.strip()]
    acts = [{"text": l[1:].strip()} for l in lines if l.startswith("•")]
    activity_sec = {"heading": "RECENT ACTIVITY IN THE SHEET", "items": acts}
    if not acts:
        activity_sec["empty"] = lines[0] if lines else "(none, so the section is left out this week)"

    return {
        "report": "newsletter-ready",
        "agent": "MortgageLab newsletter",
        "title": "MortgageLab newsletter: ready to prepare",
        "date": today.strftime("%A %-d %B %Y"),
        "headline": lead,
        "sections": [
            {"heading": "MANUAL STORY IN THE SHEET", "items": [story]},
            activity_sec,
            {"heading": "TO RUN IT", "items": [
                {"tag": "Option 1", "tone": "info",
                 "text": 'Say "run the newsletter" to Claude, on Telegram or in a Claude Code session.'},
                {"tag": "Option 2", "tone": "info", "text": "Press Run workflow on GitHub.",
                 "links": [{"label": "Run workflow", "url": run_url}]},
            ]},
            {"heading": "IF THAT IS NOT RIGHT", "items": [
                {"tone": "warn", "text": "Update the sheet first.",
                 "links": [{"label": "Open the sheet", "url": sheet_url}]},
            ]},
        ],
        "footer": "Nothing runs, and no API credit is spent, until you trigger it. Sent by newsletter-reminder.yml on GitHub.",
        "desk": True,
    }


def main():
    rep = build_report(
        os.environ.get("HEADLINE", "").strip(),
        os.environ.get("ACTIVITY", ""),
        os.environ["RUN_WORKFLOW_URL"],
        os.environ["SHEET_EDIT_URL"],
        datetime.now(ZoneInfo("Europe/London")),
    )
    sys.stdout.write(report_render.render_html(rep))


if __name__ == "__main__":
    main()
