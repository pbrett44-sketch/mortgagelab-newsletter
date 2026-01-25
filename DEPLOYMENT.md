# Deployment Guide
## Mortgagelab.ai Newsletter System

This guide will walk you through deploying your automated newsletter system to GitHub Actions.

## Prerequisites

Before you begin, ensure you have:
- ✅ Anthropic API account with API key
- ✅ GitHub account
- ✅ Mailchimp account for sending newsletters

## Step 1: Get Your Anthropic API Key

1. Go to: https://console.anthropic.com/
2. Sign in or create an account
3. Navigate to API Keys section
4. Create a new API key
5. **Copy and save it securely** (you won't be able to see it again)

**Estimated cost:** £2-4/month based on weekly usage

## Step 2: Create GitHub Repository

### Option A: Create New Repository

1. Go to GitHub.com
2. Click "New repository"
3. Name it: `mortgagelab-newsletter`
4. Make it **Private** (recommended)
5. Don't initialize with README (we have one)
6. Click "Create repository"

### Option B: Use Existing Repository

If you already have a repository for mortgagelab.ai, you can add this as a subdirectory.

## Step 3: Upload Code to GitHub

### If you're comfortable with git:

```bash
cd /path/to/mortgagelab-newsletter
git init
git add .
git commit -m "Initial newsletter system setup"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/mortgagelab-newsletter.git
git push -u origin main
```

### If you prefer GitHub web interface:

1. Go to your repository on GitHub
2. Click "Add file" → "Upload files"
3. Drag and drop all the files from your local `mortgagelab-newsletter` folder
4. Commit the changes

## Step 4: Add API Key to GitHub Secrets

**CRITICAL:** Never commit your API key to the repository!

1. Go to your repository on GitHub
2. Click "Settings" tab
3. In the left sidebar, click "Secrets and variables" → "Actions"
4. Click "New repository secret"
5. Name: `ANTHROPIC_API_KEY`
6. Value: Paste your Anthropic API key
7. Click "Add secret"

## Step 5: Enable GitHub Actions

1. Go to the "Actions" tab in your repository
2. If prompted, click "I understand my workflows, go ahead and enable them"
3. You should see "Weekly Newsletter Generation" workflow

## Step 6: Test the System

### Manual Test Run

1. Go to "Actions" tab
2. Click on "Weekly Newsletter Generation" workflow
3. Click "Run workflow" dropdown
4. Click the green "Run workflow" button
5. Wait for it to complete (usually 2-5 minutes)

### Check the Results

1. Click on the completed workflow run
2. Click on "generate-newsletter" job
3. Scroll through the logs to see:
   - RSS feeds being fetched
   - Articles being analyzed
   - Newsletter being generated
4. Download the newsletter artifact:
   - Scroll to bottom of workflow page
   - Under "Artifacts" section, download the newsletter files

## Step 7: Set Up Mailchimp Template (One-time)

1. Log into Mailchimp
2. Go to Campaigns → Email templates
3. Create a new template or use existing
4. Design your template structure:
   - Header with mortgagelab.ai branding
   - Main content area (this is where you'll paste generated HTML)
   - Footer with unsubscribe link

**Pro tip:** Keep the template simple - the newsletter HTML already includes styling

## Step 8: Weekly Workflow

### Every Thursday Morning:

**9:00 AM:** GitHub Actions automatically:
1. Pulls latest news from RSS feeds
2. Analyzes articles with Claude AI
3. Generates newsletter content
4. Creates HTML file
5. Saves to repository

**You receive notification** (configure in GitHub settings)

### Your Actions (Thursday Afternoon):

1. Go to repository → Actions tab
2. Click latest "Weekly Newsletter Generation" run
3. Download the newsletter artifact
4. Open the HTML file
5. Review the content
6. Copy the HTML content
7. Paste into your Mailchimp campaign
8. Send test email to yourself
9. Review and schedule for Friday morning

## Customization Options

### Change Schedule

Edit `.github/workflows/weekly-newsletter.yml`:

```yaml
schedule:
  # Change '0 9 * * 4' to your preferred time
  # Format: minute hour day-of-month month day-of-week
  # Current: 9 AM every Thursday
  - cron: '0 9 * * 4'
```

### Change Number of Stories

Edit `src/ai_analyser.py` line where `top_n=5` appears:

```python
top_articles = sorted_articles[:7]  # Change 5 to 7 for 7 stories
```

### Adjust Analysis Criteria

Edit `config/claude_prompts.py` to modify how articles are scored.

## Troubleshooting

### "No articles found"

**Possible causes:**
- RSS feeds may be down
- Network issues in GitHub Actions
- RSS feed URLs changed

**Solution:**
- Check RSS feed URLs in `rss_feeds.json`
- Test feeds manually: https://validator.w3.org/feed/

### "API key error"

**Possible causes:**
- API key not set in GitHub Secrets
- API key invalid or expired

**Solution:**
- Regenerate API key in Anthropic console
- Update GitHub Secret

### "Generation failed"

**Possible causes:**
- Not enough articles found
- API rate limits hit
- Network timeout

**Solution:**
- Check GitHub Actions logs for specific error
- Wait and try again
- Contact support if persists

## Monitoring Costs

### Track API Usage:

1. Go to: https://console.anthropic.com/
2. Click on "Usage" tab
3. Monitor your weekly costs

**Expected usage per newsletter:**
- ~50-100 API calls per week
- ~50,000-100,000 tokens processed
- Cost: £0.50-1.00 per week

## Next Steps

### Week 1:
- Run first test generation
- Review output quality
- Adjust prompts if needed
- Send first newsletter

### Month 1:
- Monitor subscriber engagement
- Gather feedback
- Refine article selection
- Update RSS sources if needed

### Ongoing:
- Review quarterly for RSS feed changes
- Update prompts based on feedback
- Track API costs
- Archive best newsletters

## Getting Help

If you encounter issues:

1. **Check logs:** GitHub Actions → Your workflow → View logs
2. **Test locally:** Run `python tests/test_newsletter.py`
3. **Review documentation:** README.md in repository
4. **Contact support:** Anthropic support or GitHub support

## Security Reminders

- ✅ Never commit API keys to repository
- ✅ Keep repository private (unless you want to open-source it)
- ✅ Rotate API keys regularly (every 6 months)
- ✅ Monitor usage for unexpected spikes

---

**System Status:** Ready for deployment ✓
**Last Updated:** January 23, 2026
