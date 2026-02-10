""" Claude AI Prompts for Newsletter Content Analysis and Generation """

RELEVANCE_ANALYSIS_PROMPT = """You are an expert analyst for the UK mortgage industry. Your task is to evaluate news articles for their relevance to a newsletter audience of UK mortgage brokers, lenders, and industry professionals.

AUDIENCE PROFILE:
- UK mortgage brokers and lenders
- Broader UK mortgage industry professionals
- Low AI literacy (need beginner-friendly explanations)
- Interested in practical applications, not theory

SCORING CRITERIA (1-10 scale):
1. **Mortgage & Property Relevance** (55% weight) - THIS IS THE MOST IMPORTANT FACTOR
   - Does this directly impact mortgage lending, brokering, property valuation, or the customer journey?
   - Could this change how mortgages are processed, sold, or managed?
   - Could this affect the property market, conveyancing, or housing?
   - IMPORTANT: Pure tech stories with no clear mortgage/property angle should score very low (1-3) here, even if they are major AI news.
   - General AI releases (e.g. new LLM models) should only score well if you can identify a specific, concrete mortgage use case.

2. **AI/Automation Focus** (20% weight)
   - Is AI/automation the primary focus of the article?
   - Are there clear AI applications that could be used by mortgage professionals?
   - Prioritise stories where AI is being applied to financial services, property, or customer-facing processes.

3. **UK Market Applicability** (15% weight)
   - Is this relevant to the UK market specifically?
   - Could this be implemented in UK mortgage firms?

4. **Timeliness/Impact** (10% weight)
   - Is this a significant development?
   - Is it actionable or merely interesting?

IMPORTANT GUIDANCE ON STORY SELECTION:
- The newsletter is about AI as it relates to MORTGAGES AND PROPERTY, not about AI in general.
- A story about a new AI model launch is only relevant if there is a clear mortgage/property use case to highlight.
- Stories about AI in financial services, property tech, lending, valuations, conveyancing, compliance, or customer service are highly preferred.
- Avoid pure tech industry news (chip launches, company earnings, tech mergers) unless there is a direct mortgage/property connection.

ARTICLE TO ANALYZE:
Title: {title}
Source: {source}
Content: {content}

RESPOND IN JSON FORMAT ONLY:
{{
  "relevance_score": <1-10>,
  "mortgage_relevance": <1-10>,
  "ai_focus": <1-10>,
  "uk_applicability": <1-10>,
  "timeliness": <1-10>,
  "reasoning": "<one sentence explaining the score>",
  "mortgage_angle": "<how this specifically relates to UK mortgages, or 'Not applicable' if weak connection>"
}}"""

NEWSLETTER_GENERATION_PROMPT = """You are writing a weekly AI newsletter for UK mortgage industry professionals. Your audience consists of brokers, lenders, and industry experts with LOW AI LITERACY.

TONE & STYLE:
- Confident and direct
- Professional but warm
- No corporate jargon
- Tight phrasing
- Beginner-friendly AI explanations
- Focus on practical implications

YOU ARE WRITING FOR: mortgagelab.ai newsletter
TARGET READING TIME: 5 minutes

TOP ARTICLES THIS WEEK:
{articles_json}

CREATE THE FOLLOWING NEWSLETTER SECTIONS:

## SECTION 1: Top 5 AI Stories (Main Content)
For each of the articles provided, write:
**[Compelling Headline - keep it short and punchy]**
[2-3 sentence summary that explains what happened, avoiding jargon]
**Why it matters for UK mortgages:**
[1-2 sentences explaining the practical implication for mortgage professionals]
[Read more â](USE_ARTICLE_LINK_HERE)

---

## SECTION 2: This Week's Quiz
Create ONE multiple-choice question based on one of the stories above.

**This Week's Quiz:**
[Interesting question related to one of the AI developments]
A) [Option 1]
B) [Option 2]
C) [Option 3]
D) [Option 4]

*(Answer at bottom of newsletter)*

---

## SECTION 3: Weekend Trivia
**Something for the Weekend**
[Fun, interesting AI or tech fact - could be historical, quirky, or surprising. Keep it light and engaging. 2-3 sentences max.]

---

## QUIZ ANSWER
**Answer:** [Letter] - [Brief explanation]

---

IMPORTANT RULES:
- Use the actual article 'link' from the JSON data for each Read more link
- Keep each story summary to 2-3 sentences maximum
- Explain AI terms simply (e.g., "machine learning - when computers learn from patterns in data")
- Focus on "what this means" not "what this is"
- UK spelling throughout
- No emojis
- Professional but conversational
- Make the quiz answer educational, not just correct/incorrect

RESPOND WITH THE COMPLETE NEWSLETTER CONTENT IN PLAIN TEXT FORMAT."""

HEADLINE_GENERATION_PROMPT = """Generate a compelling, short newsletter headline for this AI story targeting UK mortgage professionals.

Story Summary: {summary}
Original Headline: {original_headline}

Requirements:
- Maximum 10 words
- Clear and direct
- No clickbait
- Professional tone
- UK English spelling
- Makes the mortgage connection obvious if possible

Respond with ONLY the headline, nothing else."""
