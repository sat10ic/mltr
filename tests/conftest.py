"""
Pytest configuration and shared fixtures for MLTR tests.
"""

import os
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import pytest


# Test markers
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "e2e: marks tests as end-to-end tests")
    config.addinivalue_line("markers", "llm: marks tests requiring LLM")
    config.addinivalue_line("markers", "backtest: marks tests running backtests")
    config.addinivalue_line("markers", "api: marks tests requiring API calls")


# Set random seeds for reproducibility
@pytest.fixture(scope="session", autouse=True)
def set_random_seeds():
    """Set random seeds for reproducibility."""
    np.random.seed(42)
    # Additional seeds for ML libraries
    os.environ["PYTHONHASHSEED"] = "42"


# Paths
@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """Path to test data directory."""
    path = Path(__file__).parent / "data"
    path.mkdir(exist_ok=True)
    return path


@pytest.fixture(scope="session")
def temp_output_dir(tmp_path_factory) -> Path:
    """Temporary directory for test outputs."""
    return tmp_path_factory.mktemp("outputs")


# Sample OHLCV data
@pytest.fixture
def sample_ohlcv_data() -> pd.DataFrame:
    """Generate sample OHLCV data for testing."""
    np.random.seed(42)

    dates = pd.date_range(start="2024-01-01", periods=100, freq="D")
    symbols = ["RELIANCE", "TCS", "INFY"]

    data = []
    for symbol in symbols:
        base_price = np.random.uniform(1000, 3000)
        prices = base_price + np.cumsum(np.random.randn(len(dates)) * 10)

        for i, date in enumerate(dates):
            open_price = prices[i] + np.random.randn() * 2
            high_price = max(open_price, prices[i]) + abs(np.random.randn())
            low_price = min(open_price, prices[i]) - abs(np.random.randn())
            close_price = prices[i]
            volume = int(np.random.uniform(1000000, 5000000))
            delivery_pct = np.random.uniform(40, 80)

            data.append(
                {
                    "symbol": symbol,
                    "timestamp": date,
                    "open": round(open_price, 2),
                    "high": round(high_price, 2),
                    "low": round(low_price, 2),
                    "close": round(close_price, 2),
                    "volume": volume,
                    "delivery_pct": round(delivery_pct, 2),
                }
            )

    df = pd.DataFrame(data)
    return df


@pytest.fixture
def sample_features() -> pd.DataFrame:
    """Generate sample feature data for testing."""
    np.random.seed(42)

    dates = pd.date_range(start="2024-01-01", periods=100, freq="D")
    symbols = ["RELIANCE", "TCS"]

    data = []
    for symbol in symbols:
        for date in dates:
            data.append(
                {
                    "symbol": symbol,
                    "timestamp": date,
                    "rsi_14": np.random.uniform(30, 70),
                    "macd": np.random.uniform(-10, 10),
                    "bb_position": np.random.uniform(0, 1),
                    "volume_ratio": np.random.uniform(0.5, 2.0),
                    "sentiment_score": np.random.uniform(-0.5, 0.5),
                }
            )

    return pd.DataFrame(data)


@pytest.fixture
def sample_news_data() -> pd.DataFrame:
    """Generate sample news data for testing."""
    np.random.seed(42)

    articles = [
        {
            "article_id": "news_001",
            "source": "economictimes",
            "title": "Reliance Industries posts strong Q4 results",
            "content": "Reliance Industries reported strong quarterly results with revenue growth.",
            "published_at": datetime.now() - timedelta(days=1),
            "sentiment_score": 0.75,
            "sentiment_label": "positive",
            "symbols_mentioned": ["RELIANCE"],
        },
        {
            "article_id": "news_002",
            "source": "moneycontrol",
            "title": "TCS wins major contract in Europe",
            "content": "TCS announced a multi-million dollar deal with European client.",
            "published_at": datetime.now() - timedelta(days=2),
            "sentiment_score": 0.65,
            "sentiment_label": "positive",
            "symbols_mentioned": ["TCS"],
        },
        {
            "article_id": "news_003",
            "source": "businessstandard",
            "title": "IT sector faces headwinds",
            "content": "Indian IT sector facing challenges due to global economic slowdown.",
            "published_at": datetime.now() - timedelta(days=3),
            "sentiment_score": -0.45,
            "sentiment_label": "negative",
            "symbols_mentioned": ["TCS", "INFY", "WIPRO"],
        },
    ]

    return pd.DataFrame(articles)


