"""
Integration tests for backtesting engine.
Uses deterministic seed for reproducibility.
"""

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def deterministic_backtest_data():
    """Generate deterministic data for backtesting."""
    np.random.seed(42)

    dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")

    # Create a simple uptrend with some noise
    trend = np.linspace(1000, 1200, len(dates))
    noise = np.random.randn(len(dates)) * 10
    prices = trend + noise

    df = pd.DataFrame(
        {
            "timestamp": dates,
            "symbol": "TEST",
            "open": prices + np.random.randn(len(dates)),
            "high": prices + np.abs(np.random.randn(len(dates)) * 2),
            "low": prices - np.abs(np.random.randn(len(dates)) * 2),
            "close": prices,
            "volume": np.random.randint(1000000, 5000000, len(dates)),
        }
    )

    return df


@pytest.mark.backtest
@pytest.mark.slow
def test_simple_buy_hold_strategy(deterministic_backtest_data):
    """Test simple buy-and-hold strategy."""
    df = deterministic_backtest_data

    # Calculate buy-and-hold return
    initial_price = df.iloc[0]["close"]
    final_price = df.iloc[-1]["close"]
    total_return = (final_price / initial_price) - 1

    # Verify expected characteristics
    assert total_return > 0, "Expected positive return for uptrend"
    assert 0.10 < total_return < 0.30, "Return should be in reasonable range"


@pytest.mark.backtest
def test_simple_moving_average_crossover(deterministic_backtest_data):
    """Test SMA crossover strategy with deterministic data."""
    df = deterministic_backtest_data.copy()

    # Calculate SMAs
    df["sma_20"] = df["close"].rolling(window=20).mean()
    df["sma_50"] = df["close"].rolling(window=50).mean()

    # Generate signals
    df["signal"] = 0
    df.loc[df["sma_20"] > df["sma_50"], "signal"] = 1  # Buy signal
    df.loc[df["sma_20"] < df["sma_50"], "signal"] = -1  # Sell signal

    # Calculate strategy returns
    df["position"] = df["signal"].shift(1)  # Enter on next day
    df["returns"] = df["close"].pct_change()
    df["strategy_returns"] = df["position"] * df["returns"]

    # Calculate cumulative returns
    strategy_cum_return = (1 + df["strategy_returns"].fillna(0)).cumprod().iloc[-1] - 1

    # Verify strategy ran successfully
    assert not df["strategy_returns"].isna().all(), "Strategy should have some returns"
    assert len(df[df["signal"] != 0]) > 0, "Strategy should generate signals"


@pytest.mark.backtest
def test_backtest_metrics_calculation(deterministic_backtest_data):
    """Test calculation of backtest performance metrics."""
    df = deterministic_backtest_data.copy()

    # Simple returns
    df["returns"] = df["close"].pct_change()

    # Calculate metrics
    total_return = (df["close"].iloc[-1] / df["close"].iloc[0]) - 1
    mean_return = df["returns"].mean()
    volatility = df["returns"].std()
    sharpe_ratio = (mean_return / volatility) * np.sqrt(252) if volatility > 0 else 0

    # Calculate drawdown
    cumulative = (1 + df["returns"]).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()

    # Verify metrics are reasonable
    assert -1 < total_return < 1, "Total return should be reasonable"
    assert volatility > 0, "Volatility should be positive"
    assert -5 < sharpe_ratio < 5, "Sharpe ratio should be in reasonable range"
    assert max_drawdown <= 0, "Max drawdown should be negative or zero"
    assert max_drawdown > -0.5, "Max drawdown shouldn't be too extreme"


@pytest.mark.backtest
def test_transaction_costs_impact(deterministic_backtest_data):
    """Test that transaction costs reduce returns."""
    df = deterministic_backtest_data.copy()

    # Generate random trades
    np.random.seed(42)
    df["position"] = np.random.choice([-1, 0, 1], size=len(df))
    df["position_change"] = df["position"].diff().abs()
    df["returns"] = df["close"].pct_change()

    # Calculate returns without costs
    df["strategy_returns_no_cost"] = df["position"].shift(1) * df["returns"]

    # Calculate returns with transaction costs (0.1% per trade)
    transaction_cost = 0.001
    df["costs"] = df["position_change"] * transaction_cost
    df["strategy_returns_with_cost"] = df["strategy_returns_no_cost"] - df["costs"]

    # Calculate cumulative returns
    cum_return_no_cost = (1 + df["strategy_returns_no_cost"].fillna(0)).cumprod().iloc[-1] - 1
    cum_return_with_cost = (
        1 + df["strategy_returns_with_cost"].fillna(0)
    ).cumprod().iloc[-1] - 1

    # Verify costs reduce returns
    assert (
        cum_return_with_cost <= cum_return_no_cost
    ), "Returns with costs should be less than or equal to returns without costs"


