# Machine Learning Explained
## How MLTR Learns to Trade (For Non-Technical People)

**Welcome!** This guide explains how the machine learning part of MLTR works, using simple analogies and real examples.

---

## 📚 Table of Contents

1. [What is Machine Learning?](#what-is-machine-learning)
2. [How MLTR Learns](#how-mltr-learns)
3. [The Learning Process](#the-learning-process)
4. [Types of Models We Use](#types-of-models-we-use)
5. [Training Your First Model](#training-your-first-model)
6. [Understanding Model Performance](#understanding-model-performance)
7. [When to Retrain](#when-to-retrain)
8. [Common Mistakes to Avoid](#common-mistakes-to-avoid)

---

## What is Machine Learning?

### The Simple Explanation

**Machine Learning** is teaching a computer to find patterns by showing it examples, instead of programming every rule manually.

###

 Analogy: Learning to Recognize a Cat

**Traditional Programming** (writing rules):
```
IF has_whiskers AND has_tail AND says_meow:
    it's a cat
```
Problem: What about cats without tails? Cats that don't meow? This gets complicated fast!

**Machine Learning** (learning from examples):
```
Show the computer 10,000 cat pictures
Show the computer 10,000 dog pictures
Computer learns: "Cats tend to have these features..."
Now show it a new picture → it recognizes it's a cat!
```

### Applied to Stock Trading

**Traditional Programming**:
```
IF RSI < 30 AND MACD_crosses_up:
    buy_signal = True
```
Problem: Markets are complex! One rule doesn't work for all stocks, all times.

**Machine Learning**:
```
Show the system 10,000 past trading days
System learns: "When RSI is low AND news is positive AND volume spikes,
               price goes up 72% of the time"
```

---

## How MLTR Learns

Let's break down exactly how MLTR learns to trade.

### Step 1: Collect Historical Data

We gather past information:

```
Date: 2024-01-15
Stock: RELIANCE
- Price: ₹2,400
- RSI: 28
- MACD: Crossed up yesterday
- News sentiment: +0.6 (positive)
- Volume: 2x normal

What happened next?
- 5 days later: Price = ₹2,480 (up 3.3%)
- Result: ✅ Good buy opportunity!
```

We collect 1000s of these examples.

### Step 2: Extract Features

We calculate useful statistics (features):

| Date | Stock | RSI | MACD | Sentiment | Volume | Result |
|------|-------|-----|------|-----------|---------|--------|
| 2024-01-15 | RELIANCE | 28 | +cross | +0.6 | 2x | +3.3% ✅ |
| 2024-01-22 | TCS | 72 | -cross | -0.2 | 1.5x | -2.1% ❌ |
| 2024-02-03 | INFY | 45 | flat | +0.8 | 0.8x | +1.2% ✅ |
| ... | ... | ... | ... | ... | ... | ... |

Each row is one "example" the system learns from.

### Step 3: Find Patterns

The machine learning model looks for patterns:

**Pattern 1**: "When RSI < 30 AND sentiment > 0.5, price went up 75% of the time"
**Pattern 2**: "When RSI > 70 AND volume > 1.5x, price went down 68% of the time"
**Pattern 3**: "When MACD crosses up AND news positive, price went up 72% of the time"

It finds hundreds of these patterns automatically!

### Step 4: Make Predictions

When you ask for today's signals:

```
Today: RELIANCE
- RSI: 27 (matches Pattern 1)
- Sentiment: +0.65 (matches Pattern 1)
- MACD: Just crossed up (matches Pattern 3)

Model thinks:
- Pattern 1 suggests: 75% chance of going up
- Pattern 3 suggests: 72% chance of going up
- Combined confidence: 73%

→ Generate BUY signal with 73% confidence
```

---

## The Learning Process

Let's walk through training a model step-by-step.

### Analogy: Teaching a Child Math

1. **Show examples**:
   - "2 + 2 = 4"
   - "3 + 5 = 8"
   - "1 + 7 = 8"

2. **Child learns pattern**: "Add the two numbers together"

3. **Test understanding**:
   - You: "What's 6 + 3?"
   - Child: "9!"
   - ✅ Correct!

4. **Keep practicing** with more examples to get better

### Applied to Stock Trading

1. **Show examples** (Training Data):
   ```
   Example 1: RSI=28, Sentiment=+0.7 → Price went UP
   Example 2: RSI=75, Sentiment=-0.3 → Price went DOWN
   Example 3: RSI=32, Sentiment=+0.5 → Price went UP
   ... (show 10,000 examples)
   ```

2. **Model learns patterns**:
   - "Low RSI + positive sentiment usually means price goes up"
   - "High RSI + negative sentiment usually means price goes down"

3. **Test understanding** (Testing Data):
   ```
   Test: RSI=29, Sentiment=+0.6 → What will happen?
   Model predicts: UP
   Reality: Price went up 2.5%
   ✅ Correct!
   ```

4. **Measure accuracy**:
   - Tested on 1000 new examples
   - Got 720 correct
   - Accuracy: 72%

### The Actual Process in MLTR

#### Phase 1: Data Preparation (5 minutes)

```bash
python scripts/prepare_training_data.py
```

What happens:
```
Loading historical data...
✓ Loaded 50 stocks × 2 years = 25,000 days of data

Computing features...
✓ RSI, MACD, Bollinger Bands, Sentiment
✓ Total: 30 features per stock per day

Creating labels (what to predict)...
✓ "Will price go up 2%+ in next 5 days?" → YES/NO
✓ Generated 25,000 training examples

Splitting data...
✓ Training set: 20,000 examples (80%)
✓ Testing set: 5,000 examples (20%)

Ready to train!
```

#### Phase 2: Model Training (20 minutes)

```bash
python scripts/train_models.py
```

What happens:
```
Training Random Forest model...
Epoch 1/10: Looking at 20,000 examples...
Epoch 2/10: Adjusting patterns...
Epoch 3/10: Getting better...
...
Epoch 10/10: Done!

Training complete!
Accuracy on training data: 78%
Accuracy on testing data: 72%

Model saved to: data/models/random_forest_v1.pkl
```

**Why 72% accuracy is good**:
- Random guessing: 50% (coin flip)
- Simple rules (RSI only): 55-60%
- Our ML model: 72%
- That 12% improvement = significant edge!

#### Phase 3: Validation (5 minutes)

We double-check the model isn't "cheating":

```bash
python scripts/validate_model.py
```

```
Backtesting on unseen data (2023)...

Results:
- Total trades: 156
- Wins: 112 (72%)
- Average profit: +2.8%
- Average loss: -1.5%
- Overall return: +24%

✓ Model performs well on new data!
✓ No overfitting detected
✓ Ready for production
```

---

## Types of Models We Use

MLTR uses several types of machine learning models. Here's what they do:

### 1. Random Forest (Primary Model)

**What it is**: A team of decision trees that vote on the answer.

**Analogy**:
- You ask 100 doctors "Is this patient sick?"
- 72 say "Yes", 28 say "No"
- You go with the majority: "Yes, probably sick"

**In trading**:
- Create 100 "decision trees"
- Each tree looks at different features
- They vote: "72 trees say buy, 28 say don't buy"
- → 72% confidence BUY signal

**Why we use it**:
- Very reliable
- Hard to fool (needs many trees to agree)
- Works well with messy data

**Example output**:
```
Random Forest Prediction:
- Trees voting BUY: 72/100
- Confidence: 72%
- Most important feature: RSI (35% weight)
- 2nd most important: Sentiment (25% weight)
```

### 2. XGBoost (Advanced Model)

**What it is**: A smarter version of Random Forest that learns from mistakes.

**Analogy**:
- First tree makes predictions, gets some wrong
- Second tree focuses on the mistakes: "Let me fix those errors"
- Third tree fixes the remaining errors
- Repeat 100 times → very accurate!

**In trading**:
- Starts with simple patterns
- Each iteration learns more complex patterns
- Final model is combination of all learnings

**Why we use it**:
- Usually 2-5% more accurate than Random Forest
- Great for finding subtle patterns
- Industry standard for competitions

**When we use it**:
- When we have lots of data (2+ years)
- For monthly retraining
- When accuracy is critical

### 3. River (Online Learning)

**What it is**: A model that learns continuously, not just in batches.

**Analogy**:
- Traditional: Study for exam once, then take test
- Online: Learn a little bit every single day

**In trading**:
- Learns from each new day of data immediately
- Adapts to changing market conditions quickly
- Never "outdated" because it's always learning

**Why we use it**:
- For intraday trading (during market hours)
- When markets are volatile (patterns change fast)
- As a complement to main models

**Example**:
```
9:30 AM: Model makes prediction
3:30 PM: Market closes, check if prediction was right
3:31 PM: Model updates itself based on result
Next day: Model is slightly smarter
```

### Which Model to Use?

We use ALL of them together (ensemble):

```
Final Prediction =
    40% Random Forest +
    40% XGBoost +
    20% River

Example:
- Random Forest says: 75% BUY
- XGBoost says: 78% BUY
- River says: 68% BUY

Final: (0.40×75) + (0.40×78) + (0.20×68) = 74.8% BUY
```

This is more reliable than any single model!

---

## Training Your First Model

Let's actually train a model step-by-step.

### Step 1: Prepare Your Data

First, make sure you have enough data:

```bash
# Check how much data you have
python -c "
import pandas as pd
df = pd.read_parquet('data/processed/ohlcv')
print(f'Total days: {len(df)}')
print(f'Total stocks: {df[\"symbol\"].nunique()}')
"
```

You should see:
```
Total days: 25,000
Total stocks: 50
```

**Minimum requirements**:
- At least 1 year of data (365 days)
- At least 10 stocks
- More is better!

### Step 2: Choose Your Target

**What are we trying to predict?**

Option 1: **Binary** (Simple - Yes/No)
```yaml
# In config.yaml
ml:
  targets:
    binary:
      forward_days: 5  # Predict 5 days ahead
      threshold_pct: 2.0  # Did price go up 2%+?
```

Option 2: **Regression** (Advanced - exact number)
```yaml
ml:
  targets:
    regression:
      forward_days: 5  # Predict exact return in 5 days
```

**For beginners**: Use Binary! It's simpler and more reliable.

### Step 3: Train the Model

```bash
python scripts/train_models.py --config configs/config.yaml
```

**What you'll see** (takes 20-30 minutes):

```
=== MLTR Model Training ===

Step 1/5: Loading data...
✓ Loaded 25,000 examples

Step 2/5: Computing features...
✓ RSI, MACD, Bollinger, ADX, OBV
✓ Sentiment, news volume
✓ Total: 35 features

Step 3/5: Creating labels...
✓ Forward return: 5 days
✓ Threshold: 2%
✓ Positive examples: 12,500 (50%)
✓ Negative examples: 12,500 (50%)

Step 4/5: Training models...

Random Forest:
[████████████████████] 100% | Accuracy: 73.2%

XGBoost:
[████████████████████] 100% | Accuracy: 75.8%

Step 5/5: Evaluating...

Performance on test set:
- Random Forest: 72.5%
- XGBoost: 74.3%
- Ensemble: 74.8%

Confusion Matrix:
                 Predicted UP | Predicted DOWN
Actually UP      1,850        | 700
Actually DOWN    550          | 1,900

✓ Training complete!
✓ Models saved to: data/models/
```

### Step 4: Understand the Results

Let's break down those numbers:

**Accuracy: 74.8%**
- Out of 5,000 test cases, got 3,750 right
- That's pretty good! (Random would be 50%)

**Confusion Matrix**:
```
True Positives (1,850): Said UP, and it DID go up ✅
False Negatives (700): Said DOWN, but it went UP ❌
False Positives (550): Said UP, but it went DOWN ❌
True Negatives (1,900): Said DOWN, and it DID go down ✅
```

**What this means**:
- When model says "BUY", it's right 77% of the time (1,850 / 2,400)
- When model says "SELL", it's right 73% of the time (1,900 / 2,600)
- It's better at identifying good buys than avoiding bad ones

### Step 5: Test It Live (Paper Trading)

Before using real money, test with paper trading:

```bash
python scripts/paper_trade.py --days 30
```

This simulates trading for 30 days using only data from the past.

```
Day 1: Generated 3 signals, took 2 trades
Day 2: 1 win (+2.5%), 1 loss (-0.8%)
...
Day 30: Results

Total trades: 45
Wins: 33 (73%)
Average win: +2.8%
Average loss: -1.2%
Total return: +12.5%
Max drawdown: -3.2%

Sharpe ratio: 1.42 (good!)
```

If you see decent results (>60% win rate, positive return), you're ready!

---

## Understanding Model Performance

How do we know if a model is good? Let's explore key metrics.

### 1. Accuracy

**What it is**: Percentage of predictions that were correct.

```
Accuracy = Correct Predictions / Total Predictions

Example: 720 correct out of 1000 = 72%
```

**Interpretation**:
- < 55%: Bad, might as well flip a coin
- 55-65%: Okay, slight edge
- 65-75%: Good, meaningful advantage
- > 75%: Excellent (but be careful - might be overfitting!)

### 2. Precision

**What it is**: When model says "BUY", how often is it right?

```
Precision = True Positives / (True Positives + False Positives)

Example: Said BUY 1000 times, 750 were good = 75% precision
```

**Why it matters**: High precision = you're not wasting money on bad trades.

### 3. Recall

**What it is**: Of all the good opportunities, how many did we catch?

```
Recall = True Positives / (True Positives + False Negatives)

Example: 1000 good opportunities, caught 800 = 80% recall
```

**Why it matters**: High recall = you're not missing good trades.

### 4. Sharpe Ratio

**What it is**: How much return you get per unit of risk.

```
Sharpe = (Average Return - Risk Free Rate) / Standard Deviation

Example: 18% return, 12% volatility, 6% risk-free rate
Sharpe = (18% - 6%) / 12% = 1.0
```

**Interpretation**:
- < 1.0: Not great (high risk for the return)
- 1.0-2.0: Good (reasonable risk/reward)
- > 2.0: Excellent (high return for low risk)

### 5. Maximum Drawdown

**What it is**: The worst losing streak (peak to trough).

```
Example:
Portfolio value: ₹100,000 → ₹95,000 → ₹92,000 → ₹98,000
Max drawdown: -8% (from ₹100k to ₹92k)
```

**Why it matters**: Shows worst-case scenario. Can you stomach a 20% drawdown?

### Real Example

Let's evaluate our model:

```python
python scripts/evaluate_model.py

=== Model Evaluation ===

Accuracy: 72.5%
Precision: 75.2%
Recall: 70.1%

Backtest Results (2023):
Total Return: +24.3%
Sharpe Ratio: 1.45
Max Drawdown: -8.2%
Win Rate: 72%

Benchmark (Buy & Hold):
Total Return: +15.2%
Max Drawdown: -12.5%

✓ Model outperforms benchmark!
✓ Lower drawdown than buy & hold
✓ Sharpe ratio is healthy
```

This is a good model!

---

## When to Retrain

Models don't stay good forever. Markets change!

### Signs You Need to Retrain

1. **Performance Degrading**:
   ```
   Month 1: 75% accuracy
   Month 2: 73% accuracy
   Month 3: 68% accuracy  ← Time to retrain!
   ```

2. **Market Regime Changed**:
   - Bull market → Bear market
   - Low volatility → High volatility
   - Old patterns don't work anymore

3. **New Data Available**:
   - Every month, you have 20 more trading days
   - Model can learn from this new data

4. **Added New Features**:
   - Added sentiment analysis
   - Added volume profile
   - Model needs to learn how to use them

### Retraining Schedule

**Recommended**:
- **Monthly**: Light retrain (quick, 10 minutes)
- **Quarterly**: Full retrain (thorough, 1 hour)
- **Ad-hoc**: When performance drops

**How to retrain**:

```bash
# Monthly (incremental)
python scripts/train_models.py --incremental

# Quarterly (from scratch)
python scripts/train_models.py --full
```

### Before vs After Retraining

Before (old model):
```
Test Period: October 2024
Accuracy: 68%
Return: +2.1%
Sharpe: 0.85
```

After (retrained):
```
Test Period: October 2024
Accuracy: 73%
Return: +5.3%
Sharpe: 1.35

✓ Improvement: +5% accuracy, +3.2% return
```

---

## Common Mistakes to Avoid

### Mistake 1: Overfitting

**What it is**: Model memorizes training data instead of learning patterns.

**Analogy**:
- Student memorizes specific exam questions
- Can ace that exact exam
- But fails on different questions (can't generalize)

**In trading**:
```
Model learns: "On Jan 15, 2023, when RELIANCE was ₹2,450, it went up"
This is useless! We need general patterns, not specific dates.
```

**How to avoid**:
- Use walk-forward validation
- Test on completely new data
- Keep models simple (don't use 500 features)
- Regularization (technical term for "don't memorize")

**Signs of overfitting**:
```
Training accuracy: 95%  ← Suspiciously high!
Testing accuracy: 62%   ← Performs poorly on new data
```

### Mistake 2: Look-Ahead Bias

**What it is**: Using future information that wouldn't be available at prediction time.

**Example of cheating** (accidentally):
```python
# BAD: Using news from 5 days in future
df['future_sentiment'] = df['sentiment'].shift(-5)  # CHEATING!
model.train(features=['future_sentiment'])
# Of course it works! You're peeking into the future!
```

**How to avoid**:
- Only use data available BEFORE the prediction time
- Our system prevents this automatically
- Run tests to verify (we have 20+ tests for this!)

### Mistake 3: Not Enough Data

**What it is**: Training on too little data.

**Problem**:
```
Data: 30 days (6 weeks)
Model learns: "Stocks go up!" (because market was bullish those 6 weeks)
Reality: Market crashes next month
Model fails spectacularly
```

**Minimum requirements**:
- 1 year of data (okay)
- 2 years of data (good)
- 3+ years of data (better)
- Must include different market conditions!

### Mistake 4: Not Testing Properly

**What it is**: Testing on data the model already saw.

**Problem**:
```python
# BAD: Test on training data
model.train(data_2023)
accuracy = model.test(data_2023)  # Cheating!
# Accuracy will be inflated!
```

**How to do it right**:
```python
# GOOD: Split data properly
train_data = data_2022_2023  # Train on 2022-2023
test_data = data_2024        # Test on 2024 (future)
model.train(train_data)
accuracy = model.test(test_data)
```

### Mistake 5: Ignoring Transaction Costs

**What it is**: Forgetting that trading has costs.

**Example**:
```
Model predicts: +1.5% profit
Reality:
- Entry: 0.05% brokerage
- Exit: 0.05% brokerage
- Slippage: 0.1%
- Total costs: 0.2%
- Actual profit: 1.5% - 0.2% = 1.3%
```

After 100 trades: Costs = 20% of returns!

**How to account**:
```python
# Our backtests include costs automatically
backtest_config:
  commission: 0.05%
  slippage: 0.1%
```

---

## Quiz: Test Your Understanding

Try to answer these questions:

1. **What's a better model?**
   - A) 95% accuracy on training, 60% on testing
   - B) 72% accuracy on training, 70% on testing

   Answer: B! Model A is overfitting.

2. **Why do we split data into train/test?**
   - A) To save disk space
   - B) To verify model works on new data
   - C) Because it's tradition

   Answer: B! We need to test on unseen data.

3. **When should you retrain?**
   - A) Every day
   - B) Never, one training is enough
   - C) Monthly or when performance drops

   Answer: C! Balance between keeping fresh and avoiding overtraining.

4. **What's a good Sharpe ratio?**
   - A) 0.5
   - B) 1.5
   - C) 5.0

   Answer: B! 1.0-2.0 is good range for trading.