@pytest.fixture
def sample_model_predictions() -> pd.DataFrame:
    """Generate sample model predictions for testing."""
    np.random.seed(42)

    symbols = ["RELIANCE", "TCS", "INFY"]
    dates = pd.date_range(start="2024-01-01", periods=30, freq="D")

    data = []
    for symbol in symbols:
        for date in dates:
            probability = np.random.uniform(0.3, 0.9)
            data.append(
                {
                    "symbol": symbol,
                    "prediction_date": date,
                    "target_date": date + timedelta(days=5),
                    "predicted_return": np.random.uniform(-0.02, 0.05),
                    "probability": probability,
                    "confidence": probability * np.random.uniform(0.9, 1.0),
                }
            )

    return pd.DataFrame(data)


@pytest.fixture
def sample_signal() -> dict:
    """Generate a sample trading signal."""
    return {
        "signal_id": "sig_001",
        "symbol": "RELIANCE",
        "signal_date": "2024-11-03",
        "action": "BUY",
        "entry_price": 2450.00,
        "stop_loss": 2400.00,
        "take_profit": 2550.00,
        "position_size": 100,
        "confidence": 0.72,
        "reasoning": "Bullish RSI divergence + positive sector sentiment",
        "ml_probability": 0.68,
        "sentiment_boost": 0.04,
    }


@pytest.fixture
def sample_config() -> dict:
    """Generate sample configuration for testing."""
    return {
        "features": {
            "technical": {
                "momentum": {"rsi_periods": [14], "macd_fast": 12, "macd_slow": 26},
                "trend": {"sma_periods": [20, 50], "ema_periods": [10, 20]},
            },
            "sentiment": {"aggregation_windows": [1, 3, 7]},
        },
        "ml": {
            "targets": {
                "binary": {"forward_days": 5, "threshold_pct": 2.0},
            },
            "training": {
                "cv_folds": 3,  # Reduced for testing
                "test_size": 0.2,
            },
        },
        "signals": {
            "thresholds": {"min_confidence": 0.6},
            "filters": {"min_liquidity_tier": 2},
        },
        "risk": {
            "position": {"risk_per_trade_pct": 1.0, "max_position_size_pct": 3.0},
            "portfolio": {"max_positions": 10, "max_sector_allocation_pct": 30},
        },
    }


# Mock objects for external dependencies
@pytest.fixture
def mock_api_response():
    """Mock API response for testing."""

    class MockResponse:
        def __init__(self, json_data, status_code=200):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self):
            if self.status_code != 200:
                raise Exception(f"HTTP {self.status_code}")

    return MockResponse


@pytest.fixture
def mock_llm_response():
    """Mock LLM response for testing."""

    class MockLLM:
        def query(self, prompt, **kwargs):
            return {
                "response": "This is a mock LLM response",
                "function_calls": [],
                "tokens_used": 100,
            }

        def generate(self, prompt, **kwargs):
            return "Mock generated text"

    return MockLLM()


# Database fixtures
@pytest.fixture
def in_memory_duckdb():
    """Create an in-memory DuckDB connection for testing."""
    import duckdb

    conn = duckdb.connect(":memory:")
    yield conn
    conn.close()


# Cleanup
@pytest.fixture(autouse=True)
def cleanup_after_test():
    """Cleanup after each test."""
    yield
    # Add any cleanup logic here
    pass
