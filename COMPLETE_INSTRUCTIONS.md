# COMPLETE DEPLOYMENT INSTRUCTIONS
## Step-by-Step Guide with Claude Code Commands

**Project:** Mortgagelab.ai Automated Newsletter System  
**Estimated Time:** 30-60 minutes  
**Difficulty:** Beginner-friendly

---

## OVERVIEW

This guide will walk you through:
1. Getting your Anthropic API key
2. Testing the system locally
3. Deploying to GitHub Actions
4. Running your first automated newsletter

By the end, you'll have a fully automated newsletter system that runs every Thursday at 9 AM.

---

## PREREQUISITES

Before you start, ensure you have:
- [ ] Computer with internet connection
- [ ] GitHub account (free) - sign up at https://github.com
- [ ] Python 3.11+ installed (check with: `python --version` or `python3 --version`)
- [ ] Git installed (check with: `git --version`)
- [ ] Text editor (VS Code, Sublime, or even Notepad)
- [ ] Mailchimp account (free tier is fine)

---

## PART 1: GET YOUR API KEY (5 minutes)

### Step 1.1: Create Anthropic Account

1. Go to: https://console.anthropic.com/
2. Click "Sign Up" (top right)
3. Use your email or Google account
4. Verify your email if prompted
5. You'll land on the Anthropic Console dashboard

### Step 1.2: Add Payment Method

1. In the Console, click "Settings" (or "Billing")
2. Click "Add Payment Method"
3. Enter your credit/debit card details
4. **Don't worry:** You'll only be charged for what you use (~£2-4/month)
5. Anthropic gives you £5 free credit to start

### Step 1.3: Generate API Key

1. In the Console, click "API Keys" in the left sidebar
2. Click "Create Key" or "+ Create Key"
3. Give it a name: "Mortgagelab Newsletter"
4. Click "Create Key"
5. **CRITICAL:** Copy the key immediately (starts with `sk-ant-`)
6. Save it somewhere secure (password manager, notes app)
7. You won't be able to see it again!

**Your API key should look like:**
```
sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## PART 2: SET UP LOCALLY (15 minutes)

### Step 2.1: Download the Project Files

1. Download the `mortgagelab-newsletter` folder from Claude
2. Save it to your computer (e.g., `Documents/mortgagelab-newsletter`)
3. Remember this location - you'll need it

### Step 2.2: Open Terminal/Command Prompt

**On Mac:**
- Press `Cmd + Space`
- Type "Terminal"
- Press Enter

**On Windows:**
- Press `Win + R`
- Type "cmd"
- Press Enter

**On Linux:**
- Press `Ctrl + Alt + T`

### Step 2.3: Navigate to Project Folder

```bash
# Replace this path with where you saved the folder
cd Documents/mortgagelab-newsletter

# On Windows, it might be:
# cd C:\Users\YourName\Documents\mortgagelab-newsletter

# Verify you're in the right place
ls
# You should see: README.md, requirements.txt, src/, etc.
```

### Step 2.4: Install Python Dependencies

```bash
# Mac/Linux:
pip3 install -r requirements.txt

# Windows:
pip install -r requirements.txt

# If that doesn't work, try:
python -m pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed anthropic-0.18.0 feedparser-6.0.10 ...
```

### Step 2.5: Set Your API Key (TEMPORARY)

**On Mac/Linux:**
```bash
export ANTHROPIC_API_KEY='sk-ant-your-actual-key-here'
```

**On Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

**On Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY='sk-ant-your-actual-key-here'
```

**⚠️ IMPORTANT:** Replace `sk-ant-your-actual-key-here` with your actual API key!

### Step 2.6: Test RSS Feeds Only (No API Cost)

```bash
python3 tests/test_newsletter.py
# On Windows: python tests/test_newsletter.py
```

When prompted:
```
Choose test mode:
1. Test RSS feeds only (no API calls)
2. Test full pipeline (uses Claude API)

Enter choice (1 or 2): 1
```

**Type `1` and press Enter**

