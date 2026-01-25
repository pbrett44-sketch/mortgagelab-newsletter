# Mortgagelab.ai Automated Newsletter System

**Project Owner:** Paul Brett
**Purpose:** Weekly automated AI news newsletter for the UK mortgage industry
**Publish Day:** Friday mornings
**Created:** January 23, 2026

## Overview

This system automatically generates a weekly newsletter featuring:
- 5 curated AI news stories relevant to the UK mortgage industry
- 1 multiple-choice quiz question
- Weekend trivia piece
- Target reading time: ~5 minutes

## Target Audience

- UK mortgage brokers
- Lenders
- Broader mortgage industry professionals
- Assumed AI literacy: Low level (beginner-friendly explanations)

## Workflow

**Thursday Morning (Automated):**
1. Python script pulls RSS feeds from 15+ news sources
2. Claude API analyses each article for mortgage + AI relevance
3. Ranks stories by impact and relevance to UK mortgage industry
4. Generates complete newsletter content (5 stories + quiz + trivia)
5. Outputs HTML formatted for Mailchimp

**Thursday Afternoon (Manual):**
1. You review the generated content
2. Make any necessary edits
3. Paste into Mailchimp template
4. Schedule for Friday morning delivery

## Technology Stack

- **Hosting:** GitHub Actions (free, cloud-based automation)
- **Language:** Python 3.11+
- **API:** Anthropic Claude API
- **Scheduler:** GitHub Actions cron (runs every Thursday 9am UK time)
- **Output:** HTML formatted for Mailchimp
- **Delivery:** Manual via Mailchimp

## News Sources

### UK Mortgage Press (8 sources)
- Mortgage Strategy
- Mortgage Finance Gazette
- What Mortgage
- Mortgage Introducer
- Financial Reporter
- Mortgage Soup
- Bridging & Commercial
- Mortgage Solutions

### AI/Tech News (6 sources)
- TechCrunch AI
- The Verge AI
- MIT Technology Review AI
- VentureBeat AI
- AI Magazine
- AI Magazine RSS

### Broadsheet Tech (3 sources)
- Financial Times Technology
- The Times Technology
- The Guardian Technology

**Total: 17 news sources**

## Newsletter Structure

### Section 1: Top 5 AI Stories
Each story includes:
- Compelling headline
- 2-3 sentence summary
- "Why it matters for UK mortgages" explanation
- Link to original source

### Section 2: Quiz Question
- 1 multiple-choice question (4 options)
- Related to one of the week's AI developments
- Answer provided at bottom of newsletter

### Section 3: Weekend Trivia
- Fun, interesting AI or tech fact
- "Something for the weekend" tone
- Keeps it light and engaging

## File Structure

```
mortgagelab-newsletter/
├── README.md                          # This file
├── rss_feeds.json                     # RSS feed URLs and categories
├── requirements.txt                   # Python dependencies
├── src/
│   ├── feed_aggregator.py            # Pulls RSS feeds
│   ├── ai_analyser.py                # Claude API integration
│   ├── content_generator.py          # Newsletter content creation
│   └── html_formatter.py             # HTML output for Mailchimp
├── .github/
│   └── workflows/
│       └── weekly-newsletter.yml     # GitHub Actions automation
├── config/
│   ├── claude_prompts.py             # AI analysis prompts
│   └── newsletter_template.html      # Base HTML template
├── output/
│   └── newsletter_YYYY-MM-DD.html    # Generated newsletters
└── tests/
    └── test_newsletter.py            # Manual testing script
```

## Setup Requirements

### 1. Anthropic API Key
- Sign up at: https://console.anthropic.com/
- Estimated cost: £2-4/month
- Store as GitHub secret: `ANTHROPIC_API_KEY`

### 2. GitHub Repository
- Fork or create new repo
- Enable GitHub Actions
- Set up secrets for API key

### 3. Mailchimp Template
- Design newsletter template in Mailchimp
- Keep structure consistent for pasting generated content

## Running the System

### Automatic (Production):
- Runs every Thursday at 9:00 AM UK time
- GitHub Actions triggers Python script
- Generated HTML saved to repository
- Email notification sent to you with download link

### Manual (Testing):
```bash
python tests/test_newsletter.py
```

## Content Generation Philosophy

- **Relevance:** Only include AI news with clear mortgage industry implications
- **Accessibility:** Explain AI concepts for low-literacy audience
- **Brevity:** Keep summaries concise (2-3 sentences)
- **Value:** Focus on practical implications, not theoretical
- **Balance:** Mix of regulatory, tech, and market news
- **UK Focus:** Prioritise UK-relevant developments

## Scoring Criteria (AI Analysis)

Each article scored 1-10 on:
1. **Direct mortgage relevance** (40% weight)
2. **AI/automation focus** (30% weight)
3. **UK market applicability** (20% weight)
4. **Timeliness/impact** (10% weight)

Top 5 scoring articles included in newsletter.

## Customisation Options

You can adjust:
- Number of stories (currently 5)
- Tone (currently: confident, direct, professional)
- Technical depth (currently: beginner-friendly)
- Quiz difficulty
- Trivia topic focus

## Maintenance

- **Weekly:** Review generated content Thursday afternoon
- **Monthly:** Review source quality and relevance scores
- **Quarterly:** Update RSS feeds if sources change
- **Annually:** Review and update AI analysis prompts

## Future Enhancements

Potential additions (Month 2+):
- A/B testing different headlines
- Subscriber engagement tracking
- Automated social media posts
- Archive page on mortgagelab.ai
- Subscriber preference learning

## Support

For issues or questions:
- Check GitHub Issues
- Review Claude Code documentation
- Test manually using `test_newsletter.py`

---

**Status:** Ready for deployment
**Next Step:** Deploy to GitHub Actions and run first test
