# MLTR Beginner's Guide
## Complete Step-by-Step Setup for Non-Programmers

**Welcome!** This guide will walk you through setting up the MLTR trading system from scratch, even if you've never programmed before.

---

## 📚 Table of Contents

1. [What is MLTR?](#what-is-mltr)
2. [What You'll Need](#what-youll-need)
3. [Installation Guide](#installation-guide)
4. [First Time Setup](#first-time-setup)
5. [Running the System](#running-the-system)
6. [Understanding the Features](#understanding-the-features)
7. [**NEW: Tracking Your Portfolio**](#tracking-your-portfolio)
8. [Daily Usage](#daily-usage)
9. [Troubleshooting](#troubleshooting)

---

## What is MLTR?

**MLTR** stands for **ML Trading Research & Intelligence System**.

Think of it as your personal AI assistant for stock trading that:
- 📊 **Watches** stock prices and news automatically
- 🤖 **Learns** patterns from historical data
- 💡 **Suggests** when to buy or sell stocks
- 📝 **Explains** why it made each suggestion
- 📈 **Gets smarter** over time by learning from its past suggestions

**Important**: This is a **research and learning tool**, not a get-rich-quick system!

---

## What You'll Need

### Hardware (Your Computer)
- **Minimum**: Any laptop with 8GB RAM (like a 5-year-old laptop)
- **Better**: Desktop with 16GB RAM
- **Storage**: 50GB free space (about 50 movies worth)

### Software (All Free!)
- **Windows 10/11**, **macOS**, or **Linux** (any will work)
- **Internet connection** (for downloading data)
- **1-2 hours** of your time for setup

### Knowledge
- ✅ Ability to copy and paste text
- ✅ Basic understanding of stocks (buy low, sell high)
- ❌ NO programming experience needed!

### Money

**For Learning & Backtesting (Free)**:
- ✅ Historical data via yfinance: **FREE**
- ✅ Paper trading (simulated): **FREE**
- ✅ Local LLM models: **FREE**
- ✅ All software tools: **FREE**
- **Total: ₹0/month**

**For Live Trading (Paid)**:
- 📊 Zerodha Kite Connect API: **₹2,000 one-time** (requires Zerodha account)
- 📊 Dhan HQ API: **₹500-1,000/month** (based on plan)
- 📊 Upstox API: **FREE** (requires Upstox account)
- 📊 Real-time data feeds (optional): **$10-50/month**
- **Total: ₹500-2,000/month** (after learning phase)

**Recommendation**: Start with FREE options for 2-3 months. Only upgrade when confident.

---

## Installation Guide

We'll install everything step-by-step. **Don't skip steps!**

### Step 1: Install Python (15 minutes)

**What is Python?** It's the language our system speaks. Think of it like installing Microsoft Word to read Word documents.

#### For Windows:

1. **Download Python**:
   - Go to: https://www.python.org/downloads/
   - Click the big yellow "Download Python 3.11" button
   - A file will download (about 25MB)

2. **Install Python**:
   - Double-click the downloaded file
   - ⚠️ **IMPORTANT**: Check the box "Add Python to PATH" at the bottom!
   - Click "Install Now"
   - Wait 5 minutes
   - Click "Close" when done

3. **Verify It Worked**:
   - Press `Windows Key` + `R`
   - Type: `cmd` and press Enter
   - A black window opens (the "command prompt")
   - Type: `python --version`
   - You should see: `Python 3.11.x`
   - ✅ Success! If not, see [Troubleshooting](#troubleshooting)

#### For macOS:

1. **Open Terminal**:
   - Press `Cmd + Space`
   - Type: `Terminal`
   - Press Enter (a white/black window opens)

2. **Install Homebrew** (a tool installer):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
   - Press Enter when asked
   - Type your password (it won't show, that's normal!)
   - Wait 10 minutes

3. **Install Python**:
   ```bash
   brew install python@3.11
   ```
   - Wait 5 minutes

4. **Verify**:
   ```bash
   python3 --version
   ```
   - Should show: `Python 3.11.x`

### Step 2: Download MLTR (5 minutes)

1. **Open Terminal/Command Prompt** (same as before)

2. **Create a folder** for your project:

   **Windows**:
   ```bash
   cd C:\Users\YourName\Documents
   mkdir MLTR
   cd MLTR
   ```

   **Mac/Linux**:
   ```bash
   cd ~/Documents
   mkdir MLTR
   cd MLTR
   ```

3. **Download the code**:

   Option A - If you have Git:
   ```bash
   git clone https://github.com/yourusername/mltr.git
   cd mltr
   ```

   Option B - No Git (easier):
   - Go to: https://github.com/yourusername/mltr
   - Click green "Code" button → "Download ZIP"
   - Extract the ZIP file to `C:\Users\YourName\Documents\MLTR\` (Windows)
   - Or `~/Documents/MLTR/` (Mac)
   - Open terminal and navigate there:
     ```bash
     cd C:\Users\YourName\Documents\MLTR\mltr-main
     ```

### Step 3: Install Dependencies (30 minutes)

**What are dependencies?** These are helper programs that MLTR needs to work. Like how a car needs wheels, an engine, etc.

1. **Still in Terminal**, run:
   ```bash
   python -m venv venv
   ```
   - This creates a "virtual environment" (an isolated space for our project)
   - Wait 2 minutes

2. **Activate the environment**:

   **Windows**:
   ```bash
   venv\Scripts\activate
   ```

   **Mac/Linux**:
   ```bash
   source venv/bin/activate
   ```

   - You should see `(venv)` appear at the start of your line
   - This means you're "inside" the virtual environment

3. **Install all the helpers**:
   ```bash
   pip install -r requirements.txt
   ```
   - This will download and install ~80 programs
   - **Wait 20-30 minutes** (go get coffee ☕)
   - You'll see lots of text scrolling - that's normal!

4. **Verify installation**:
   ```bash
   python -c "import pandas; print('Success!')"
   ```
   - Should print: `Success!`

---

## First Time Setup

Now we'll configure MLTR with your preferences.

### Step 1: Basic Configuration (5 minutes)

1. **Copy the example config**:
   ```bash
   cp .env.example .env
   cp configs/config.example.yaml configs/config.yaml
   ```

2. **Open config.yaml** in a text editor:
   - **Windows**: Right-click → "Open with" → "Notepad"
   - **Mac**: Right-click → "Open With" → "TextEdit"

   Or use a better editor (recommended):
   - Download **VS Code**: https://code.visualstudio.com/
   - Open VS Code
   - File → Open Folder → Select your MLTR folder
   - Click on `configs/config.yaml` in the sidebar

3. **Edit the basics** (for now, we'll keep it simple):

   Find this section:
   ```yaml
   data:
     market:
       provider: "yfinance"
       universe: "NIFTY50"
   ```

   **What it means**:
   - `provider: "yfinance"` - We'll use free data from Yahoo Finance
   - `universe: "NIFTY50"` - We'll watch the top 50 Indian stocks

   **Change if you want**:
   - Change to `NIFTY100` for 100 stocks (needs more RAM)
   - Change to `NIFTY500` for 500 stocks (needs 16GB RAM)

4. **Save the file** (Ctrl+S or Cmd+S)

### Step 2: Download Initial Data (10 minutes)

Let's download some stock price data to work with:

```bash
python scripts/setup_data.py --universe NIFTY50 --days 365
```

**What this does**:
- Downloads 1 year of stock prices for 50 stocks
- Saves it in the `data/` folder
- Takes about 10 minutes

You'll see:
```
Downloading data for 50 symbols...
[████████████████████] 100%
✓ Data setup complete!
Total rows: 12,500
```

### Step 3: Quick Test (2 minutes)

Let's make sure everything works:

```bash
bash scripts/run_example.sh
```

You should see:
```
==========================================
MLTR Smoke Test
==========================================

Step 1: Checking dependencies...
✓ Core dependencies installed

Step 2: Validating example data...
✓ Example data valid

[... more checks ...]

✓ Smoke test completed!
```

**If you see any ✗ (red X)**, see [Troubleshooting](#troubleshooting).

---

## Running the System

Now the fun part - let's actually use the system!

### Understanding the Parts

MLTR has several parts that work together:

```
┌─────────────────────────────────────┐
│        Dashboard (Web Page)         │ ← What you see
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│     LLM (AI Brain)                  │ ← Makes decisions
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│     ML Models (Pattern Finder)      │ ← Finds patterns
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│     Data (Stock Prices & News)      │ ← What we analyze
└─────────────────────────────────────┘
```

### Starting the Dashboard (Beginner Mode)

The **dashboard** is a web page that shows you everything in a nice, visual way.

1. **Start the dashboard**:
   ```bash
   streamlit run src/dashboard/app.py
   ```

2. **Wait for this message**:
   ```
   You can now view your Streamlit app in your browser.

   Local URL: http://localhost:8501
   ```

3. **Open your web browser** and go to:
   ```
   http://localhost:8501
   ```

4. **You should see**:
   - MLTR logo at the top
   - Sidebar with different pages
   - Main area showing today's signals (will be empty at first)

### Your First Analysis

Let's generate your first trading signal!

#### Step 1: Get Recent Data

In the dashboard:
1. Click **"Data Management"** in the sidebar
2. Click **"Fetch Latest Data"**
3. Select **"Last 7 days"**
4. Click **"Download"**
5. Wait 2-3 minutes

You'll see:
```
✓ Downloaded 350 rows
✓ Data saved to database
```

#### Step 2: Compute Features

**What are features?** These are calculations from the stock prices, like:
- Is the stock going up or down?
- Is it expensive or cheap right now?
- Is trading volume high or low?

In the dashboard:
1. Click **"Features"** in the sidebar
2. Select indicators to compute:
   - ✅ RSI (Relative Strength Index)
   - ✅ MACD (Trend indicator)
   - ✅ Bollinger Bands (Volatility)
3. Click **"Compute Features"**
4. Wait 1 minute

You'll see:
```
✓ Computed RSI for 50 stocks
✓ Computed MACD for 50 stocks
✓ Computed Bollinger Bands for 50 stocks
Total features: 150
```

#### Step 3: Generate Signals (Simple Mode)

For now, we'll use **simple rules** (no machine learning yet):

In the dashboard:
1. Click **"Signals"** in the sidebar
2. Select **"Simple Strategy"**
3. Choose parameters:
   - RSI below: 30 (oversold = might go up)
   - RSI above: 70 (overbought = might go down)
4. Click **"Generate Signals"**

You might see:
```
📊 Found 3 signals:

BUY: RELIANCE
- Current Price: ₹2,450
- RSI: 28 (oversold)
- Confidence: 65%
- Reasoning: RSI indicates stock is oversold and may bounce

SELL: TCS
- Current Price: ₹3,580
- RSI: 72 (overbought)
- Confidence: 60%
- Reasoning: RSI indicates stock is overbought and may correct

[... more signals ...]
```

**Important**: These are **suggestions**, not commands! Always do your own research before trading.

---

## Understanding the Features

Let's explain each part of the system in simple terms.

### 1. Data Collection

**What it does**: Downloads stock prices and news automatically.

**How it works**:
- Every day at 4 PM (after market closes), it downloads today's prices
- It also scrapes news from financial websites
- Everything is saved in a database on your computer

**You need to**:
- Keep your computer on during market hours (optional)
- Or manually click "Fetch Data" once a day

**Example**:
```
Today's Data:
- RELIANCE: Open ₹2,450, Close ₹2,465, Volume: 1.2M
- News: "Reliance announces new project" (Positive sentiment)
```

### 2. Feature Engineering

**What it does**: Calculates useful statistics from raw prices.

**Think of it like**:
- Raw data: "Price is ₹2,450"
- Feature: "Price went up 2% today, up 10% this month, RSI is 65"

**Common features**:

| Feature | What It Means | Good/Bad |
|---------|---------------|----------|
| **RSI < 30** | Stock is oversold (cheap) | 🟢 Might go up soon |
| **RSI > 70** | Stock is overbought (expensive) | 🔴 Might go down soon |
| **MACD crosses up** | Upward trend starting | 🟢 Good to buy |
| **Volume spike** | Lots of people trading | ⚠️ Big move coming |
| **News sentiment +0.8** | Very positive news | 🟢 Good sign |

**You need to**:
- Click "Compute Features" after downloading data
- Or set it to auto-compute (we'll cover later)

### 3. Machine Learning Models

**What it does**: Learns patterns from historical data to predict future prices.

**How it works** (simplified):
1. Show the model 1000s of examples: "When RSI was 25 and MACD crossed up, price went up 80% of the time"
2. Model learns: "Low RSI + MACD cross = probably good buy"
3. When it sees this pattern again, it suggests buying

**Think of it like**:
- A doctor seeing 10,000 patients and learning: "Fever + cough + fatigue = probably flu"
- Our model sees 10,000 stock movements and learns: "Low RSI + positive news = probably going up"

**You need to**:
- Initially: Nothing! We provide pre-trained models
- Later: Click "Retrain Models" once a month to keep them fresh

### 4. Signal Generation

**What it does**: Converts predictions into actionable buy/sell suggestions.

**Example Signal**:
```
🟢 BUY: RELIANCE

Entry Price: ₹2,450
Stop Loss: ₹2,400 (sell if it drops here - limits loss to 2%)
Target: ₹2,550 (sell if it reaches here - take 4% profit)

Confidence: 72%

Reasoning:
- RSI: 28 (oversold)
- MACD: Bullish crossover
- News sentiment: +0.65 (positive)
- Historical: Similar setups worked 72% of the time

Position Size: 40 shares (₹98,000 investment)
Risk: ₹2,000 (2% of ₹100,000 capital)
```

**What each part means**:
- **Entry Price**: Buy at this price
- **Stop Loss**: If price drops to ₹2,400, sell immediately (limits your loss)
- **Target**: If price reaches ₹2,550, sell and take profit
- **Confidence**: How sure the system is (72% = pretty confident)
- **Position Size**: How many shares to buy based on your risk tolerance

### 5. Backtesting

**What it does**: Tests if a strategy would have worked in the past.

**Example**:
```
Testing Strategy: "Buy when RSI < 30"
Period: Jan 2023 - Oct 2024

Results:
- Total Trades: 156
- Wins: 89 (57%)
- Losses: 67 (43%)
- Average Win: +3.2%
- Average Loss: -1.8%
- Overall Return: +24% (vs market +15%)
- Max Drawdown: -8% (worst losing streak)
```

**Why it's important**:
- You can test strategies without risking real money
- See if a strategy actually works before using it

**You need to**:
- Click "Backtest" → Select strategy → Select date range → Run
- Wait 5-10 minutes for results

### 6. LLM Orchestration

**What it does**: The LLM (Language Model) is the "brain" that coordinates everything and explains decisions in plain English.

**Example conversations with the LLM**:

You: "Why did you suggest buying Reliance?"

LLM: "I suggested buying Reliance because:
1. The RSI is 28, which historically means the stock is oversold and tends to bounce back
2. There's been positive news about their new energy project (sentiment: +0.7)
3. The price recently broke above the 20-day moving average, indicating a potential trend change
4. In similar situations over the past 2 years, this setup worked 72% of the time

The risk/reward is favorable: potential gain of ₹100 vs risk of ₹50 per share."

**Cool features**:
- Ask questions in plain English
- Get explanations for every signal
- Request custom backtests: "Test buying INFY when RSI < 25 and news is positive"

---

## Tracking Your Portfolio

**NEW FEATURE**: MLTR now tracks your actual trades and helps protect your portfolio!

### What is Portfolio Tracking?

Think of it as a **smart diary** that:
- ✅ Remembers what signals the AI suggested
- ✅ Tracks what you actually bought/sold
- ✅ Warns you if a stock you own is falling fast
- ✅ Helps the AI learn from your real results

**Why this matters**: The AI can suggest "BUY", but did you actually buy? This feature bridges that gap.

---

### Setting Up Portfolio Tracking (5 minutes)

#### Step 1: Enable Portfolio Tracking

```bash
# Create portfolio tracker
python -c "
from src.portfolio import PortfolioTracker
tracker = PortfolioTracker(db_path='data/portfolio.db')
print('✓ Portfolio tracker created!')
"
```

You should see: `✓ Portfolio tracker created!`

#### Step 2: Connect Your Broker (Optional but Recommended)

**Option A: Automatic Sync (Zerodha, Upstox)**

If you have Zerodha account:

```bash
# Interactive setup
python scripts/setup_broker.py
```

Follow the prompts:
1. Choose broker: `zerodha`
2. Enter API key (from https://kite.trade)
3. Enter access token
4. Done! Your holdings will sync automatically

**Option B: Manual Entry (Any Broker)**

If your broker isn't supported or you prefer manual control:

```python
# Add a holding manually
from src.portfolio import PortfolioTracker
from datetime import datetime

tracker = PortfolioTracker(db_path='data/portfolio.db')

# Record what you bought
tracker.record_trade(
    symbol="RELIANCE",
    trade_type="BUY",
    price=2450.50,        # What you paid per share
    quantity=100,         # How many shares
    timestamp=datetime.now(),
    commission=20.0,      # Brokerage fee
    notes="First purchase"
)

print("✓ Trade recorded!")
```

**Option C: Import from CSV (Easiest for Bulk)**

If you have existing holdings, create a CSV file:

```csv
symbol,quantity,avg_price
RELIANCE,100,2450.50
TCS,50,3200.00
INFY,200,1445.00
```

Then import:

```bash
python -m src.cli portfolio import --holdings my_holdings.csv
```

---

### How to Use Portfolio Tracking

#### 1. Recording Signals and Trades

**When AI suggests a trade**:

```python
from src.portfolio import PortfolioTracker
from datetime import datetime

tracker = PortfolioTracker(db_path='data/portfolio.db')

# AI says "BUY RELIANCE"
signal_id = tracker.record_signal(
    symbol="RELIANCE",
    signal_type="BUY",
    price=2450.00,           # Price when signal generated
    timestamp=datetime.now(),
    confidence=0.85          # How confident AI is (0 to 1)
)

print(f"Signal recorded: ID {signal_id}")
```

**When you actually execute the trade**:

```python
# You bought it!
tracker.record_trade(
    symbol="RELIANCE",
    trade_type="BUY",
    price=2451.00,           # Actual execution price
    quantity=100,
    timestamp=datetime.now(),
    signal_id=signal_id,     # Link to the signal
    commission=20.0
)

print("✓ Trade recorded and linked to signal!")
```

**Why link them?** This tells the AI: "I followed your advice, let's see how it goes!"

#### 2. Checking Your Holdings

```python
# What do I own right now?
holdings = tracker.get_current_holdings()
print(holdings)
```

Output:
```
   symbol  quantity  avg_price  current_price  market_value  unrealized_pnl
0  RELIANCE    100    2450.50       2520.00     252000         6950.00
1  TCS          50    3200.00       3180.00     159000        -1000.00
2  INFY        200    1445.00       1460.00     292000         3000.00
```

**What this shows**:
- You own 100 shares of RELIANCE, bought at avg ₹2450.50
- Current price ₹2520, so you're up ₹6,950
- TCS is down ₹1,000 (not good, watch this!)
- Total portfolio: ₹703,000

#### 3. Emergency Alerts (YOUR SAFETY NET!)

**This is the most important feature** - it warns you when something dangerous is happening!

```python
from src.portfolio import EmergencyAlertSystem

# Create alert system
alerts = EmergencyAlertSystem()

# Check your RELIANCE position
alert = alerts.check_position(
    symbol="RELIANCE",
    current_price=2250,      # Stock dropped!
    avg_price=2450,          # Your purchase price
    quantity=100,
    day_open=2400,           # Today's open
    day_high=2420,
    day_low=2240
)

if alert:
    print(f"🚨 ALERT: {alert['message']}")
    print(f"Action: {alert['action']}")
```

Output:
```
🚨 ALERT: RELIANCE down 8.2% from your average price!
Action: Consider reviewing stop-loss. Current loss: ₹20,000
```

**What triggers alerts?**

| Situation | Alert | What to Do |
|-----------|-------|------------|
| Stock down >5% today | 🚨 INTRADAY_DROP | Check news, consider exit |
| Position loss >10% | ⚠️ POSITION_LOSS | Review stop-loss |
| Hit stop-loss price | 🚨 STOP_LOSS_HIT | **EXIT IMMEDIATELY** |
| Volume 3x normal | ⚡ VOLUME_SPIKE | Check for news |
| Approaching circuit limit | 🚨 CIRCUIT_LIMIT | Exit difficult! Act now |
| Portfolio down >15% | ⚠️ PORTFOLIO_DRAWDOWN | Reduce exposure |

**Set up automatic alerts** (runs every hour during market):

```bash
# Add to your crontab (Linux/Mac)
0 10-15 * * 1-5 python scripts/check_alerts.py

# Or on Windows, use Task Scheduler
```

#### 4. Did You Follow the Signals?

**Execution Rate** tells you: "What % of AI signals did I actually execute?"

```python
# Check last 30 days
rate = tracker.get_execution_rate(days=30)
print(f"You followed {rate*100:.1f}% of signals")
```

Output: `You followed 68.5% of signals`

**What's a good rate?**
- 80-100%: You trust the AI a lot (risky if AI is wrong!)
- 50-70%: **Ideal** - You use judgment
- <30%: Why run the AI if you ignore it?

**See which signals you followed**:

```python
performance = tracker.get_signal_performance()
print(performance.head(10))
```

Output:
```
   symbol  signal_type  signal_price  confidence  executed  execution_price  outcome
0  RELIANCE  BUY         2450.00      0.85       True      2451.00         +5.2%
1  TCS       SELL        3200.00      0.72       True      3198.00         +2.1%
2  INFY      BUY         1445.00      0.68       False     -               +8.3% (MISSED)
3  WIPRO     SELL        420.00       0.55       True      419.50          -1.5%
```

**Key insight**: You missed INFY which went up 8.3%! Maybe lower your confidence threshold.

#### 5. Helping the AI Learn (Feedback Loop)

**The magic part**: Your actual results teach the AI!

```python
# Generate feedback for a signal
feedback = tracker.generate_ml_feedback(
    symbol="RELIANCE",
    signal_id=123
)

print(feedback)
```

Output:
```python
{
    "symbol": "RELIANCE",
    "signal_id": 123,
    "followed": True,
    "outcome": "PROFIT",
    "return_pct": 5.2,
    "recommendation": "Good trade! Model prediction was accurate."
}
```

**How AI uses this**:

| Your Result | AI Learns |
|-------------|-----------|
| ✅ Followed signal → Profit | "These features work! Use more." |
| ❌ Followed signal → Loss | "These features failed. Use less." |
| 🤔 Ignored signal → Would've profited | "Increase confidence threshold." |
| 😅 Ignored signal → Would've lost | "Good! Model needs retraining." |

**Run monthly feedback**:

```bash
# Analyze last 30 days and update models
python scripts/generate_feedback.py --days 30
```

This creates a `ml_feedback.csv` that the AI uses to improve.

---

### Dashboard: See Everything in One Place

The Streamlit dashboard shows your portfolio:

```bash
streamlit run src/dashboard/app.py
```

Navigate to **"My Portfolio"** tab:

#### What you'll see:

**1. Current Holdings**
```
Symbol    Qty   Avg Price  Current  P&L      P&L %    Action
RELIANCE  100   ₹2,450    ₹2,520   +₹7,000  +2.9%    🟢 Hold
TCS       50    ₹3,200    ₹3,180   -₹1,000  -0.6%    🟡 Watch
INFY      200   ₹1,445    ₹1,460   +₹3,000  +1.0%    🟢 Hold
```

**2. Active Alerts** (last 24 hours)
```
🚨 CRITICAL - TCS approaching stop-loss!
   Current: ₹3,180 | Stop-Loss: ₹3,168 (-1% away)
   Action: Consider exiting position
```

**3. Signal Execution Summary**
```
Last 30 Days:
- Signals generated: 24
- Signals executed: 18 (75.0%)
- Profitable trades: 13 (72.2%)
- Average return: +3.4%
```

**4. Comparison Chart**
- Blue line: If you followed ALL signals
- Green line: Your actual performance
- This shows if you're beating or lagging the AI

---

### Real-World Example: Full Workflow

Let's walk through a complete day:

**9:00 AM** - Before market opens

```bash
# Run daily analysis
python scripts/daily_routine.py
```

Output:
```
📊 Today's Signals:
1. BUY RELIANCE at ₹2,450 (Confidence: 85%)
2. SELL TCS at ₹3,200 (Confidence: 72%)
3. HOLD INFY (Confidence: 55%)

🚨 Active Alerts:
- No critical alerts

✓ Ready for market open
```

**9:30 AM** - You decide to follow the RELIANCE signal

In your broker app:
- Buy 100 RELIANCE @ ₹2,451

In MLTR:
```python
tracker.record_trade(
    symbol="RELIANCE",
    trade_type="BUY",
    price=2451.00,
    quantity=100,
    timestamp=datetime.now(),
    signal_id=get_today_signal_id("RELIANCE"),  # Links to AI's suggestion
    commission=20.0
)
```

**2:30 PM** - RELIANCE drops to ₹2,320

Your phone buzzes (email/Telegram alert):
```
🚨 CRITICAL ALERT
RELIANCE down 5.3% today!
Current: ₹2,320
Your avg: ₹2,451
Loss: ₹13,100

Action: Check news. Consider exit.
```

You check news:
- "Reliance Q4 earnings miss estimates"

Decision: Exit to limit losses

```python
tracker.record_trade(
    symbol="RELIANCE",
    trade_type="SELL",
    price=2320.00,
    quantity=100,
    timestamp=datetime.now(),
    notes="Exiting due to bad earnings"
)
```

**End of Week** - Review performance

```bash
# Generate weekly report
python scripts/weekly_report.py
```

Output:
```
📊 Week Summary:
- Total trades: 8
- Profitable: 5 (62.5%)
- Average return: +1.2%
- Portfolio value: ₹712,000 (+1.3%)

💡 AI Feedback:
- RELIANCE signal (loss): Earnings calendar not checked
- INFY signal (ignored, went up 8%): Consider lowering confidence threshold
- TCS signal (profit): Good exit timing

✅ Action Items:
1. Add earnings date filter to signals
2. Lower confidence threshold from 0.7 to 0.6
3. Review stop-loss strategy (too tight?)
```

**This feedback makes the AI smarter** for next week!

---

### Advanced: Broker Auto-Sync

Once set up, your portfolio updates automatically:

```yaml
# In configs/config.yaml
portfolio:
  broker: zerodha
  sync_frequency: hourly

  alerts:
    enabled: true
    notifications:
      - console
      - email       # Your email
      - telegram    # Telegram bot (optional)
```

Now every hour:
1. MLTR fetches your latest holdings from Zerodha
2. Checks for emergency situations
3. Sends alerts if needed
4. Updates dashboard

**You do nothing!** It's all automatic.

---

### FAQ: Portfolio Tracking

**Q: What if I trade with multiple brokers?**

A: Import CSV from each broker and merge:

```bash
python -m src.cli portfolio import --holdings zerodha_holdings.csv
python -m src.cli portfolio import --holdings upstox_holdings.csv --merge
```

**Q: Can I track non-Indian stocks (US, etc.)?**

A: Yes! The tracker works with any symbol:

```python
tracker.record_trade(symbol="AAPL", ...)  # Apple
tracker.record_trade(symbol="TSLA", ...)  # Tesla
```

**Q: What if I forgot to record a trade?**

A: Add it retroactively:

```python
from datetime import datetime, timedelta

# Trade from 3 days ago
past_time = datetime.now() - timedelta(days=3)
tracker.record_trade(
    symbol="RELIANCE",
    trade_type="BUY",
    price=2450.00,
    quantity=100,
    timestamp=past_time  # Backdated
)
```

**Q: How do I export my portfolio for taxes?**

A:
```bash
# Export all trades to CSV
python -m src.cli portfolio export --year 2025 --output trades_2025.csv
```

**Q: Does this track mutual funds / crypto?**

A: Currently stocks only. Crypto support planned for v0.2.

**Q: Is my portfolio data secure?**

A: Yes! Stored locally in encrypted database. Never sent to cloud (unless you enable cloud backup).

---

## Daily Usage

Here's your typical daily workflow (updated with portfolio tracking):

### Morning Routine (5 minutes) - Before Market Opens (9:15 AM)

1. **Check overnight news**:
   ```bash
   python scripts/fetch_news.py
   ```
   Or in dashboard: Click "News" → "Fetch Latest"

2. **Review yesterday's signals**:
   - Dashboard → "Past Signals"
   - See which signals were right/wrong
   - System learns from this automatically

3. **Get today's signals**:
   - Dashboard → "Generate Signals"
   - Review each signal
   - Decide which ones to act on

### During Market Hours (Optional)

The system can run automatically:

```bash
python scripts/live_monitor.py
```

This will:
- Update prices every minute
- Generate intraday signals if opportunities arise
- Send notifications if enabled

### Evening Routine (10 minutes) - After Market Close (3:30 PM)

1. **Download today's data**:
   ```bash
   python scripts/fetch_data.py --date today
   ```

2. **Update features**:
   ```bash
   python scripts/compute_features.py
   ```

3. **Log your trades** (if you made any):
   - Dashboard → "Trade Log"
   - Enter: Symbol, Entry Price, Exit Price
   - System learns from your actual results

4. **Review performance**:
   - Dashboard → "Performance"
   - See your win rate, average profit, etc.

### Weekly Routine (30 minutes) - Sunday Morning

1. **Retrain models** on latest data:
   ```bash
   python scripts/train_models.py
   ```
   - Takes 20-30 minutes
   - Models learn from the past week

2. **Run indicator league**:
   ```bash
   python scripts/indicator_league.py
   ```
   - Tests which indicators are working best
   - System adjusts automatically

3. **Review weekly report**:
   - Dashboard → "Reports" → "Weekly Summary"
   - See what worked, what didn't
   - Make adjustments

### Monthly Routine (1 hour) - First Sunday of Month

1. **Full backtest** of all strategies:
   ```bash
   python scripts/full_backtest.py --months 3
   ```

2. **Review and update**:
   - Which strategies are still working?
   - Any new patterns emerging?
   - Adjust confidence thresholds if needed

3. **System health check**:
   ```bash
   python scripts/health_check.py
   ```
   - Verifies all components working
   - Checks for data quality issues

---

## Troubleshooting

### Common Issues and Solutions

#### 1. "Python not found" or "python: command not found"

**Problem**: Python isn't installed or not in PATH

**Solution**:
- **Windows**: Reinstall Python, CHECK the "Add to PATH" box
- **Mac/Linux**: Use `python3` instead of `python` in all commands

#### 2. "Module not found" errors

**Problem**: Dependencies not installed

**Solution**:
```bash
# Make sure venv is activated (you see "(venv)" in terminal)
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

#### 3. "Out of memory" error

**Problem**: Your computer doesn't have enough RAM

**Solution**:
- Reduce the universe in `config.yaml`:
  ```yaml
  data:
    market:
      universe: "NIFTY50"  # Change from NIFTY500
  ```
- Close other programs
- Restart your computer

#### 4. Data download fails

**Problem**: Network issues or API limits

**Solution**:
```bash
# Try again with delay between requests
python scripts/setup_data.py --universe NIFTY50 --days 365 --delay 2
```

#### 5. Dashboard won't load

**Problem**: Port 8501 is already in use

**Solution**:
```bash
# Use a different port
streamlit run src/dashboard/app.py --server.port 8502
# Then go to http://localhost:8502
```

#### 6. Signals seem random or inaccurate

**Problem**: Not enough data or models not trained

**Solution**:
1. Download at least 2 years of data:
   ```bash
   python scripts/setup_data.py --universe NIFTY50 --days 730
   ```

2. Train models:
   ```bash
   python scripts/train_models.py
   ```

3. Wait a few weeks of real data before trusting signals

### Getting Help

1. **Check logs**:
   ```bash
   cat logs/mltr.log
   ```

2. **Run diagnostics**:
   ```bash
   python scripts/diagnose.py
   ```

3. **Ask the community**:
   - Open an issue on GitHub
   - Join our Discord (link in README)
   - Search existing issues first!

---

## Next Steps

Now that you've got the basics down:

1. **Read**: [ML_EXPLAINED.md](ML_EXPLAINED.md) - Understand how the machine learning works
2. **Read**: [LLM_SETUP_GUIDE.md](LLM_SETUP_GUIDE.md) - Set up the AI brain
3. **Read**: [FEATURES_GUIDE.md](FEATURES_GUIDE.md) - Deep dive into each feature
4. **Watch**: Video tutorials (coming soon!)
5. **Experiment**: Try different strategies and see what works

**Remember**:
- Start small (paper trading or tiny amounts)
- Learn from mistakes
- Be patient - it takes time to get good
- Never invest money you can't afford to lose

---

## Safety Reminders

⚠️ **CRITICAL WARNINGS**:

1. **This is NOT financial advice** - Always do your own research
2. **Start with paper trading** - Practice without real money first
3. **Never invest more than you can afford to lose**
4. **Past performance ≠ future results** - What worked before might not work now
5. **Check every signal manually** - Don't blindly follow suggestions
6. **Use stop losses** - Always limit your downside risk
7. **Diversify** - Don't put all money in one stock
8. **Keep learning** - Markets change, you need to adapt

**Legal Disclaimer**:
- You are solely responsible for your trading decisions
- The creators are not liable for any financial losses
- This tool is for educational purposes
- Consult a licensed financial advisor before trading

---

## Glossary

Simple definitions of terms used in this guide:

| Term | Simple Definition |
|------|-------------------|
| **API** | A way for programs to talk to each other (like a phone line between apps) |
| **Backtest** | Testing a strategy on historical data to see if it would have worked |
| **CLI** | Command Line Interface - the black window where you type commands |
| **Dashboard** | The pretty web page that shows everything visually |
| **Feature** | A calculated value from raw data (like "price went up 5% today") |
| **LLM** | Large Language Model - the AI that understands and explains in English |
| **ML Model** | Machine Learning Model - the part that learns patterns and makes predictions |
| **RSI** | Relative Strength Index - shows if a stock is overbought (expensive) or oversold (cheap) |
| **Signal** | A suggestion to buy or sell a stock |
| **Stop Loss** | A price where you automatically sell to limit your loss |
| **Terminal** | The window where you type commands (Command Prompt on Windows) |
| **Virtual Environment** | An isolated space for your project's dependencies |

---

**Congratulations!** You've completed the beginner's guide. You're now ready to start exploring MLTR!

Remember: Start slow, learn continuously, and never risk more than you can afford to lose.

Happy trading! 📈

---

**Need Help?**
- 📧 Email: support@example.com
- 💬 Discord: [Join here]
- 📖 Docs: [Read more guides]
- 🐛 Issues: [Report bugs on GitHub]
