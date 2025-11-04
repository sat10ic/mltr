# LLM Setup Guide
## Setting Up the AI Brain (For Beginners)

**Welcome!** This guide shows you how to set up the Language Model (LLM) - the AI brain that talks to you in English and orchestrates everything.

---

## 📚 Table of Contents

1. [What is an LLM?](#what-is-an-llm)
2. [Why Do We Need It?](#why-do-we-need-it)
3. [Choosing Your LLM](#choosing-your-llm)
4. [Installation Guide](#installation-guide)
5. [First Conversation](#first-conversation)
6. [Using LLM for Trading](#using-llm-for-trading)
7. [**NEW: Portfolio Monitoring with LLM**](#portfolio-monitoring-with-llm)
8. [Advanced Features](#advanced-features)
9. [Troubleshooting](#troubleshooting)

---

## What is an LLM?

**LLM** = **Large Language Model**

### Simple Explanation

An LLM is an AI that:
- 📖 Reads and understands text (English, code, data)
- 💬 Talks back to you in natural language
- 🧠 Can reason and make decisions
- 🔧 Can use tools to get things done

**Think of it like**:
- A super-smart assistant who understands trading
- Can read all your data and explain it
- Takes your English commands and converts them to actions
- Explains complex patterns in simple terms

### Examples of LLMs

You might have heard of:
- **ChatGPT** (by OpenAI) - Costs money, runs on their servers
- **Claude** (by Anthropic) - Costs money, runs on their servers
- **Qwen** (by Alibaba) - FREE, runs on YOUR computer! ✓
- **LLaMA** (by Meta) - FREE, runs on YOUR computer! ✓

We use **Qwen** or **LLaMA** because:
- ✅ Completely free
- ✅ Runs locally (private, your data stays on your computer)
- ✅ Fast enough for trading (responds in 1-2 seconds)
- ✅ Good enough for our needs

---

## Why Do We Need It?

### Without LLM (Traditional Approach)

You have to learn code to do anything:

```python
# Want to backtest?
from src.backtest import BacktestEngine
engine = BacktestEngine()
results = engine.run(
    strategy="momentum",
    symbols=["RELIANCE", "TCS"],
    start="2023-01-01",
    end="2024-01-01",
    params={"rsi_threshold": 30}
)
print(results.sharpe)
```

This is hard if you don't know Python!

### With LLM (Natural Language)

Just talk to it normally:

```
You: "Backtest a momentum strategy on Reliance and TCS for 2023,
      using RSI threshold of 30"

LLM: "Running backtest now..."
     [executes the code above automatically]
     "Done! Here are the results:
      - Sharpe ratio: 1.45
      - Total return: +24%
      - Win rate: 72%

      This strategy performed well. The Sharpe ratio of 1.45 indicates
      good risk-adjusted returns. Would you like me to try different
      parameters to see if we can improve it?"
```

**Much easier!** No coding required.

### What LLM Does in MLTR

1. **Natural Language Interface**:
   - You: "Show me stocks with RSI below 30"
   - LLM: Searches data, shows results

2. **Explains Signals**:
   - LLM: "I suggest buying Reliance because RSI is 28 (oversold),
          news sentiment is positive (+0.7), and similar setups worked
          72% of the time historically. Risk/reward is 1:2."

3. **Orchestrates Tasks**:
   - You: "Train a new model, backtest it, and generate signals"
   - LLM: Coordinates all three steps automatically

4. **Learns from Research**:
   - You: Upload a PDF about momentum strategies
   - LLM: Reads it, understands it, applies the concepts

5. **Answers Questions**:
   - You: "Why did my signal fail?"
   - LLM: Analyzes the trade, explains what went wrong

---

## Choosing Your LLM

We support several options. Here's a comparison:

| Model | Size | RAM Needed | Speed | Quality | Best For |
|-------|------|------------|-------|---------|----------|
| **Qwen 2.5 3B** | 2GB | 8GB | Very fast | Good | Low-end computers, learning |
| **Qwen 2.5 7B** | 4GB | 16GB | Fast | Great | Recommended! |
| **Qwen 2.5 14B** | 8GB | 32GB | Medium | Excellent | High-end computers |
| **LLaMA 3 8B** | 5GB | 16GB | Fast | Great | Alternative to Qwen 7B |
| **LLaMA 3 70B** | 40GB | 64GB + GPU | Slow | Amazing | Servers only |

### Recommendation for Beginners

**Start with Qwen 2.5 7B** (quantized to 4-bit):
- Good balance of speed and quality
- Works on most modern computers (16GB RAM)
- Fast enough for real-time trading (1-2 sec response)
- Smart enough to handle complex questions

### If Your Computer is Weak

Use **Qwen 2.5 3B**:
- Works on 8GB RAM
- Responds in < 1 second
- Still pretty smart for basic tasks
- You can always upgrade later

### If You Have a Gaming PC

Use **Qwen 2.5 14B** or **LLaMA 3 8B** with GPU:
- Much faster (10x)
- Smarter responses
- Can handle very complex reasoning

---

## Installation Guide

Let's install the LLM step-by-step.

### Option 1: Using Ollama (Easiest - Recommended)

**Ollama** is a tool that makes running LLMs super easy (like Docker for AI models).

#### Step 1: Install Ollama (5 minutes)

**Windows**:
1. Go to: https://ollama.com/download/windows
2. Download the installer
3. Run it, click "Next" a few times
4. Done!

**Mac**:
1. Go to: https://ollama.com/download/mac
2. Download the installer
3. Drag to Applications folder
4. Open Ollama from Applications

**Linux**:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### Step 2: Download the Model (10 minutes)

Open Terminal/Command Prompt:

```bash
# Download Qwen 2.5 7B (4GB download)
ollama pull qwen2.5:7b

# Wait 10 minutes for download...
# ████████████████████] 100%
```

#### Step 3: Test It

```bash
ollama run qwen2.5:7b "What is RSI in stock trading?"
```

You should see:
```
RSI stands for Relative Strength Index. It's a momentum indicator
that measures the speed and magnitude of price movements...
[detailed explanation]
```

**Works!** ✅

#### Step 4: Configure MLTR

Edit `configs/config.yaml`:

```yaml
llm:
  model:
    provider: "ollama"
    model_name: "qwen2.5:7b"

  inference:
    temperature: 0.7  # Creativity (0=robotic, 1=creative)
    max_tokens: 2048  # Max response length
```

Save and you're done!

### Option 2: Using llama.cpp (More Control)

If Ollama doesn't work or you want more control:

#### Step 1: Install llama.cpp

```bash
pip install llama-cpp-python
```

#### Step 2: Download Model File

Go to Hugging Face and download the model:

1. Visit: https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF
2. Download: `qwen2.5-7b-instruct-q4_k_m.gguf` (4GB)
3. Save to: `models/llm/` folder in your MLTR directory

**Or use command line**:

```bash
mkdir -p models/llm
cd models/llm

# Download using huggingface-cli
pip install huggingface-hub
huggingface-cli download Qwen/Qwen2.5-7B-Instruct-GGUF \
    qwen2.5-7b-instruct-q4_k_m.gguf \
    --local-dir .
```

#### Step 3: Configure MLTR

Edit `configs/config.yaml`:

```yaml
llm:
  model:
    provider: "llamacpp"
    model_path: "models/llm/qwen2.5-7b-instruct-q4_k_m.gguf"

  inference:
    n_ctx: 4096  # Context window
    n_threads: 8  # CPU threads
    n_gpu_layers: 0  # 0 for CPU, 35 for GPU
```

#### Step 4: Test It

```bash
python scripts/test_llm.py
```

You should see:
```
Loading model...
✓ Model loaded successfully

Testing query...
Query: "Explain RSI indicator"
Response: "RSI stands for Relative Strength Index..."

✓ LLM working correctly!
```

---

## First Conversation

Let's chat with your LLM!

### Start the Chat Interface

```bash
python src/llm/chat.py
```

You'll see:
```
=== MLTR LLM Chat ===
Type 'quit' to exit
Type 'help' for available commands

You:
```

### Example Conversations

**Example 1: Basic Question**

```
You: What is a good RSI value for buying?

LLM: For buying opportunities, look for RSI values below 30. This
     indicates the stock is "oversold" - meaning it has dropped
     significantly and may be due for a bounce back up.

     However, don't rely on RSI alone! Combine it with:
     - Positive news sentiment
     - Volume confirmation
     - Overall market trend

     An RSI between 25-30 with positive sentiment gives you about
     70-75% success rate historically in our data.
```

**Example 2: Analyze Stock**

```
You: Analyze RELIANCE for me

LLM: Fetching latest data for RELIANCE...

     Current Analysis (as of Nov 3, 2024):

     Price: ₹2,450
     RSI: 32 (slightly oversold, neutral to bullish)
     MACD: Bullish crossover yesterday
     Volume: 1.5x average (increased interest)
     News Sentiment: +0.65 (positive)

     Technical Signals:
     - RSI at 32 suggests mild oversold condition
     - MACD crossover indicates potential upward momentum
     - Price above 20-day moving average (₹2,420)

     Sentiment Analysis:
     - Recent news about new energy project (positive)
     - Analyst upgrades this week
     - Sector performing well

     Recommendation: MODERATE BUY
     Confidence: 68%

     Entry: ₹2,445-2,455
     Stop Loss: ₹2,390 (2.4% risk)
     Target: ₹2,545 (4% gain)
     Risk/Reward: 1:1.7
```

**Example 3: Run Backtest**

```
You: Backtest buying when RSI < 25 on NIFTY50 stocks for 2023

LLM: Running backtest with parameters:
     - Strategy: Buy when RSI < 25
     - Universe: NIFTY50 (50 stocks)
     - Period: Jan 1, 2023 - Dec 31, 2023

     [Running... this will take 2 minutes]

     Results:

     Performance:
     - Total trades: 47
     - Wins: 34 (72%)
     - Losses: 13 (28%)
     - Average win: +3.8%
     - Average loss: -1.6%
     - Net return: +28.4%
     - Sharpe ratio: 1.52

     Best trades:
     1. TCS on March 15: +8.2%
     2. INFY on July 3: +6.4%
     3. RELIANCE on Sep 22: +5.9%

     Worst trades:
     1. TATAMOTORS on Feb 8: -4.2%
     2. ADANIPORTS on Nov 12: -3.1%

     Analysis:
     The strategy worked well in 2023, with a 72% win rate. It
     performed best in consolidating markets and struggled during
     strong downtrends. Consider adding a trend filter (like MACD)
     to avoid buying in strong downtrends.

     Would you like me to test with a trend filter added?
```

### Available Commands

While in chat, you can use special commands:

| Command | What It Does |
|---------|--------------|
| `/help` | Show all available commands |
| `/signals` | Generate trading signals for today |
| `/backtest <params>` | Run a backtest |
| `/analyze <symbol>` | Deep analysis of a stock |
| `/explain <signal_id>` | Explain why a signal was generated |
| `/performance` | Show your trading performance |
| `/learn <topic>` | Teach LLM about a concept |
| `/reset` | Start fresh conversation |
| `/quit` | Exit chat |

---

## Using LLM for Trading

Let's see how to use the LLM for actual trading tasks.

### Daily Morning Routine

Start your day by asking the LLM:

```
You: What are the best opportunities today?

LLM: Analyzing market data from this morning...

     Top 3 Opportunities (High Confidence):

     1. HDFCBANK - BUY
        Current: ₹1,580
        RSI: 27 (oversold)
        Sentiment: +0.72 (positive earnings report)
        Confidence: 78%
        Target: ₹1,640 (+3.8%)
        Stop: ₹1,545 (-2.2%)

     2. INFY - BUY
        Current: ₹1,420
        RSI: 31 (oversold)
        MACD: Bullish cross
        Confidence: 72%
        Target: ₹1,475 (+3.9%)
        Stop: ₹1,390 (-2.1%)

     3. RELIANCE - SELL
        Current: ₹2,480
        RSI: 76 (overbought)
        Volume declining
        Confidence: 65%
        Target: ₹2,390 (-3.6%)
        Stop: ₹2,520 (+1.6%)

     Market Conditions:
     - Overall sentiment: Neutral
     - Volatility: Medium
     - Best time to enter: 10:00-11:00 AM

     Would you like detailed analysis on any of these?
```

### Asking "Why?"

Always ask the LLM to explain its reasoning:

```
You: Why are you so confident about HDFCBANK?

LLM: Let me break down the confidence score of 78% for HDFCBANK:

     Technical Factors (40% of score):
     - RSI at 27: Historically, when HDFCBANK drops to RSI < 30,
       it bounces back 82% of the time within 5 days
     - Price at support level: ₹1,580 has been strong support 3 times
       in past 6 months
     - Volume: 1.8x average, showing strong interest

     Fundamental Factors (30% of score):
     - Earnings beat expectations by 12%
     - Q3 guidance positive
     - Sector rotation into banking stocks happening now

     Sentiment Factors (30% of score):
     - News sentiment: +0.72 (very positive)
     - Analyst upgrades: 3 in past week
     - Social media mentions up 2.5x (bullish chatter)

     Historical Success Rate:
     When all these factors align, similar setups have:
     - Win rate: 78%
     - Average gain: +4.2%
     - Average time to target: 4 days

     Risk Factors to Watch:
     - Banking sector sensitive to RBI policy
     - Global markets looking weak
     - Stop loss is critical here

     The 78% confidence is based on this combination of factors
     aligning favorably. Not a guarantee, but strong probability.
```

### Getting Personalized Advice

The LLM learns your preferences:

```
You: I'm a conservative investor. Are these signals suitable for me?

LLM: Looking at your profile:
     - Risk tolerance: Conservative
     - Typical holding period: 2-3 weeks
     - Preferred sectors: Banking, IT
     - Max position size: 5% of portfolio

     Adjusting recommendations:

     ✅ KEEP: HDFCBANK
        - Banking sector (your preference)
        - Low volatility stock
        - Risk/reward 1:1.7 (acceptable)
        - Recommended position: 4% of portfolio

     ⚠️ MODIFY: INFY
        - IT sector (your preference) ✓
        - But higher volatility recently
        - Recommendation: Reduce position to 3% (instead of 5%)
        - Use tighter stop loss: ₹1,400 (instead of ₹1,390)

     ❌ SKIP: RELIANCE
        - Energy sector (not your preference)
        - Sell signals riskier for conservative investors
        - Better to wait for buy opportunities

     Conservative Strategy:
     - Take only the HDFCBANK position today
     - Wait for INFY to confirm trend (2 more days)
     - Skip RELIANCE entirely

     This approach:
     - Lowers overall risk
     - Matches your preferences
     - Still gives you market exposure

     Adjusted expected return: +2.8% (vs +4.2% for aggressive)
     Adjusted risk: -1.2% max loss (vs -2.2% for aggressive)
```

### Learning from PDFs

Upload research papers and the LLM learns from them:

```
You: I uploaded a PDF about momentum strategies. Read it and apply
     the concepts.

LLM: Reading "Advanced Momentum Strategies.pdf"...

     [Processing... 2 minutes]

     Key Insights Learned:

     1. Dual Momentum Strategy:
        - Combine absolute momentum (stock vs itself) with
          relative momentum (stock vs market)
        - Author found 15% better results than single momentum

     2. Volatility Adjustment:
        - Position size should be inverse to volatility
        - High volatility = smaller position
        - Reduces overall portfolio volatility

     3. Time-Series Filters:
        - Don't buy if 12-month return is negative
        - Even if short-term RSI looks good
        - Prevents "catching falling knives"

     Applying to MLTR:

     I've updated the signal generation to include:
     - ✅ Relative strength check vs Nifty 50
     - ✅ Volatility-adjusted position sizing
     - ✅ 12-month trend filter

     Regenerating signals with new rules...

     Updated signals now available. The momentum signals have
     improved confidence scores (+8% average) and better risk
     profiles. Would you like to see the new signals?
```

---

## Portfolio Monitoring with LLM

**NEW**: Use the LLM to monitor your actual portfolio and get personalized insights!

### Why Use LLM for Portfolio Monitoring?

The LLM is perfect for portfolio monitoring because it can:
- 📊 Analyze your actual holdings in plain English
- 🚨 Explain alerts in context of your situation
- 💡 Suggest actions based on your trading history
- 🤔 Answer "what if" questions about your portfolio

### Basic Portfolio Questions

**Check your holdings**:

```
You: What's in my portfolio right now?

LLM: Let me check your holdings...

     You currently hold 3 positions:

     1. RELIANCE - 100 shares @ avg ₹2,450
        Current: ₹2,520 (+2.9%, +₹7,000)
        Status: 🟢 Profitable, trending up

     2. TCS - 50 shares @ avg ₹3,200
        Current: ₹3,180 (-0.6%, -₹1,000)
        Status: 🟡 Small loss, watch closely

     3. INFY - 200 shares @ avg ₹1,445
        Current: ₹1,460 (+1.0%, +₹3,000)
        Status: 🟢 Profitable, stable

     Total Portfolio Value: ₹703,000
     Total P&L: +₹9,000 (+1.3%)
```

**Check specific position**:

```
You: How is my RELIANCE position doing?

LLM: Your RELIANCE position looks good:

     Purchase: 100 shares @ ₹2,450 (3 weeks ago)
     Current: ₹2,520
     P&L: +₹7,000 (+2.9%)

     Recent Performance:
     - Up 1.2% this week
     - Up 2.9% since purchase
     - Outperforming NIFTY50 (+0.8%)

     Technical Analysis:
     - RSI: 58 (neutral, room to grow)
     - MACD: Bullish crossover yesterday
     - Volume: Normal

     News Sentiment: Positive (+0.6)
     - New retail expansion announced
     - Strong quarterly results

     Recommendation: 🟢 HOLD
     No immediate concerns. Consider taking partial profits
     if it reaches ₹2,600 (target resistance).
```

### Emergency Alert Analysis

**Understanding alerts**:

```
You: I got an alert about TCS. What should I do?

LLM: Let me check the alert...

     🚨 ALERT DETAILS:
     Symbol: TCS
     Type: POSITION_LOSS
     Severity: HIGH
     Message: "TCS down 8.2% from your average price"

     YOUR SITUATION:
     - You bought TCS at ₹3,200
     - Current price: ₹2,940 (-8.1%)
     - Loss: ₹13,000 on 50 shares
     - This represents 22% of your portfolio

     WHAT HAPPENED:
     - TCS reported weak Q4 earnings (1 hour ago)
     - Revenue missed estimates by 3%
     - Stock gapped down at market open
     - High volume (2.5x normal) = panic selling

     ANALYSIS:
     - Your stop-loss (7%) was breached
     - Fundamentals still strong (this is temporary)
     - But short-term momentum is negative

     OPTIONS:
     1. 🚨 EXIT NOW: Cut losses at -8%, wait for clarity
     2. 🎯 HOLD & AVERAGE: Buy more if it drops to ₹2,850
     3. ⏰ WAIT: Set tight stop-loss at ₹2,900 (-9.4%)

     MY RECOMMENDATION: Option 1 (EXIT NOW)
     Reason: You're already past your stop-loss threshold.
     The risk of further downside (10-15%) is higher than
     the chance of quick recovery. Exit and reassess in a week.

     Would you like me to calculate the tax implications of
     selling now?
```

### Signal Execution Analysis

**Did you follow the AI's advice?**

```
You: Show me which signals I followed this month

LLM: Here's your signal execution analysis for November:

     📊 SIGNAL SUMMARY:
     Total signals: 18
     Followed: 13 (72.2%)
     Ignored: 5 (27.8%)

     FOLLOWED SIGNALS (13):
     ✅ Profitable: 9 (69.2%)
     ❌ Loss: 4 (30.8%)
     Average return: +3.1%

     Examples:
     1. RELIANCE BUY @ ₹2,450 → Result: +2.9% (holding)
     2. WIPRO BUY @ ₹415 → Result: +6.2% (sold @ ₹441)
     3. TATAMOTORS SELL @ ₹925 → Result: +4.1% (avoided drop)
     ...

     IGNORED SIGNALS (5):
     😊 Good ignores: 3 (avoided losses)
     😢 Missed opportunities: 2

     Missed opportunities:
     1. INFY BUY @ ₹1,445 → Went up 8.3% (you missed ₹24,030!)
     2. HDFC BUY @ ₹1,625 → Went up 4.2% (you missed ₹6,825!)

     💡 INSIGHTS:
     - You're good at filtering bad signals (60% of ignores were correct)
     - But you're also missing some good ones
     - Your execution rate (72%) is in the ideal range
     - Consider lowering confidence threshold from 0.7 to 0.65
       to catch more profitable signals

     Overall: You beat the AI by +0.8% with selective execution!
```

### Personalized Advice

**Ask for customized recommendations**:

```
You: Should I add more tech stocks to my portfolio?

LLM: Let me analyze your portfolio composition...

     CURRENT ALLOCATION:
     Tech (TCS, INFY): 64% (₹451,000)
     Energy (RELIANCE): 36% (₹252,000)

     ANALYSIS:
     ⚠️ CONCENTRATION RISK: You're heavily weighted in tech (64%)

     CONSIDERATIONS:
     1. Sector Risk: If tech sector corrects, you lose heavily
     2. Diversification: Ideal is <30% in any single sector
     3. Your Holdings: Both TCS and INFY are IT services
        (similar business models = correlated risk)

     RECOMMENDATION: ⚠️ DO NOT add more tech right now

     INSTEAD, CONSIDER:
     1. Reduce tech to 40-50% (sell some TCS or INFY)
     2. Add sectors:
        - Financials: HDFC Bank, ICICI Bank (stable)
        - Consumer: HUL, Asian Paints (defensive)
        - Pharma: Sun Pharma, Dr. Reddy's (diversifier)

     SUGGESTED TARGET:
     Tech: 40% (₹280k) - Reduce by ₹171k
     Energy: 25% (₹175k) - Reduce by ₹77k
     Financials: 20% (₹140k) - Add new
     Consumer: 10% (₹70k) - Add new
     Pharma: 5% (₹35k) - Add new

     This would give you better risk-adjusted returns while
     maintaining growth potential.

     Would you like me to suggest specific stocks for each sector?
```

### "What If" Scenarios

**Test scenarios before committing**:

```
You: What if I sell TCS and buy INFY instead?

LLM: Let me run that scenario...

     CURRENT SCENARIO:
     - TCS: 50 shares @ ₹3,180 = ₹159,000 (-₹1,000 loss)

     PROPOSED SCENARIO:
     - Sell TCS at ₹3,180 = ₹159,000 (minus ₹300 commission)
     - Buy INFY at ₹1,460 = 108 shares (₹158,700 after commission)

     COMPARISON (Based on 6-month backtest):

     | Metric          | Keep TCS | Switch to INFY |
     |-----------------|----------|----------------|
     | Expected Return | +8.2%    | +12.5%         |
     | Volatility      | 18%      | 22%            |
     | Sharpe Ratio    | 0.45     | 0.57           |
     | Max Drawdown    | -15%     | -19%           |

     RISK ANALYSIS:
     ✅ INFY has better growth potential (+4.3% higher return)
     ✅ Better risk-adjusted returns (Sharpe: 0.57 vs 0.45)
     ⚠️ Slightly higher volatility (4% more)
     ⚠️ You'll realize your TCS loss for taxes

     FUNDAMENTALS:
     TCS:
     - PE: 28.5 (slightly expensive)
     - Revenue growth: 9% YoY
     - Margin pressure from wage hikes

     INFY:
     - PE: 23.2 (more attractive)
     - Revenue growth: 12% YoY
     - Strong deal pipeline, better margins

     TAX IMPACT:
     - Short-term capital loss: ₹1,000
     - Can offset against gains this year
     - Tax saved: ~₹300 (assuming 30% bracket)

     MY RECOMMENDATION: ✅ SWITCH

     Reasons:
     1. Better growth prospects
     2. More attractive valuation
     3. Tax loss harvesting benefit
     4. Maintains tech exposure while upgrading position

     Timing: Consider executing during market dip (2-3% down day)
     to get better INFY entry price.
```

### Daily Portfolio Review

**Morning routine**:

```
You: Review my portfolio for today

LLM: Good morning! Here's your portfolio health check:

     📊 OVERNIGHT CHANGES:
     - RELIANCE: +0.8% (positive news on EV battery plant)
     - TCS: -0.3% (weak global IT spending forecast)
     - INFY: +1.2% (won major US banking deal)

     Portfolio value: ₹708,450 (+0.8% overnight)

     🚨 ALERTS:
     - No critical alerts
     - 1 notification: RELIANCE approaching resistance at ₹2,550

     📰 RELEVANT NEWS:
     1. IT sector: Weak demand from US banks (negative for TCS)
     2. Reliance: Announced EV battery gigafactory (positive)
     3. Market: NIFTY50 opened +0.5% (positive sentiment)

     💡 TODAY'S SIGNALS:
     1. HOLD RELIANCE (confidence: 82%)
        - Near resistance, wait for breakout confirmation
     2. WATCH TCS (confidence: 68%)
        - Weak sector sentiment, consider reducing if drops <₹3,150
     3. BUY MORE INFY (confidence: 76%)
        - Strong momentum, major deal win
        - Consider adding 50 shares if dips to ₹1,450

     🎯 ACTION ITEMS:
     1. Set alert for RELIANCE @ ₹2,550 (resistance)
     2. Set stop-loss for TCS @ ₹3,150 (-1% from current)
     3. Place limit order for INFY @ ₹1,450 (if it dips)

     Overall sentiment: 🟢 POSITIVE
     No immediate concerns. Your portfolio is well-positioned.

     Any questions about today's plan?
```

### Learning from Your Behavior

**LLM adapts to your style**:

```
You: Why do you keep suggesting high-risk trades? I'm conservative.

LLM: You're right - let me adjust to your risk profile.

     ANALYZING YOUR TRADING HISTORY:

     Past 3 months:
     - You followed 68% of signals
     - You NEVER followed signals with confidence <70%
     - You ignored all signals with potential loss >5%
     - You prefer stocks with:
       * PE ratio <25
       * Market cap >₹50,000 crore
       * Low volatility (beta <1.2)

     ADJUSTING RECOMMENDATIONS:

     Before (default settings):
     - Show all signals
     - Min confidence: 60%
     - Include high-growth, high-risk stocks

     After (customized for you):
     - Filter out signals with confidence <70%
     - Exclude stocks with volatility >25%
     - Focus on large-cap, stable companies
     - Max position size: 15% (conservative)
     - Emphasize value over growth

     UPDATED SIGNALS FOR YOU:
     1. HDFC Bank (conservative, stable) - BUY
     2. Asian Paints (low volatility) - BUY
     3. HUL (defensive) - HOLD

     (Previously suggested but now filtered out:)
     - ZOMATO (too volatile for your profile)
     - PAYTM (high-risk growth stock)
     - Small-cap tech stocks

     Your personalized model is now active!

     Note: Your returns may be lower than aggressive traders,
     but your risk is also much lower. That's okay!
```

### Configuration

Enable LLM portfolio monitoring in `configs/config.yaml`:

```yaml
llm:
  portfolio_monitoring:
    enabled: true

    # How often to generate portfolio summaries
    daily_review:
      enabled: true
      time: "08:30"  # Before market open

    # Alert integration
    alerts:
      explain_alerts: true  # LLM explains each alert
      suggest_actions: true  # LLM suggests what to do
      risk_analysis: true  # Analyze risk before suggesting

    # Personalization
    learn_from_behavior: true  # Adapt to your trading style
    confidence_threshold_adjust: true  # Adjust based on execution rate
    risk_profile: "moderate"  # conservative, moderate, aggressive

    # Advanced
    scenario_analysis: true  # Enable "what if" questions
    tax_optimization: true  # Consider tax implications
```

### Example Conversations

**Tax planning**:

```
You: I have ₹80,000 in short-term gains this year. How do I minimize taxes?

LLM: Let me help with tax-loss harvesting...

     YOUR SITUATION:
     - Short-term capital gains: ₹80,000
     - Tax rate: 15% (for stocks)
     - Tax liability: ₹12,000

     CURRENT LOSSES:
     - TCS: -₹1,000 (short-term, can offset)

     TAX SAVING OPPORTUNITY:
     If you exit TCS now:
     - Realized loss: ₹1,000
     - Taxable gains: ₹80,000 - ₹1,000 = ₹79,000
     - Tax saved: ₹150

     ADDITIONAL OPPORTUNITIES:
     Looking at your watchlist...

     Stocks you were considering anyway:
     - BAJAJFINSV: Currently -3% from your target entry
       You could buy now, sell in 2 days for small loss,
       then rebuy (wash sale harvesting)
       Potential loss: ₹5,000 → Tax saved: ₹750

     STRATEGY:
     1. Exit TCS (you wanted to anyway) = ₹150 saved
     2. Harvest ₹15,000 in losses before year-end = ₹2,250 saved
     3. Total tax savings: ₹2,400
     4. Net tax liability: ₹9,600 (down from ₹12,000)

     Note: Ensure 30-day gap before repurchasing same stocks
     to avoid wash sale issues.
```

**Risk management**:

```
You: My portfolio is down 12% today! Should I panic sell?

LLM: Stay calm. Let me analyze this...

     MARKET CONTEXT:
     - NIFTY50: -4.2% (broad market selloff)
     - Your portfolio: -12% (outperforming market by -7.8%)
     - Cause: Global tech selloff, not India-specific

     YOUR POSITIONS:
     - RELIANCE: -3% (less than market = defensive)
     - TCS: -18% (tech selloff, overbought correction)
     - INFY: -15% (tech selloff)

     HISTORICAL CONTEXT:
     Last 10 times NIFTY dropped >4% in a day:
     - 8 times (80%): Recovered within 1 week
     - 2 times (20%): Continued downtrend (2020 crash, 2022 war)

     CURRENT SITUATION:
     - No India-specific bad news
     - Corporate earnings are strong
     - This looks like temporary panic, not structural issue

     MY ANALYSIS: This is a BUYING OPPORTUNITY, not a sell signal

     🛑 DO NOT PANIC SELL

     RECOMMENDED ACTIONS:
     1. ✅ HOLD all positions (don't lock in losses)
     2. ✅ If you have cash, consider averaging down:
        - TCS at ₹3,000 would improve your avg cost
        - INFY at ₹1,400 is attractive
     3. ✅ Set stop-losses at -20% (protect against true crash)
     4. ⏰ Review tomorrow - if markets recover, you saved yourself

     HISTORICAL LESSON:
     March 2020: NIFTY dropped 30% in 2 weeks
     - Those who sold: Locked in 30% loss
     - Those who held: Recovered fully in 6 months
     - Those who bought: Made 60%+ in next year

     Your portfolio is quality stocks (TCS, INFY, RELIANCE).
     They will recover. Patience is key.

     Want me to send you calming statistics? 😊
```

### Key Takeaways

1. **Natural conversation**: Ask LLM anything about your portfolio
2. **Contextual alerts**: LLM explains alerts with full context
3. **Personalized advice**: Adapts to your risk tolerance and trading style
4. **Tax optimization**: Considers tax implications in recommendations
5. **Behavioral learning**: Gets smarter by watching what you actually do

**The LLM makes portfolio management feel like talking to a smart financial advisor!**

---

## Advanced Features

Once you're comfortable, try these advanced features.

### 1. Function Calling

The LLM can use tools automatically:

```
You: Compare the performance of momentum vs mean reversion strategies
     on INFY for the past year

LLM: To answer this, I'll need to:
     1. Run backtest for momentum strategy
     2. Run backtest for mean reversion strategy
     3. Compare the results

     [Executing: run_backtest(strategy='momentum', symbols=['INFY'], ...]
     [Executing: run_backtest(strategy='mean_reversion', symbols=['INFY'], ...]

     Results Comparison:

     Momentum Strategy:
     - Return: +18.2%
     - Sharpe: 1.32
     - Win rate: 68%
     - Max drawdown: -8.5%
     - Avg trade duration: 12 days

     Mean Reversion Strategy:
     - Return: +22.4%
     - Sharpe: 1.58
     - Win rate: 64%
     - Max drawdown: -6.2%
     - Avg trade duration: 5 days

     Winner: Mean Reversion (for INFY specifically)

     Analysis:
     INFY shows strong mean-reversion behavior. It tends to bounce
     back to its average price quickly. The momentum strategy worked,
     but mean reversion was more efficient with:
     - 4.2% higher returns
     - Lower drawdown
     - Faster trades (less time in market = less risk)

     Recommendation: For INFY, use mean reversion. For momentum
     stocks like RELIANCE, stick with momentum strategy.
```

The LLM automatically called two functions (`run_backtest`) and compared results!

### 2. Multi-Step Reasoning

Complex queries with multiple steps:

```
You: Find the 5 best stocks from NIFTY100 that are:
     - Oversold (RSI < 30)
     - Have positive news
     - Showed strong recovery in similar situations historically
     Then rank them by risk/reward ratio

LLM: Breaking this down into steps:

     Step 1: Filter NIFTY100 for RSI < 30
     [Filtering... found 12 stocks]

     Step 2: Check news sentiment
     [Analyzing... 7 stocks have positive sentiment]

     Step 3: Historical pattern analysis
     [Backtesting... 5 stocks show consistent recovery pattern]

     Step 4: Calculate risk/reward for each
     [Computing stop loss and targets...]

     Final Results (Ranked):

     1. HDFCBANK
        RSI: 27 | Sentiment: +0.75 | Risk/Reward: 1:2.3
        Historical recovery: 84% within 7 days

     2. MARUTI
        RSI: 28 | Sentiment: +0.62 | Risk/Reward: 1:2.1
        Historical recovery: 79% within 5 days

     3. DRREDDY
        RSI: 29 | Sentiment: +0.58 | Risk/Reward: 1:2.0
        Historical recovery: 76% within 8 days

     4. SUNPHARMA
        RSI: 29 | Sentiment: +0.54 | Risk/Reward: 1:1.9
        Historical recovery: 74% within 6 days

     5. TITAN
        RSI: 28 | Sentiment: +0.51 | Risk/Reward: 1:1.8
        Historical recovery: 71% within 7 days

     My pick: HDFCBANK
     Best combination of all factors. Would you like a detailed
     entry plan?
```

### 3. Continuous Learning

The LLM learns from your feedback:

```
You: Yesterday's INFY signal failed. It dropped 3% instead of going up.
     Why did that happen?

LLM: Let me analyze what went wrong with the INFY signal from Nov 2...

     Signal Details:
     - Entry: ₹1,420
     - Reason: RSI 31, positive sentiment
     - Expected: +3.9% gain
     - Actual: -3.0% loss

     Post-mortem Analysis:

     What We Missed:
     1. Sector Weakness:
        - IT sector was down 2.1% that day
        - We didn't weight sector trend heavily enough

     2. False News:
        - Positive sentiment was from analyst upgrade
        - But actual earnings report was mixed
        - Our sentiment model overweighted analyst opinions

     3. Volume Pattern:
        - Volume was high, but it was selling volume (not buying)
        - We only looked at total volume, not buy/sell ratio

     Lessons Learned:

     ✅ Added sector trend filter
        - Now checking if sector is strong before buying
        - Weight: 15% of decision

     ✅ Improved sentiment analysis
        - Differentiate analyst opinions vs actual news
        - Weight: Earnings reports 2x more than upgrades

     ✅ Added volume analysis
        - Check if volume is buying or selling pressure
        - Flag if volume is from distribution

     Updated Models:
     These improvements have been incorporated. The new model
     would have flagged INFY as "AVOID" on that day.

     I'm continuously learning from these mistakes. Keep providing
     feedback - it makes me smarter!
```

---

## Troubleshooting

### Issue 1: LLM Responds Slowly

**Symptoms**: Takes 10+ seconds to respond

**Causes & Solutions**:

**A) Using too large a model on CPU**:
```yaml
# Change from 14B to 7B or 3B
llm:
  model:
    model_name: "qwen2.5:3b"  # Smaller = faster
```

**B) Context too large**:
```yaml
llm:
  inference:
    n_ctx: 2048  # Reduce from 4096
```

**C) Not using GPU** (if you have one):
```yaml
llm:
  inference:
    n_gpu_layers: 35  # Use GPU layers
```

### Issue 2: LLM Gives Wrong Answers

**Symptoms**: Factually incorrect or nonsense responses

**Causes & Solutions**:

**A) Temperature too high** (too creative):
```yaml
llm:
  inference:
    temperature: 0.3  # Lower = more factual (was 0.7)
```

**B) Not enough context**:
```python
# Provide more context in your query
# Bad:
"Analyze INFY"

# Good:
"Analyze INFY with latest price data, news from past 3 days,
 and compare to its 50-day average"
```

**C) Model hallucinating**:
- Use smaller model (counterintuitively, sometimes more grounded)
- Ask for sources: "Explain with data to back it up"
- Verify numbers manually

### Issue 3: Out of Memory Error

**Symptoms**: `RuntimeError: out of memory`

**Solutions**:

**A) Use quantized model**:
```
# Instead of:
ollama pull qwen2.5:7b  # 7GB

# Use:
ollama pull qwen2.5:7b-q4  # 4GB (quantized)
```

**B) Reduce context window**:
```yaml
llm:
  inference:
    n_ctx: 1024  # Reduce from 4096
```

**C) Close other programs** before running