5. **What's look-ahead bias?**
   - A) Looking at your screen a lot
   - B) Using future data in predictions
   - C) Predicting too far ahead

   Answer: B! Using data that wouldn't be available at prediction time.

---

## Next Steps

Now you understand how ML works! Next:

1. **Try training your first model**: Follow the steps in this guide
2. **Read**: [LLM_SETUP_GUIDE.md](LLM_SETUP_GUIDE.md) - Set up the AI brain
3. **Experiment**: Try different features and see what improves performance
4. **Monitor**: Track your model's performance over time
5. **Learn**: Take an online ML course (free on Coursera/YouTube)

**Remember**:
- ML is a tool, not magic
- It gives you an edge, not guaranteed profits
- Always combine ML with your own judgment
- Keep learning and improving!

---

## Glossary

| Term | Simple Definition |
|------|-------------------|
| **Training** | Teaching the model by showing it examples |
| **Testing** | Checking if the model learned correctly using new data |
| **Features** | The inputs to the model (RSI, MACD, sentiment, etc.) |
| **Labels** | What we're trying to predict (price going up/down) |
| **Overfitting** | Model memorizes instead of learning patterns |
| **Accuracy** | Percentage of correct predictions |
| **Precision** | Of predictions saying "BUY", how many were right |
| **Recall** | Of all good opportunities, how many we caught |
| **Ensemble** | Combining multiple models for better results |
| **Backtest** | Testing strategy on historical data |
| **Walk-Forward** | Training on past, testing on future (proper way) |

---

**You did it!** You now understand machine learning for trading! 🎉

Continue to: [LLM_SETUP_GUIDE.md](LLM_SETUP_GUIDE.md) to set up the AI brain that explains everything in plain English!
