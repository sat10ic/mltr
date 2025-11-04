"""
Unit tests for data schemas and validation.
Uses pandera for schema validation.
"""

import pandas as pd
import pandera as pa
import pytest
from pandera import Column, DataFrameSchema


# Define schemas
class OHLCVSchema(DataFrameSchema):
    """Schema for OHLCV data."""

    symbol: str = Column(str, nullable=False)
    timestamp: pd.Timestamp = Column(pd.Timestamp, nullable=False)
    open: float = Column(float, ge=0, nullable=False)
    high: float = Column(float, ge=0, nullable=False)
    low: float = Column(float, ge=0, nullable=False)
    close: float = Column(float, ge=0, nullable=False)
    volume: int = Column(int, ge=0, nullable=False)
    delivery_pct: float = Column(float, ge=0, le=100, nullable=True)

    class Config:
        strict = True
        coerce = True


class FeaturesSchema(DataFrameSchema):
    """Schema for feature data."""

    symbol: str = Column(str, nullable=False)
    timestamp: pd.Timestamp = Column(pd.Timestamp, nullable=False)
    rsi_14: float = Column(float, ge=0, le=100, nullable=True)
    macd: float = Column(float, nullable=True)
    bb_position: float = Column(float, ge=0, le=1, nullable=True)
    volume_ratio: float = Column(float, ge=0, nullable=True)
    sentiment_score: float = Column(float, ge=-1, le=1, nullable=True)


class NewsSchema(DataFrameSchema):
    """Schema for news data."""

    article_id: str = Column(str, nullable=False, unique=True)
    source: str = Column(str, nullable=False)
    title: str = Column(str, nullable=False)
    content: str = Column(str, nullable=False)
    published_at: pd.Timestamp = Column(pd.Timestamp, nullable=False)
    sentiment_score: float = Column(float, ge=-1, le=1, nullable=True)
    sentiment_label: str = Column(str, nullable=True)
    symbols_mentioned: object = Column(object, nullable=True)


def test_ohlcv_schema_validation(sample_ohlcv_data):
    """Test OHLCV data schema validation."""
    # Should pass validation
    validated_df = OHLCVSchema.validate(sample_ohlcv_data)
    assert len(validated_df) == len(sample_ohlcv_data)


def test_ohlcv_schema_high_low_relationship(sample_ohlcv_data):
    """Test that high >= low in OHLCV data."""
    assert (sample_ohlcv_data["high"] >= sample_ohlcv_data["low"]).all()


def test_ohlcv_schema_high_includes_open_close(sample_ohlcv_data):
    """Test that high is >= both open and close."""
    assert (sample_ohlcv_data["high"] >= sample_ohlcv_data["open"]).all()
    assert (sample_ohlcv_data["high"] >= sample_ohlcv_data["close"]).all()


def test_ohlcv_schema_low_includes_open_close(sample_ohlcv_data):
    """Test that low is <= both open and close."""
    assert (sample_ohlcv_data["low"] <= sample_ohlcv_data["open"]).all()
    assert (sample_ohlcv_data["low"] <= sample_ohlcv_data["close"]).all()


def test_ohlcv_schema_invalid_negative_price():
    """Test that negative prices are rejected."""
    invalid_data = pd.DataFrame(
        [
            {
                "symbol": "TEST",
                "timestamp": pd.Timestamp("2024-01-01"),
                "open": -100,  # Invalid
                "high": 105,
                "low": 95,
                "close": 100,
                "volume": 1000,
                "delivery_pct": 50.0,
            }
        ]
    )

    with pytest.raises(pa.errors.SchemaError):
        OHLCVSchema.validate(invalid_data)


def test_ohlcv_schema_invalid_volume():
    """Test that negative volume is rejected."""
    invalid_data = pd.DataFrame(
        [
            {
                "symbol": "TEST",
                "timestamp": pd.Timestamp("2024-01-01"),
                "open": 100,
                "high": 105,
                "low": 95,
                "close": 100,
                "volume": -1000,  # Invalid
                "delivery_pct": 50.0,
            }
        ]
    )

    with pytest.raises(pa.errors.SchemaError):
        OHLCVSchema.validate(invalid_data)


def test_features_schema_validation(sample_features):
    """Test feature data schema validation."""
    validated_df = FeaturesSchema.validate(sample_features)
    assert len(validated_df) == len(sample_features)


def test_features_rsi_range(sample_features):
    """Test that RSI is within valid range 0-100."""
    rsi_values = sample_features["rsi_14"].dropna()
    assert (rsi_values >= 0).all()
    assert (rsi_values <= 100).all()


def test_features_sentiment_range(sample_features):
    """Test that sentiment score is within -1 to 1."""
    sentiment = sample_features["sentiment_score"].dropna()
    assert (sentiment >= -1).all()
    assert (sentiment <= 1).all()


def test_news_schema_validation(sample_news_data):
    """Test news data schema validation."""
    validated_df = NewsSchema.validate(sample_news_data)
    assert len(validated_df) == len(sample_news_data)


def test_news_unique_article_ids(sample_news_data):
    """Test that article IDs are unique."""
    assert sample_news_data["article_id"].is_unique


def test_news_sentiment_range(sample_news_data):
    """Test that sentiment scores are within -1 to 1."""
    sentiment = sample_news_data["sentiment_score"].dropna()
    assert (sentiment >= -1).all()
    assert (sentiment <= 1).all()


def test_news_published_date_not_future(sample_news_data):
    """Test that published dates are not in the future."""
    now = pd.Timestamp.now()
    assert (sample_news_data["published_at"] <= now).all()


# Schema validation functions (can be imported by other modules)
def validate_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    """Validate OHLCV data and return validated DataFrame."""
    return OHLCVSchema.validate(df)


def validate_features(df: pd.DataFrame) -> pd.DataFrame:
    """Validate feature data and return validated DataFrame."""
    return FeaturesSchema.validate(df)


def validate_news(df: pd.DataFrame) -> pd.DataFrame:
    """Validate news data and return validated DataFrame."""
    return NewsSchema.validate(df)