**Expected output:**
```
Testing RSS feed aggregation...
✓ Fetched 12 articles from Mortgage Strategy
✓ Fetched 8 articles from Mortgage Finance Gazette
✓ Fetched 15 articles from What Mortgage
...
✓ Successfully fetched 127 articles

Sample articles:
1. AI regulation looms for UK mortgage sector
   Source: Mortgage Strategy
   Category: UK Mortgage Press
...
```

**If you see this, your RSS feeds are working!** ✅

### Step 2.7: Test Full Pipeline (Uses API - ~£0.50)

```bash
python3 tests/test_newsletter.py
# On Windows: python tests/test_newsletter.py
```

When prompted, **type `2` and press Enter**

**Expected output:**
```
Running full newsletter generation pipeline...
This will use Claude API credits.

==================================================
 MORTGAGELAB.AI NEWSLETTER GENERATOR
==================================================

STEP 1: Fetching RSS Feeds
--------------------------------------------------
✓ Fetched 12 articles from Mortgage Strategy
✓ Fetched 8 articles from Mortgage Finance Gazette
...
Total articles collected: 127

STEP 2: Analyzing Articles with Claude AI
--------------------------------------------------
Analyzing article 1/127: AI regulation looms for UK...
  Score: 8/10 - Direct impact on mortgage compliance...
Analyzing article 2/127: ChatGPT usage rises in brokerages...
  Score: 7/10 - Shows AI adoption trends relevant to...
...

Top 5 articles selected:
1. [8/10] AI regulation looms for UK mortgage sector
2. [7/10] ChatGPT usage rises in brokerages
3. [7/10] Machine learning detects mortgage fraud
4. [6/10] Automated underwriting gains traction
5. [6/10] Voice AI assistants for mortgage queries

STEP 3: Generating Newsletter Content
--------------------------------------------------
✓ Newsletter content generated successfully

STEP 4: Converting to HTML for Mailchimp
--------------------------------------------------
Saved HTML newsletter to output/newsletter_2026-01-23.html

==================================================
 SUCCESS!
==================================================

Newsletter generated successfully at: 14:23:45

Output files:
  • Raw articles: output/articles_raw_2026-01-23.json
  • Analyzed articles: output/articles_analyzed_2026-01-23.json
  • Newsletter content: output/newsletter_content_2026-01-23.txt
  • HTML newsletter: output/newsletter_2026-01-23.html

Ready for Mailchimp! 📧
==================================================
```

**If you see this, everything works!** 🎉

### Step 2.8: Review Your First Newsletter

```bash
# Mac:
open output/newsletter_2026-01-23.html

# Windows:
start output/newsletter_2026-01-23.html

# Linux:
xdg-open output/newsletter_2026-01-23.html
```

This will open the HTML newsletter in your browser. You should see:
- Professional formatting
- 5 AI news stories relevant to mortgages
- 1 quiz question
- Weekend trivia

**Does it look good?** If yes, proceed to deployment! If no, we can adjust the prompts.

---

## PART 3: DEPLOY TO GITHUB (20 minutes)

### Step 3.1: Create GitHub Repository

1. Go to: https://github.com
2. Log in
3. Click the **"+"** icon (top right) → "New repository"
4. Fill in:
   - **Repository name:** `mortgagelab-newsletter`
   - **Description:** "Automated AI newsletter for UK mortgage industry"
   - **Visibility:** ✅ Private (recommended)
   - **DO NOT** check "Add a README file"
5. Click "Create repository"

You'll see a page with setup instructions. **Keep this page open.**

### Step 3.2: Initialize Git in Your Local Folder

**In your terminal (still in the project folder):**

```bash
# Check you're in the right folder
pwd
# Should show: /path/to/mortgagelab-newsletter

# Initialize git
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial newsletter system setup"
```

**Expected output:**
```
[main (root-commit) abc1234] Initial newsletter system setup
 15 files changed, 1200 insertions(+)
 create mode 100644 README.md
 create mode 100644 generate_newsletter.py
 ...
```

### Step 3.3: Connect to GitHub

