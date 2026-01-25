# Quick Start Guide
## Get Your Newsletter Running in 15 Minutes

Follow these steps to get your first newsletter generated today.

## 1. Get Your API Key (2 minutes)

1. Visit: https://console.anthropic.com/
2. Sign up or log in
3. Go to "API Keys"
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-...`)

## 2. Set Up Locally First (5 minutes)

```bash
# Navigate to the project folder
cd mortgagelab-newsletter

# Install Python dependencies
pip install -r requirements.txt

# Set your API key (Mac/Linux)
export ANTHROPIC_API_KEY='your-api-key-here'

# Or for Windows
set ANTHROPIC_API_KEY=your-api-key-here
```

## 3. Test the System (5 minutes)

```bash
# Run the test script
python tests/test_newsletter.py

# Choose option 1 first (tests RSS feeds only, no API costs)
# Then choose option 2 (full pipeline test)
```

This will:
- ✓ Fetch articles from all RSS feeds
- ✓ Analyze them with Claude
- ✓ Generate newsletter content
- ✓ Create HTML file

## 4. Review Your First Newsletter (2 minutes)

```bash
# Open the generated HTML in your browser
open output/newsletter_*.html

# Or on Windows:
start output/newsletter_*.html
```

You should see:
- 5 AI news stories relevant to UK mortgages
- 1 quiz question
- Weekend trivia
- Professional HTML formatting

## 5. Deploy to GitHub Actions (10 minutes)

See DEPLOYMENT.md for full instructions, but here's the summary:

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial setup"

# Create repository on GitHub.com, then:
git remote add origin https://github.com/YOUR-USERNAME/mortgagelab-newsletter.git
git push -u origin main

# Add your API key to GitHub Secrets
# Go to Settings → Secrets and variables → Actions
# Add secret: ANTHROPIC_API_KEY
```

## 6. Manual First Run on GitHub (1 minute)

1. Go to your GitHub repository
2. Click "Actions" tab
3. Click "Weekly Newsletter Generation"
4. Click "Run workflow"
5. Wait 2-3 minutes
6. Download the artifact

## Done! 🎉

Your automated newsletter system is now:
- ✅ Running in the cloud
- ✅ Scheduled for every Thursday 9 AM
- ✅ Generating AI-relevant mortgage industry news
- ✅ Ready for Mailchimp

## Your Weekly Routine

**Thursday Morning:** System runs automatically

**Thursday Afternoon (15 minutes):**
1. Check GitHub Actions for completion
2. Download newsletter HTML
3. Review content
4. Paste into Mailchimp
5. Schedule for Friday morning

## Troubleshooting

**"API key not found"**
```bash
# Make sure you exported it:
echo $ANTHROPIC_API_KEY

# Should show your key starting with sk-ant-
```

**"No module named anthropic"**
```bash
# Install requirements:
pip install -r requirements.txt
```

**"No articles found"**
- Check your internet connection
- Some RSS feeds may be temporarily down
- Try again in a few hours

## What's Next?

- Week 1: Send your first newsletter
- Week 2: Gather subscriber feedback
- Week 3: Refine the AI prompts if needed
- Month 2: Consider adding more RSS sources

## Need Help?

1. Check the logs: `output/` folder for generated files
2. Read DEPLOYMENT.md for detailed setup
3. Read README.md for system architecture
4. Test locally before deploying changes

---

**Remember:** The system generates content automatically, but YOU make the final decision on what gets sent. Always review before publishing!

Good luck with your newsletter! 📧
