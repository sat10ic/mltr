# Portfolio Management Module

Track your actual trades, monitor holdings, and get emergency alerts for portfolio protection.

## Overview

This module helps you:

1. **Track Signal Execution**: Did you actually follow the buy/sell signals?
2. **Monitor Holdings**: What's in your portfolio right now?
3. **Emergency Alerts**: Get warnings when stocks fall rapidly
4. **ML Feedback**: Help the AI learn from your actual results
5. **Broker Sync**: Automatically import from Zerodha, Upstox, etc.

## Quick Start

### 1. Track Your Portfolio

```python
from src.portfolio import PortfolioTracker

# Create tracker
tracker = PortfolioTracker(db_path="data/portfolio.db")

# Record a signal from the ML system
signal_id = tracker.record_signal(
    symbol="RELIANCE",
    signal_type="BUY",
    price=2450.50,
    timestamp=datetime.now(),
    confidence=0.85
)

# Record your actual trade (when you execute it)
tracker.record_trade(
    symbol="RELIANCE",
    trade_type="BUY",
    price=2451.00,  # Actual execution price
    quantity=100,
    timestamp=datetime.now(),
    signal_id=signal_id  # Link to signal
)

# Check what you're holding
holdings = tracker.get_current_holdings()
print(holdings)
```

### 2. Get Emergency Alerts

```python
from src.portfolio import EmergencyAlertSystem

# Create alert system
alerts = EmergencyAlertSystem()

# Check a position for problems
alert = alerts.check_position(
    symbol="RELIANCE",
    current_price=2300,  # Stock fell
    avg_price=2500,       # Your purchase price
    quantity=100,
    day_open=2480
)

if alert:
    print(f"🚨 ALERT: {alert['message']}")
    print(f"Action: {alert['action']}")
```

Output:
```
🚨 ALERT: RELIANCE down 8.0% from your average price!
Action: Consider reviewing stop-loss. Current loss: ₹20,000
```

### 3. Sync with Your Broker

```python
from src.portfolio import BrokerSync

# Connect to Zerodha
sync = BrokerSync(
    broker="zerodha",
    api_key="your_api_key",
    access_token="your_access_token"
)

# Fetch current holdings
holdings = sync.fetch_holdings()

# Fetch recent trades
trades = sync.fetch_trades(days=7)

# Sync to tracker
sync.sync_to_tracker(tracker)
```

## Features

### 1. Portfolio Tracker

**What it does**: Keeps track of what you actually own and whether you followed the signals.

**Key Features**:
- Stores all generated signals
- Records all executed trades
- Calculates execution rate (how often you follow signals)
- Provides feedback to ML models
- Tracks performance of followed vs. ignored signals

**Example Use Case**:
```python
# Get execution rate
rate = tracker.get_execution_rate(days=30)
print(f"You followed {rate*100:.1f}% of signals in the last 30 days")

# Analyze signal performance
performance = tracker.get_signal_performance()
print(performance.head())
```

### 2. Emergency Alert System

**What it does**: Monitors your positions and alerts you when something dangerous is happening.

**Alert Types**:

| Alert Type | Trigger | Severity |
|------------|---------|----------|
| **POSITION_LOSS** | Position down >10% | HIGH |
| **INTRADAY_DROP** | Stock down >5% today | CRITICAL |
| **STOP_LOSS_HIT** | Price hits stop-loss | CRITICAL |
| **VOLUME_SPIKE** | Volume >3x average | MEDIUM |
| **CIRCUIT_LIMIT** | Approaching circuit limit | CRITICAL |
| **PORTFOLIO_DRAWDOWN** | Portfolio down >15% | HIGH |
| **CONCENTRATION_RISK** | Single stock >30% | MEDIUM |
| **MULTIPLE_LOSSES** | >70% positions losing | HIGH |

**Example**:
```python
# Check entire portfolio
import pandas as pd

positions = pd.DataFrame({
    "symbol": ["RELIANCE", "TCS", "INFY"],
    "quantity": [100, 50, 200],
    "avg_price": [2500, 3200, 1450]
})

market_data = pd.DataFrame({
    "symbol": ["RELIANCE", "TCS", "INFY"],
    "close": [2300, 3150, 1420],  # Current prices
    "open": [2480, 3200, 1445],
    "volume": [5000000, 2000000, 8000000]
})

all_alerts = alerts.check_portfolio(positions, market_data)

for alert in all_alerts:
    print(alerts.format_alert_message(alert))
```

### 3. Broker Sync