**Copy the commands from your GitHub repository page.** They'll look like this:

```bash
# Example - YOUR URL WILL BE DIFFERENT
git remote add origin https://github.com/YOUR-USERNAME/mortgagelab-newsletter.git
git branch -M main
git push -u origin main
```

**On the GitHub page, find the section:**
```
…or push an existing repository from the command line
```

**Copy those three commands and paste them into your terminal.**

**You'll be prompted for your GitHub username and password.**

**⚠️ IMPORTANT:** For the password, you need a Personal Access Token (PAT), not your regular password.

#### Creating a Personal Access Token:

1. On GitHub, click your profile picture (top right)
2. Settings → Developer settings (bottom of left sidebar)
3. Personal access tokens → Tokens (classic)
4. "Generate new token" → "Generate new token (classic)"
5. Note: "Mortgagelab Newsletter"
6. Expiration: 90 days (or longer)
7. Select scopes: ✅ **repo** (check the top-level box)
8. Click "Generate token"
9. **Copy the token** (starts with `ghp_`)
10. Use this as your password when pushing

**After successful push:**
```bash
Enumerating objects: 20, done.
Counting objects: 100% (20/20), done.
...
To https://github.com/YOUR-USERNAME/mortgagelab-newsletter.git
 * [new branch]      main -> main
```

### Step 3.4: Verify Files on GitHub

1. Go to your repository: `https://github.com/YOUR-USERNAME/mortgagelab-newsletter`
2. You should see all your files:
   - README.md
   - requirements.txt
   - src/
   - .github/
   - etc.

**If you see them, excellent!** ✅

### Step 3.5: Add API Key to GitHub Secrets

**⚠️ CRITICAL - NEVER COMMIT YOUR API KEY TO THE REPOSITORY!**

1. On your GitHub repository page
2. Click **"Settings"** tab (top)
3. In left sidebar: **"Secrets and variables"** → **"Actions"**
4. Click **"New repository secret"** (green button)
5. Fill in:
   - **Name:** `ANTHROPIC_API_KEY`
   - **Secret:** Your API key (the `sk-ant-...` key)
6. Click **"Add secret"**

**You should now see:**
```
Repository secrets
ANTHROPIC_API_KEY   Updated now by YOUR-USERNAME
```

### Step 3.6: Enable GitHub Actions

1. Still on your repository page
2. Click **"Actions"** tab (top)
3. If prompted: Click **"I understand my workflows, go ahead and enable them"**
4. You should see: **"Weekly Newsletter Generation"** workflow

---

## PART 4: RUN YOUR FIRST AUTOMATED NEWSLETTER (5 minutes)

### Step 4.1: Manual Test Run

1. On the Actions tab
2. Click **"Weekly Newsletter Generation"** (left sidebar)
3. Click **"Run workflow"** dropdown (right side)
4. Click the green **"Run workflow"** button
5. The page will refresh - you'll see a yellow dot 🟡 next to a new workflow run

### Step 4.2: Monitor the Run

1. Click on the workflow run (it will say "Weekly Newsletter Generation")
2. Click **"generate-newsletter"** job
3. You'll see real-time logs:

```
Run actions/checkout@v3
✓ Checkout repository

Run actions/setup-python@v4
✓ Set up Python 3.11

Run python -m pip install...
✓ Install dependencies

Run python generate_newsletter.py
==================================================
 MORTGAGELAB.AI NEWSLETTER GENERATOR
==================================================

STEP 1: Fetching RSS Feeds
--------------------------------------------------
✓ Fetched 12 articles from Mortgage Strategy
...
```

**This takes 2-5 minutes.** ⏱️

### Step 4.3: Check for Success

At the bottom of the logs, you should see:

```
==================================================
 SUCCESS!
==================================================

Newsletter generated successfully at: 09:15:32

Output files:
  • Raw articles: output/articles_raw_2026-01-23.json
  • Analyzed articles: output/articles_analyzed_2026-01-23.json
  • Newsletter content: output/newsletter_content_2026-01-23.txt
  • HTML newsletter: output/newsletter_2026-01-23.html

Ready for Mailchimp! 📧
==================================================
```