### Issue 4: LLM Won't Start

**Symptoms**: Error when trying to load model

**Check**:

1. **Is Ollama running?**
   ```bash
   ollama list  # Should show installed models
   ```

2. **Is model downloaded?**
   ```bash
   ollama pull qwen2.5:7b
   ```

3. **Check model path** (if using llama.cpp):
   ```bash
   ls models/llm/  # File should exist
   ```

4. **Check logs**:
   ```bash
   tail -f logs/llm.log
   ```

### Issue 5: LLM Can't Access Data

**Symptoms**: "I don't have access to that data"

**Solutions**:

**A) Give explicit permission**:
```yaml
llm:
  functions:
    enabled: true
    available_functions:
      - "fetch_data"
      - "run_backtest"
      - "generate_signals"
```

**B) Use correct function names**:
```
# Bad:
"Get me the data for RELIANCE"

# Good:
"Fetch OHLCV data for RELIANCE from the database"
```

---

## Tips for Best Results

### 1. Be Specific

**Vague**:
```
"Analyze the market"
```

**Specific**:
```
"Analyze NIFTY50 stocks with RSI < 35, positive news sentiment,
 and compare to their 3-month performance"
```

### 2. Ask for Reasoning

Always ask "why?":
```
You: Why did you suggest buying RELIANCE?

[LLM gives detailed reasoning with data]

You: Can you show me the historical data supporting that?

[LLM provides charts and statistics]
```

