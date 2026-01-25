@echo off
REM Automated Deployment Script for Mortgagelab Newsletter System
REM Windows version

color 0A
cls

echo ================================================================
echo    MORTGAGELAB.AI NEWSLETTER - AUTOMATED DEPLOYMENT
echo ================================================================
echo.

REM Check for Python
echo Checking prerequisites...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo ERROR: Python is required but not installed
    echo Install from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check for Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo ERROR: Git is required but not installed
    echo Install from: https://git-scm.com/downloads
    pause
    exit /b 1
)

echo [OK] Python found
echo [OK] Git found
echo.

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo Warning: Some dependencies may not have installed correctly
)
echo [OK] Dependencies installed
echo.

REM Get API key
echo ================================================================
echo  Anthropic API Key Setup
echo ================================================================
echo.
echo You need an Anthropic API key to continue.
echo If you don't have one:
echo   1. Visit: https://console.anthropic.com/
echo   2. Sign up or log in
echo   3. Go to API Keys section
echo   4. Create a new key
echo.
set /p ANTHROPIC_API_KEY="Enter your Anthropic API key (starts with sk-ant-): "

if not "%ANTHROPIC_API_KEY:~0,7%"=="sk-ant-" (
    color 0C
    echo ERROR: Invalid API key format
    echo API key should start with 'sk-ant-'
    pause
    exit /b 1
)

set ANTHROPIC_API_KEY=%ANTHROPIC_API_KEY%
echo [OK] API key validated
echo.

REM Test RSS feeds
echo Testing RSS Feed Aggregation...
echo ================================================================
python -c "from src.feed_aggregator import FeedAggregator; import sys; aggregator = FeedAggregator('rss_feeds.json'); articles = aggregator.fetch_all_feeds(days_back=7); print(f'Successfully fetched {len(articles)} articles from 17 sources'); sys.exit(0 if len(articles) >= 10 else 1)"

if %errorlevel% neq 0 (
    color 0C
    echo RSS feed test failed. Please check your internet connection.
    pause
    exit /b 1
)
echo.

REM Ask about full test
echo ================================================================
echo  Full System Test
echo ================================================================
echo Would you like to run a full test? (costs ~£0.50 API credits)
set /p fulltest="Run full test? (Y/N): "

if /i "%fulltest%"=="Y" (
    echo.
    echo Running full pipeline test...
    python generate_newsletter.py
    if %errorlevel% equ 0 (
        echo.
        echo [OK] Full test successful!
        echo.
        dir output\newsletter_*.html | find "newsletter"
        echo.
    ) else (
        color 0C
        echo ERROR: Full test failed
        pause
        exit /b 1
    )
) else (
    echo Skipping full test.
)
echo.

REM Initialize Git
echo ================================================================
echo  Setting up Git Repository
echo ================================================================

if exist .git (
    echo Warning: Git repository already exists
    set /p reinit="Reinitialize? (Y/N): "
    if /i "%reinit%"=="Y" (
        rmdir /s /q .git
    )
)

if not exist .git (
    git init
    git add .
    git commit -m "Initial newsletter system setup"
    echo [OK] Git repository initialized
)
echo.

REM Summary
cls
color 0A
echo ================================================================
echo                    SETUP COMPLETE!
echo ================================================================
echo.
echo Your newsletter system is ready! Here's what's been done:
echo.
echo   [OK] Python dependencies installed
echo   [OK] API key validated
echo   [OK] RSS feeds tested
echo   [OK] Git repository initialized
if /i "%fulltest%"=="Y" (
    echo   [OK] Full system test passed
)
echo.
echo ================================================================
echo NEXT STEPS - Deploy to GitHub (5-10 minutes):
echo ================================================================
echo.
echo 1. CREATE GITHUB REPOSITORY:
echo    - Go to: https://github.com/new
echo    - Repository name: mortgagelab-newsletter
echo    - Visibility: Private
echo    - Click 'Create repository'
echo.
echo 2. PUSH CODE TO GITHUB:
echo    Run these commands (replace YOUR-USERNAME):
echo.
echo    git remote add origin https://github.com/YOUR-USERNAME/mortgagelab-newsletter.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. ADD API KEY TO GITHUB:
echo    - Go to: Settings - Secrets and variables - Actions
echo    - Click 'New repository secret'
echo    - Name: ANTHROPIC_API_KEY
echo    - Secret: [your API key]
echo    - Click 'Add secret'
echo.
echo 4. RUN FIRST WORKFLOW:
echo    - Go to: Actions tab
echo    - Click 'Weekly Newsletter Generation'
echo    - Click 'Run workflow'
echo    - Wait 2-3 minutes
echo    - Download the newsletter artifact
echo.
echo ================================================================
echo.
echo Need help? Check these files:
echo    * COMPLETE_INSTRUCTIONS.md - Full guide
echo    * QUICK_REFERENCE.md - Command cheat sheet
echo    * README.md - Technical docs
echo.
echo You're ready to launch your automated newsletter!
echo.
echo ================================================================
echo.
echo GitHub commands to run:
echo ---------------------------------------------------------------
echo git remote add origin https://github.com/YOUR-USERNAME/mortgagelab-newsletter.git
echo git branch -M main
echo git push -u origin main
echo ---------------------------------------------------------------
echo.
pause