**If you see this, your automation works!** 🎉

### Step 4.4: Download the Newsletter

1. Scroll to the bottom of the workflow run page
2. Under **"Artifacts"** section
3. Click **"newsletter-2026-01-23"** (or similar)
4. It will download a ZIP file
5. Extract the ZIP file
6. Open the HTML file in your browser

---

## PART 5: SEND YOUR FIRST NEWSLETTER (10 minutes)

### Step 5.1: Set Up Mailchimp (One-time)

1. Log into Mailchimp: https://mailchimp.com
2. Create an audience if you don't have one:
   - Audience → Create Audience
   - Fill in details (your business info)
3. Create a campaign:
   - Campaigns → Create Campaign
   - Choose "Email"
   - Choose "Regular" campaign

### Step 5.2: Design Your Template

1. **To:** Select your audience
2. **From:** Your email/name (e.g., "Paul Brett / mortgagelab.ai")
3. **Subject:** "This Week in AI: Mortgage Industry Edition"
4. **Preview Text:** "5 stories, 1 quiz, and weekend AI trivia"
5. Click **"Design Email"**

**Template Design:**
1. Choose **"Code your own"** template
2. Click **"Paste in code"**
3. Open your downloaded HTML file
4. Copy ALL the HTML (Ctrl+A, Ctrl+C)
5. Paste into Mailchimp
6. Click **"Save and Continue"**

### Step 5.3: Preview and Test

1. Click **"Preview and Test"**
2. Click **"Send a test email"**
3. Enter your email
4. Click **"Send Test"**
5. Check your inbox

**Does it look good?**
- ✅ Formatting correct?
- ✅ Links work?
- ✅ Images display (if any)?
- ✅ Readable on mobile?

### Step 5.4: Schedule for Friday

1. Click **"Schedule"** (not Send)
2. Choose Friday morning (e.g., 9:00 AM)
3. Review everything
4. Click **"Schedule Campaign"**

**Done!** Your first newsletter will go out Friday! 🎉

---

## ONGOING USAGE

### Every Week (15 minutes)

**Thursday Morning:**
- GitHub Actions automatically runs at 9 AM
- Newsletter generates automatically
- No action needed from you

**Thursday Afternoon:**
1. Go to: `https://github.com/YOUR-USERNAME/mortgagelab-newsletter/actions`
2. Click latest workflow run
3. Download the artifact
4. Review the HTML
5. Paste into Mailchimp
6. Schedule for Friday morning

**That's it!** 15 minutes per week.

---

## TROUBLESHOOTING

### "API key not found"

**Problem:** The environment variable isn't set.

**Solution:**
```bash
# Check if it's set:
echo $ANTHROPIC_API_KEY
# Should show your key

# If empty, set it again:
export ANTHROPIC_API_KEY='your-key-here'
```

### "No module named anthropic"

**Problem:** Dependencies not installed.

**Solution:**
```bash
pip3 install -r requirements.txt --upgrade
```

### "No articles found"

**Problem:** RSS feeds might be temporarily down.

**Solution:**
- Wait 1 hour and try again
- Check specific feeds in `rss_feeds.json`
- Some sites may have changed their RSS URLs

### "Git push failed"

**Problem:** Authentication issue.

**Solution:**
- Use a Personal Access Token (see Step 3.3)
- Make sure token has `repo` scope
- Try: `git config credential.helper store`

### "GitHub Actions failed"

**Problem:** Various causes.

**Solution:**
1. Click on the failed run
2. Click on the red ❌ step
3. Read the error message
4. Common fixes:
   - API key not in Secrets → Add it (Step 3.5)
   - Invalid API key → Generate new one
   - Rate limit → Wait 1 hour

---

## MONITORING COSTS

### Check API Usage:

1. Go to: https://console.anthropic.com/
2. Click **"Usage"** in sidebar
3. See your daily/monthly costs

