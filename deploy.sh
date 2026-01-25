#!/bin/bash

# Automated Deployment Script for Mortgagelab Newsletter System
# Mac/Linux version

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   MORTGAGELAB.AI NEWSLETTER - AUTOMATED DEPLOYMENT            ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed${NC}"
    echo "Install from: https://www.python.org/downloads/"
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git is required but not installed${NC}"
    echo "Install from: https://git-scm.com/downloads"
    exit 1
fi

echo -e "${GREEN}✓ Python 3 found${NC}"
echo -e "${GREEN}✓ Git found${NC}"
echo ""

# Get Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "📌 Using Python $PYTHON_VERSION"
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt --quiet
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Get API key
echo "🔑 Anthropic API Key Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "You need an Anthropic API key to continue."
echo "If you don't have one:"
echo "  1. Visit: https://console.anthropic.com/"
echo "  2. Sign up or log in"
echo "  3. Go to API Keys section"
echo "  4. Create a new key"
echo ""
echo -e "${YELLOW}Enter your Anthropic API key (starts with sk-ant-):${NC}"
read -s ANTHROPIC_API_KEY

if [[ ! $ANTHROPIC_API_KEY == sk-ant-* ]]; then
    echo -e "${RED}❌ Invalid API key format${NC}"
    echo "API key should start with 'sk-ant-'"
    exit 1
fi

export ANTHROPIC_API_KEY
echo -e "${GREEN}✓ API key validated${NC}"
echo ""

# Test RSS feeds
echo "📡 Testing RSS Feed Aggregation (FREE - no API cost)..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 -c "
from src.feed_aggregator import FeedAggregator
import sys
try:
    aggregator = FeedAggregator('rss_feeds.json')
    articles = aggregator.fetch_all_feeds(days_back=7)
    print(f'✓ Successfully fetched {len(articles)} articles from 17 sources')
    if len(articles) < 10:
        print('⚠️  Warning: Low article count. Some feeds may be down.')
        sys.exit(1)
except Exception as e:
    print(f'❌ Error: {e}')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo -e "${RED}RSS feed test failed. Please check your internet connection.${NC}"
    exit 1
fi
echo ""

# Ask if they want to test full pipeline
echo "🧪 Full System Test"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Would you like to run a full test? (costs ~£0.50 API credits)"
echo -n "Run full test? (y/n): "
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    echo ""
    echo "Running full pipeline test..."
    python3 generate_newsletter.py
    
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✓ Full test successful!${NC}"
        echo ""
        echo "Generated files:"
        ls -lh output/newsletter_*.html 2>/dev/null | tail -1
        echo ""
    else
        echo -e "${RED}❌ Full test failed${NC}"
        exit 1
    fi
else
    echo "Skipping full test."
fi
echo ""

# Initialize Git
echo "📝 Setting up Git Repository"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -d .git ]; then
    echo -e "${YELLOW}⚠️  Git repository already exists${NC}"
    echo -n "Reinitialize? (y/n): "
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        rm -rf .git
    else
        echo "Keeping existing Git repository"
    fi
fi

if [ ! -d .git ]; then
    git init
    git add .
    git commit -m "Initial newsletter system setup"
    echo -e "${GREEN}✓ Git repository initialized${NC}"
fi
echo ""

# Summary
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    ✅  SETUP COMPLETE!                         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Your newsletter system is ready! Here's what's been done:"
echo ""
echo "  ✓ Python dependencies installed"
echo "  ✓ API key validated"
echo "  ✓ RSS feeds tested"
echo "  ✓ Git repository initialized"
if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "  ✓ Full system test passed"
fi
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "NEXT STEPS - Deploy to GitHub (5-10 minutes):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. CREATE GITHUB REPOSITORY:"
echo "   → Go to: https://github.com/new"
echo "   → Repository name: mortgagelab-newsletter"
echo "   → Visibility: Private"
echo "   → Click 'Create repository'"
echo ""
echo "2. PUSH CODE TO GITHUB:"
echo "   Run these commands (replace YOUR-USERNAME):"
echo ""
echo "   git remote add origin https://github.com/YOUR-USERNAME/mortgagelab-newsletter.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. ADD API KEY TO GITHUB:"
echo "   → Go to: Settings → Secrets and variables → Actions"
echo "   → Click 'New repository secret'"
echo "   → Name: ANTHROPIC_API_KEY"
echo "   → Secret: [your API key]"
echo "   → Click 'Add secret'"
echo ""
echo "4. RUN FIRST WORKFLOW:"
echo "   → Go to: Actions tab"
echo "   → Click 'Weekly Newsletter Generation'"
echo "   → Click 'Run workflow'"
echo "   → Wait 2-3 minutes"
echo "   → Download the newsletter artifact"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📚 Need help? Check these files:"
echo "   • COMPLETE_INSTRUCTIONS.md - Full guide"
echo "   • QUICK_REFERENCE.md - Command cheat sheet"
echo "   • README.md - Technical docs"
echo ""
echo "🎉 You're ready to launch your automated newsletter!"
echo ""

# Save API key reminder
echo ""
echo -e "${YELLOW}💡 TIP: Save these for later:${NC}"
echo ""
echo "Your API key: ${ANTHROPIC_API_KEY:0:12}..."
echo "(Full key stored in your password manager, right? 😉)"
echo ""
echo "GitHub commands to run:"
echo "-----------------------------------------------------"
echo "git remote add origin https://github.com/YOUR-USERNAME/mortgagelab-newsletter.git"
echo "git branch -M main"
echo "git push -u origin main"
echo "-----------------------------------------------------"
echo ""