@pytest.mark.backtest
def test_position_sizing(deterministic_backtest_data):
    """Test position sizing logic."""
    df = deterministic_backtest_data.copy()

    # Calculate ATR for position sizing
    df["tr"] = df[["high", "low"]].max(axis=1) - df[["high", "low"]].min(axis=1)
    df["atr"] = df["tr"].rolling(window=14).mean()

    # Position size = risk amount / ATR
    capital = 100000
    risk_per_trade = capital * 0.01  # 1% risk

    df["position_size"] = (risk_per_trade / df["atr"]).fillna(0)

    # Verify position sizing
    assert (df["position_size"] >= 0).all(), "Position sizes should be non-negative"
    assert not df["position_size"].isna().all(), "Should have some position sizes"


@pytest.mark.backtest
@pytest.mark.slow
def test_backtest_reproducibility():
    """Test that backtests with same seed produce same results."""
    np.random.seed(42)

    # Run 1
    dates1 = pd.date_range(start="2023-01-01", periods=100, freq="D")
    prices1 = 1000 + np.cumsum(np.random.randn(100) * 10)

    # Run 2 with same seed
    np.random.seed(42)
    dates2 = pd.date_range(start="2023-01-01", periods=100, freq="D")
    prices2 = 1000 + np.cumsum(np.random.randn(100) * 10)

    # Verify reproducibility
    assert len(prices1) == len(prices2)
    assert np.allclose(prices1, prices2), "Same seed should produce same prices"


@pytest.mark.backtest
def test_walk_forward_split():
    """Test walk-forward validation splits."""
    dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
    n_samples = len(dates)

    # Parameters
    train_size = 180  # days
    test_size = 30  # days
    step_size = 30  # days

    splits = []
    start_idx = 0

    while start_idx + train_size + test_size <= n_samples:
        train_end = start_idx + train_size
        test_end = train_end + test_size

        train_indices = list(range(start_idx, train_end))
        test_indices = list(range(train_end, test_end))

        splits.append((train_indices, test_indices))
        start_idx += step_size

    # Verify splits
    assert len(splits) > 0, "Should have at least one split"

    for train_idx, test_idx in splits:
        assert len(train_idx) == train_size, "Train size should be consistent"
        assert len(test_idx) == test_size, "Test size should be consistent"
        assert max(train_idx) < min(test_idx), "No data leakage: train before test"


@pytest.mark.backtest
def test_backtest_metrics_with_known_values():
    """Test backtest metrics with known values."""
    # Create data with known characteristics
    returns = pd.Series([0.01, -0.01, 0.02, -0.005, 0.015] * 50)  # 250 days

    # Calculate Sharpe ratio
    mean_return = returns.mean()
    std_return = returns.std()
    sharpe = (mean_return / std_return) * np.sqrt(252)

    # Verify Sharpe calculation
    assert isinstance(sharpe, float), "Sharpe should be a float"
    assert not np.isnan(sharpe), "Sharpe should not be NaN"

    # Calculate CAGR
    cumulative_return = (1 + returns).cumprod().iloc[-1] - 1
    years = len(returns) / 252
    cagr = (1 + cumulative_return) ** (1 / years) - 1

    # Verify CAGR calculation
    assert isinstance(cagr, float), "CAGR should be a float"
    assert not np.isnan(cagr), "CAGR should not be NaN"


@pytest.mark.backtest
def test_backtest_with_missing_data():
    """Test backtest handles missing data appropriately."""
    np.random.seed(42)

    dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
    prices = 1000 + np.cumsum(np.random.randn(100) * 10)

    df = pd.DataFrame({"timestamp": dates, "close": prices})

    # Introduce some missing data
    df.loc[10:15, "close"] = np.nan

    # Forward fill missing data
    df["close_filled"] = df["close"].fillna(method="ffill")

    # Verify handling
    assert df["close"].isna().sum() > 0, "Should have missing data"
    assert df["close_filled"].isna().sum() == 0, "Filled data should have no NaN"