### 3. Verify Important Decisions

Never blindly trust. Verify:
```
You: You said INFY has RSI of 28. Can you show me the actual data?

LLM: Fetching latest data...

     INFY RSI (14-day):
     Nov 3: 28.2
     Nov 2: 32.1
     Nov 1: 35.6

     Source: data/processed/features/INFY.parquet
     Last updated: 2024-11-03 15:45 IST
```

### 4. Provide Feedback

Help it learn:
```
You: That signal was wrong. The price went down, not up.

[LLM analyzes what went wrong]

You: Good analysis. Remember to check sector trend next time.

LLM: Noted! I've updated my decision process to weight sector
     trends more heavily. This will affect future signals.
```

### 5. Start Simple, Then Complex

Build up gradually:
```
Day 1: "What is RSI?"
Day 2: "Show me stocks with low RSI"
Day 3: "Find oversold stocks with positive news"
Day 4: "Backtest buying oversold stocks with positive news"
Day 5: "Create an automated strategy from this"
```

---

## Next Steps

Now you have the AI brain working! Next:

1. **Practice**: Chat with the LLM daily, get comfortable
2. **Experiment**: Try different queries, see what works
3. **Integrate**: Use LLM to orchestrate your entire workflow
4. **Customize**: Fine-tune the LLM on your own trading data
5. **Advanced**: Set up automated trading with LLM oversight