**What it does**: Automatically imports your holdings and trades from your broker.

**Supported Brokers**:
- ✅ Zerodha (Kite Connect)
- ✅ Upstox
- ✅ Angel Broking
- ✅ CSV Import (any broker)
- 🔄 More coming soon

**Setup Instructions**:

#### Zerodha Setup

1. Go to https://kite.trade/
2. Create a developer account
3. Create a new app
4. Get your API Key and Secret
5. Generate access token

```python
from src.portfolio import setup_zerodha_auth

# Interactive setup
auth = setup_zerodha_auth()

# Use the credentials
sync = BrokerSync(
    broker="zerodha",
    api_key=auth["api_key"],
    access_token=auth["access_token"]
)
```

#### CSV Import (Any Broker)

If your broker isn't supported, export holdings and trades to CSV:

**Holdings CSV format**:
```csv
symbol,quantity,avg_price
RELIANCE,100,2450.50
TCS,50,3200.00
INFY,200,1445.00
```

**Trades CSV format**:
```csv
symbol,trade_type,quantity,price,trade_time
RELIANCE,BUY,100,2450.50,2025-01-01 09:30:00
TCS,SELL,25,3200.00,2025-01-02 14:15:00
```

```python
# Import CSV
holdings = sync.import_holdings_csv("my_holdings.csv")
trades = sync.import_trades_csv("my_trades.csv")
```

## Integration with ML System

The portfolio module provides feedback to help the ML models learn from your actual results.

### How It Works

1. **Signal Generated**: ML system predicts "BUY RELIANCE at 2450"
2. **You Execute**: You buy RELIANCE at 2451 (close to signal)
3. **Outcome Tracking**: System monitors the trade outcome
4. **Feedback to ML**: Result fed back to model for improvement

```python
# Generate ML feedback for a signal
feedback = tracker.generate_ml_feedback(
    symbol="RELIANCE",
    signal_id=signal_id
)

print(feedback)
```

Example output:
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

### Feedback Types

| Outcome | Meaning | ML Action |
|---------|---------|-----------|
| **PROFIT** | Signal was good, you followed it, made money | Reinforce these features |
| **LOSS** | Signal was bad, you followed it, lost money | Reduce weight on these features |
| **MISSED_PROFIT** | Signal was good, you didn't follow it | Increase confidence thresholds |
| **AVOIDED_LOSS** | Signal was bad, you didn't follow it | Model needs retraining |

## Configuration

Add to `configs/config.yaml`:

```yaml
portfolio:
  # Database for tracking
  db_path: "data/portfolio.db"

  # Broker sync
  broker: "zerodha"  # or "upstox", "angelbroking", "csv"
  sync_frequency: "daily"  # How often to sync

  # Emergency alerts
  alerts:
    enabled: true

    # Thresholds
    intraday_drop_pct: 5.0      # Alert if >5% drop today
    position_loss_pct: 10.0     # Alert if position down >10%
    portfolio_drawdown_pct: 15.0  # Alert if portfolio down >15%
    stop_loss_pct: 7.0          # Default stop-loss level
    volume_spike_multiplier: 3.0  # Alert if volume >3x average

    # Notification channels
    notifications:
      - console  # Print to terminal
      - email    # Send email
      - telegram # Telegram bot (optional)

  # ML feedback
  feedback:
    enabled: true
    lookback_days: 30  # How far back to analyze
    min_confidence: 0.6  # Only give feedback on high-confidence signals
```

## Command-Line Interface

```bash
# Check portfolio status
python -m src.cli portfolio status

# Check for alerts
python -m src.cli portfolio alerts

# Sync with broker
python -m src.cli portfolio sync --broker zerodha

# Import from CSV
python -m src.cli portfolio import --holdings holdings.csv --trades trades.csv

# Analyze execution rate
python -m src.cli portfolio execution-rate --days 30

# Generate ML feedback
python -m src.cli portfolio feedback --days 7
```

## Dashboard Integration

The portfolio tracker is integrated into the main Streamlit dashboard:

```python
import streamlit as st
from src.portfolio import PortfolioTracker, EmergencyAlertSystem

tracker = PortfolioTracker()
alerts = EmergencyAlertSystem()

# Portfolio page
st.title("📊 My Portfolio")

# Current holdings
st.subheader("Current Holdings")
holdings = tracker.get_current_holdings()
st.dataframe(holdings)

# Emergency alerts
st.subheader("🚨 Active Alerts")
active_alerts = alerts.get_recent_alerts(hours=24)
for alert in active_alerts:
    st.warning(alerts.format_alert_message(alert))

# Execution rate
st.subheader("Signal Execution")
rate = tracker.get_execution_rate(days=30)
st.metric("Execution Rate (30 days)", f"{rate*100:.1f}%")

# Performance comparison
st.subheader("Followed vs. Ignored Signals")
performance = tracker.get_signal_performance()
st.dataframe(performance)
```

