# QUICK REFERENCE - Common Commands

## Initial Setup Commands

### Navigate to project
```bash
cd /path/to/mortgagelab-newsletter
```

### Install dependencies
```bash
pip3 install -r requirements.txt
```

### Set API key (Mac/Linux)
```bash
export ANTHROPIC_API_KEY='sk-ant-your-key-here'
```

### Set API key (Windows)
```cmd
set ANTHROPIC_API_KEY=sk-ant-your-key-here
```

---

## Testing Commands

### Test RSS feeds only (FREE)
```bash
python3 tests/test_newsletter.py
# Choose option 1
```

### Test full system (~£0.50)
```bash
python3 tests/test_newsletter.py
# Choose option 2
```

### Generate newsletter manually
```bash
python3 generate_newsletter.py
```

### View generated newsletter
```bash
# Mac
open output/newsletter_*.html

# Windows
start output/newsletter_*.html

# Linux
xdg-open output/newsletter_*.html
```

---

## Git Commands

### Initialize repository
```bash
git init
git add .
git commit -m "Initial setup"
```

### Connect to GitHub
```bash
git remote add origin https://github.com/USERNAME/mortgagelab-newsletter.git
git branch -M main
git push -u origin main
```

### Update after changes
```bash
git add .
git commit -m "Updated RSS feeds"
git push
```

---

## File Locations

### RSS feeds configuration
```bash
nano rss_feeds.json
# or
code rss_feeds.json
```

### AI prompts
```bash
nano config/claude_prompts.py
# or
code config/claude_prompts.py
```

### Generated newsletters
```bash
ls output/
```

### Test script
```bash
nano tests/test_newsletter.py
```

---

## GitHub Actions

### View workflow runs
```
https://github.com/YOUR-USERNAME/mortgagelab-newsletter/actions
```

### Manually trigger workflow
1. Go to Actions tab
2. Click "Weekly Newsletter Generation"
3. Click "Run workflow"
4. Click green "Run workflow" button

---

## Troubleshooting Commands

### Check Python version
```bash
python3 --version
# Should be 3.11 or higher
```

### Check Git version
```bash
git --version
```

### Check if API key is set
```bash
# Mac/Linux
echo $ANTHROPIC_API_KEY

# Windows (PowerShell)
echo $env:ANTHROPIC_API_KEY
```

### Reinstall dependencies
```bash
pip3 install -r requirements.txt --upgrade
```

### Check for errors in logs
```bash
cat output/newsletter_*.txt
```

---

## Maintenance Commands

### Update dependencies
```bash
pip3 install -r requirements.txt --upgrade
```

### Clean old output files
```bash
rm output/newsletter_2025-*.html
rm output/articles_*_2025-*.json
```

### Check API usage
```
https://console.anthropic.com/settings/usage
```

---

## Customization Shortcuts

### Change newsletter schedule
```bash
nano .github/workflows/weekly-newsletter.yml
# Edit the cron line
```

### Change number of stories (5 to 7)
```bash
nano generate_newsletter.py
# Find: top_n=5
# Change to: top_n=7
```

### Add RSS feed
```bash
nano rss_feeds.json
# Add new entry in appropriate section
```

---

## Quick Checks

### Did feeds work?
```bash
ls output/articles_raw_*.json
# Should show recent file
```

### Did analysis work?
```bash
ls output/articles_analyzed_*.json
# Should show recent file
```

### Did newsletter generate?
```bash
ls output/newsletter_*.html
# Should show recent HTML file
```

---

## Emergency Commands

### Reset everything
```bash
# Delete all output
rm -rf output/*

# Re-run test
python3 tests/test_newsletter.py
```

### Generate new API key
```
https://console.anthropic.com/settings/keys
```

### Force sync with GitHub
```bash
git fetch origin
git reset --hard origin/main
```

---

## Useful URLs

### Your repository
```
https://github.com/YOUR-USERNAME/mortgagelab-newsletter
```

### GitHub Actions
```
https://github.com/YOUR-USERNAME/mortgagelab-newsletter/actions
```

### Anthropic Console
```
https://console.anthropic.com/
```

### Mailchimp Dashboard
```
https://mailchimp.com/
```

---

## Weekly Workflow

**Thursday 9 AM:** ✓ Automatic (GitHub Actions)

**Thursday PM:**
1. Visit: `https://github.com/YOUR-USERNAME/mortgagelab-newsletter/actions`
2. Click latest run
3. Download artifact
4. Review HTML
5. Paste into Mailchimp
6. Schedule for Friday

**Time:** 15 minutes

---

## Cost Tracking

### View usage
```
https://console.anthropic.com/settings/usage
```

### Expected costs
- Per newsletter: £0.30-0.80
- Per month: £2-4
- Per year: £25-50

---

## Getting Help

### Check logs
```bash
cat output/newsletter_content_*.txt
```

### GitHub Actions logs
1. Go to Actions tab
2. Click failed run
3. Click red ❌ step
4. Read error message

### Documentation
- `README.md` - System overview
- `COMPLETE_INSTRUCTIONS.md` - This guide
- `DEPLOYMENT.md` - Detailed setup
- `QUICKSTART.md` - 15-minute guide

---

**Print this page and keep it handy!** 📋