**Remember**:
- LLM is a tool, not a magic oracle
- Always verify its suggestions
- Combine LLM insights with your own judgment
- Keep learning and improving together!

---

## Comparison: With vs Without LLM

### Without LLM (Traditional)

```
1. Open terminal
2. Type: python scripts/fetch_data.py --symbols RELIANCE --days 30
3. Type: python scripts/compute_features.py --symbols RELIANCE
4. Type: python scripts/generate_signals.py --confidence 0.6
5. Open dashboard
6. Find RELIANCE signal
7. Read technical indicators
8. Try to understand if it's good
9. Make decision
Time: 15 minutes
```

### With LLM (Natural Language)

```
You: "Should I buy RELIANCE today?"

[2 seconds later]

LLM: "Based on current data:
     - RSI: 28 (oversold, good)
     - News: Positive (+0.7)
     - Historical: 76% success rate
     - Confidence: 73%

     Yes, RELIANCE looks like a good buy.
     Entry: ₹2,450, Target: ₹2,540, Stop: ₹2,400

     Want detailed analysis?"

Time: 10 seconds
```

**150x faster! Plus:**
- No coding needed
- Explained in plain English
- Can ask follow-up questions
- Learns from your preferences

---

**Congratulations!** You now have a fully functional AI assistant for trading! 🎉

You've completed all the guides:
- ✅ BEGINNER_GUIDE.md - Setup and basics
- ✅ ML_EXPLAINED.md - Understanding machine learning
- ✅ LLM_SETUP_GUIDE.md - AI brain setup

**You're ready to start trading with AI!** 🚀