## Advanced Usage

### Custom Stop-Loss Strategies

```python
# ATR-based stop-loss
def calculate_atr_stop_loss(symbol, atr_multiplier=2.0):
    """Calculate stop-loss based on ATR."""
    from src.features.technical import calculate_atr

    atr = calculate_atr(symbol, period=14)
    current_price = get_current_price(symbol)

    stop_loss = current_price - (atr * atr_multiplier)
    return stop_loss

# Use in alert system
alerts.config["stop_loss_calculator"] = calculate_atr_stop_loss
```

### Portfolio Rebalancing

```python
def suggest_rebalancing(holdings, target_weights):
    """Suggest trades to reach target portfolio weights."""

    total_value = holdings["market_value"].sum()

    suggestions = []
    for symbol, target_weight in target_weights.items():
        current_value = holdings[holdings["symbol"] == symbol]["market_value"].sum()
        current_weight = current_value / total_value

        if abs(current_weight - target_weight) > 0.05:  # >5% deviation
            target_value = total_value * target_weight
            adjustment = target_value - current_value

            suggestions.append({
                "symbol": symbol,
                "action": "BUY" if adjustment > 0 else "SELL",
                "value": abs(adjustment),
                "reason": f"Rebalance to {target_weight*100:.1f}%"
            })

    return suggestions
```

## Security Considerations

**⚠️ IMPORTANT**: This module handles sensitive financial data.

1. **API Keys**: Never commit broker API keys to Git
   ```bash
   # Store in .env file
   ZERODHA_API_KEY=your_key_here
   ZERODHA_ACCESS_TOKEN=your_token_here
   ```

2. **Database**: Encrypt the portfolio database
   ```bash
   # Use encrypted database
   tracker = PortfolioTracker(db_path="encrypted.db")
   ```

3. **Permissions**: Limit file access
   ```bash
   chmod 600 data/portfolio.db
   ```

4. **Read-Only APIs**: Use read-only API keys during development

## Troubleshooting

### Problem: Broker sync not working

**Solution**:
```python
# Check broker client
sync = BrokerSync("zerodha", api_key="...", access_token="...")
if not sync.client:
    print("Client not initialized. Check API keys.")

# Test connection
try:
    profile = sync.client.profile()
    print(f"Connected as: {profile['user_name']}")
except Exception as e:
    print(f"Connection failed: {e}")
```

### Problem: Alerts not triggering

**Solution**:
```python
# Check alert thresholds
alerts = EmergencyAlertSystem()
print(alerts.config)

# Lower thresholds for testing
alerts.config["intraday_drop_pct"] = 2.0  # Alert on 2% drop
```

### Problem: Execution rate is 0%

**Solution**:
```python
# Check if signal_id is linked correctly
tracker.record_trade(
    ...,
    signal_id=signal_id  # Make sure this is set!
)

# Verify signals are recorded
signals = tracker.get_signal_performance()
print(f"Total signals: {len(signals)}")
print(f"Executed signals: {signals['executed'].sum()}")
```

## Testing

Run tests:
```bash
# Unit tests
pytest tests/unit/portfolio/

# Integration tests
pytest tests/integration/test_portfolio_tracking.py
```

## API Reference

See detailed API documentation:
- [PortfolioTracker API](../docs/api/portfolio_tracker.md)
- [EmergencyAlertSystem API](../docs/api/emergency_alerts.md)
- [BrokerSync API](../docs/api/broker_sync.md)

## Next Steps

1. **Set up your tracker**: `tracker = PortfolioTracker()`
2. **Connect broker**: Use BrokerSync to import holdings
3. **Enable alerts**: Configure EmergencyAlertSystem
4. **Monitor dashboard**: View portfolio in Streamlit UI
5. **Review feedback**: Check ML feedback to improve models

For more help, see:
- [BEGINNER_GUIDE.md](../docs/BEGINNER_GUIDE.md) - Step-by-step setup
- [ML_EXPLAINED.md](../docs/ML_EXPLAINED.md) - How ML learns from your trades
- [LLM_SETUP_GUIDE.md](../docs/LLM_SETUP_GUIDE.md) - Ask LLM about your portfolio