**Expected costs:**
- Per newsletter: £0.30 - £0.80
- Per month: £2 - £4
- Per year: £25 - £50

**Ways to reduce costs:**
- Reduce number of articles analyzed
- Decrease number of RSS sources
- Use Claude Haiku instead of Sonnet (cheaper but lower quality)

---

## CUSTOMIZATION

### Change Schedule

Edit `.github/workflows/weekly-newsletter.yml`:

```yaml
schedule:
  # Current: Every Thursday at 9 AM
  - cron: '0 9 * * 4'
  
  # Change to Tuesday at 2 PM:
  - cron: '0 14 * * 2'
  
  # Change to daily at 8 AM:
  - cron: '0 8 * * *'
```

**Cron format:** `minute hour day-of-month month day-of-week`
- Day of week: 0=Sunday, 1=Monday, ..., 6=Saturday

### Change Number of Stories

Edit `generate_newsletter.py`:

Find this line:
```python
top_5 = analyzer.rank_articles(analyzed_articles, top_n=5)
```

Change to:
```python
top_5 = analyzer.rank_articles(analyzed_articles, top_n=7)  # Now 7 stories
```

### Add More RSS Feeds

Edit `rss_feeds.json`:

```json
{
  "name": "Your Source Name",
  "url": "https://example.com/feed",
  "category": "AI News"
}
```

Add it to the appropriate section.

### Adjust AI Analysis

Edit `config/claude_prompts.py`:

Look for `RELEVANCE_ANALYSIS_PROMPT` and modify the scoring criteria.

---

## MAINTENANCE

### Weekly:
- Review generated content (15 min)
- Monitor subscriber engagement

### Monthly:
- Check API costs
- Review article quality
- Update prompts if needed

### Quarterly:
- Verify all RSS feeds still work
- Update any broken feed URLs
- Consider adding new sources

### Annually:
- Review overall system performance
- Update dependencies:
  ```bash
  pip install -r requirements.txt --upgrade
  ```
- Rotate API key (security best practice)

---

## NEXT STEPS

### Week 1:
- ✅ Send your first newsletter
- 📊 Track open rates
- 💬 Gather initial feedback

### Month 1:
- Fine-tune article selection criteria
- Adjust tone/style based on feedback
- Monitor costs

### Month 2+:
- Consider enhancements:
  - Archive page on mortgagelab.ai
  - Social media automation
  - Subscriber preferences
  - A/B testing headlines

---

## GETTING HELP

### Resources:
1. **Project README:** Full system documentation
2. **GitHub Issues:** Track problems/enhancements
3. **Anthropic Docs:** https://docs.anthropic.com
4. **GitHub Actions Docs:** https://docs.github.com/actions

### Support Channels:
- Anthropic Support: support@anthropic.com
- GitHub Support: https://support.github.com

---

## SUCCESS CHECKLIST

Before going live, verify:

- [x] Downloaded project files
- [x] Got Anthropic API key
- [x] Installed Python dependencies
- [x] Tested RSS feeds locally
- [x] Tested full pipeline locally
- [x] Created GitHub repository
- [x] Pushed code to GitHub
- [x] Added API key to GitHub Secrets
- [x] Ran test workflow successfully
- [x] Downloaded generated newsletter
- [x] Set up Mailchimp template
- [x] Sent test email to yourself
- [x] Scheduled first newsletter

---

## CONGRATULATIONS!

You now have a fully automated newsletter system that:
✅ Runs every Thursday morning automatically
✅ Analyzes 17 news sources with AI
✅ Generates professional content
✅ Costs only £2-4/month
✅ Saves you 2-3 hours/week

**Your mortgagelab.ai newsletter is live!** 🚀

---

**Questions?** Review the documentation files:
- README.md - System architecture
- DEPLOYMENT.md - Detailed setup
- PROJECT_SUMMARY.md - Complete overview

**Ready to enhance?** Consider:
- Adding more RSS sources
- Customizing the AI prompts
- Creating a web archive
- Automating social media posts

Good luck with your newsletter! 📧
