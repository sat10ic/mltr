# Development Guide
## LLM-Integrated ML Trading Research & Intelligence System

---

## Quick Start

### First Time Setup

```bash
# 1. Clone and enter directory
git clone https://github.com/yourusername/mltr.git
cd mltr

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
pip install -e ".[dev]"

# 4. Configure
cp .env.example .env
cp configs/config.example.yaml configs/config.yaml
# Edit both files with your settings

# 5. Download sample data
python scripts/setup_data.py --universe NIFTY50 --days 365

# 6. Run tests to verify setup
pytest tests/
```

---

## Project Overview

### What is MLTR?

MLTR is a **self-learning trading intelligence system** that:
- Learns from price action, indicators, and market sentiment
- Uses machine learning to predict price movements
- Incorporates a local LLM for natural language interaction
- Continuously improves through feedback loops
- Maintains safety through rigorous testing

### Key Principles

1. **No Future Data Leakage**: All features use only past data
2. **Statistical Rigor**: Walk-forward validation, significance testing
3. **Transparency**: Every signal explainable with evidence
4. **Safety First**: Feature gating, human approval, audit logs
5. **Continuous Learning**: Daily retraining, feedback loops

---

## Architecture Overview

### Layer Structure

```
User Interface (Streamlit, FastAPI)
         ↓
LLM Orchestration (Qwen/LLaMA)
         ↓
Application Layer (ML, Signals, Backtest)
         ↓
Feature Engineering (Technical, Sentiment)
         ↓
Data Layer (Market, News, Knowledge)
```

### Module Map

| Module | Purpose | Key Files |
|--------|---------|-----------|
| `src/data/` | Data acquisition & storage | `market/fetcher.py`, `news/scrapers.py` |
| `src/features/` | Feature engineering | `technical/indicators.py`, `sentiment/analyzer.py` |
| `src/ml/` | Machine learning | `models/xgboost_model.py`, `training.py` |
| `src/signals/` | Signal generation | `generator.py`, `risk_manager.py` |
| `src/backtest/` | Backtesting | `engine.py`, `indicator_league.py` |
| `src/llm/` | LLM integration | `inference.py`, `rag.py` |
| `src/knowledge/` | Knowledge base | `ingest_pdf.py`, `vector_store.py` |
| `src/api/` | REST API | `main.py`, `endpoints/` |
| `src/dashboard/` | Streamlit UI | `app.py`, `pages/` |

---

## Development Workflow

### Phase 1: Data Infrastructure (Weeks 1-8)

**Goal**: Build robust data pipelines

#### Week 1-2: Market Data

**Tasks**:
1. Implement `src/data/market/fetcher.py`:
   ```python
   def fetch_ohlcv(symbol: str, start: str, end: str) -> pd.DataFrame:
       """Fetch OHLCV data from source"""
   ```

2. Implement `src/data/market/storage.py`:
   ```python
   def save_parquet(df: pd.DataFrame, path: str):
       """Save data in Parquet format"""
   ```

3. Implement `src/data/market/database.py`:
   ```python
   def query_ohlcv(symbol: str, start: str, end: str) -> pd.DataFrame:
       """Query data from DuckDB"""
   ```

**Test**:
```bash
python -m src.data.market.fetcher --symbols RELIANCE TCS --days 365
pytest tests/unit/data/test_market.py
```

#### Week 3-4: Technical Indicators

**Tasks**:
1. Implement indicators in `src/features/technical/indicators.py`:
   ```python
   def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
       """Calculate RSI indicator"""

   def calculate_macd(prices: pd.Series) -> pd.DataFrame:
       """Calculate MACD indicator"""
   ```

2. Create indicator registry in `src/features/technical/registry.py`

3. Write comprehensive tests

**Test**:
```bash
pytest tests/unit/features/test_technical.py -v
# Verify against TradingView values for 5 stocks
```

#### Week 5-6: News & Sentiment

**Tasks**:
1. Implement scrapers in `src/data/news/scrapers/`
2. Implement sentiment analysis in `src/data/news/sentiment.py`
3. Create storage schema in DuckDB

**Example**:
```python
from src.data.news.scrapers import NewsAPIScraper
from src.data.news.sentiment import analyze_sentiment

# Scrape news
scraper = NewsAPIScraper(api_key="...")
articles = scraper.fetch(query="Reliance", days=7)

# Analyze sentiment
for article in articles:
    article['sentiment'] = analyze_sentiment(article['content'])
```

#### Week 7-8: Feature Store

**Tasks**:
1. Create feature store in `src/features/store/`
2. Implement feature metadata tracking
3. Add data quality checks

**Feature Store Interface**:
```python
from src.features.store import FeatureStore

store = FeatureStore()

# Register feature
store.register_feature(
    name="rsi_14",
    function=calculate_rsi,
    params={"period": 14},
    category="momentum",
    lag_safe=True
)

# Compute features
features = store.compute_features(
    symbols=["RELIANCE", "TCS"],
    start="2024-01-01",
    end="2024-12-31"
)
```

---

### Phase 2: ML & Signals (Weeks 9-16)

#### Week 9-10: Labeling & Training Infrastructure

**Tasks**:
1. Implement labeling in `src/ml/labeling/`:
   ```python
   def create_binary_labels(
       df: pd.DataFrame,
       forward_days: int = 5,
       threshold_pct: float = 2.0
   ) -> pd.Series:
       """Create binary classification labels"""
   ```

2. Implement time-series CV in `src/ml/validation/`
3. Set up MLflow tracking

**Example Training Script**:
```python
from src.ml.training import train_model
from src.ml.validation import walk_forward_split

# Load features
features = load_features()

# Create labels
labels = create_binary_labels(features, forward_days=5, threshold_pct=2.0)

# Walk-forward validation
for train_idx, test_idx in walk_forward_split(features):
    X_train, X_test = features.iloc[train_idx], features.iloc[test_idx]
    y_train, y_test = labels.iloc[train_idx], labels.iloc[test_idx]

    # Train
    model = train_model(X_train, y_train, model_type="xgboost")

    # Evaluate
    score = evaluate_model(model, X_test, y_test)
    mlflow.log_metrics(score)
```

#### Week 11-12: ML Models

**Tasks**:
1. Implement models in `src/ml/models/`
2. Add probability calibration
3. Create model registry

**Model Template**:
```python
# src/ml/models/xgboost_model.py
from xgboost import XGBClassifier

class XGBoostModel:
    def __init__(self, **params):
        self.model = XGBClassifier(**params)

    def train(self, X, y):
        self.model.fit(X, y)

    def predict_proba(self, X):
        return self.model.predict_proba(X)[:, 1]

    def calibrate(self, X_val, y_val):
        """Apply probability calibration"""
        from sklearn.calibration import CalibratedClassifierCV
        self.model = CalibratedClassifierCV(
            self.model,
            method="isotonic",
            cv="prefit"
        )
        self.model.fit(X_val, y_val)
```

#### Week 13-14: Signal Generation

**Tasks**:
1. Implement signal generator in `src/signals/generator.py`
2. Implement risk management in `src/signals/risk_manager.py`
3. Create signal card format

**Signal Generation Pipeline**:
```python
from src.signals.generator import SignalGenerator

generator = SignalGenerator(
    model_version="xgboost_v1.0",
    min_confidence=0.6
)

# Generate signals
signals = generator.generate_signals(date="2024-11-03")

# Apply risk management
from src.signals.risk_manager import RiskManager
risk_mgr = RiskManager()

for signal in signals:
    signal = risk_mgr.apply_risk_rules(signal)
    signal = risk_mgr.calculate_position_size(signal)
```

#### Week 15-16: Backtesting

**Tasks**:
1. Implement backtesting engine with vectorbt
2. Create performance metrics module
3. Build report generator

**Backtest Example**:
```python
from src.backtest.engine import BacktestEngine

engine = BacktestEngine()

results = engine.run(
    strategy="momentum_v1",
    symbols=["RELIANCE", "TCS", "INFY"],
    start="2023-01-01",
    end="2024-12-31",
    commission=0.0003,  # 0.03%
    slippage=0.0002
)

print(f"Sharpe: {results.sharpe:.2f}")
print(f"CAGR: {results.cagr:.2%}")
print(f"Max DD: {results.max_drawdown:.2%}")

# Generate report
results.generate_report("backtest_report.html")
```

---

### Phase 3: LLM Integration (Weeks 17-24)

#### Week 17-18: Local LLM Setup

**Tasks**:
1. Download and quantize LLM (Qwen 2.5 7B)
2. Create inference wrapper in `src/llm/inference.py`
3. Implement function calling

**LLM Setup**:
```bash
# Download model
cd models/llm
wget https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF/resolve/main/qwen2.5-7b-instruct-q4_k_m.gguf

# Install llama.cpp
pip install llama-cpp-python
```

**Usage**:
```python
from src.llm.inference import LLM

llm = LLM(model_path="models/llm/qwen2.5-7b-instruct-q4_k_m.gguf")

response = llm.query(
    "Show me momentum stocks in IT sector with RSI > 60",
    functions=["fetch_data", "filter_stocks"]
)
```

#### Week 19-20: RAG & Knowledge Base

**Tasks**:
1. Implement PDF ingestion in `src/knowledge/ingest_pdf.py`
2. Create vector store in `src/knowledge/vector_store.py`
3. Build RAG pipeline

**RAG Pipeline**:
```python
from src.knowledge.ingest_pdf import ingest_pdf
from src.knowledge.vector_store import VectorStore
from src.llm.rag import RAGPipeline

# Ingest paper
chunks = ingest_pdf("papers/momentum_strategies.pdf")

# Store embeddings
vector_store = VectorStore()
vector_store.add_documents(chunks)

# Query
rag = RAGPipeline(llm, vector_store)
response = rag.query("What are effective momentum indicators?")
```

---

### Phase 4: Production (Weeks 25-32)

#### Deployment Checklist

- [ ] All tests passing
- [ ] Configuration validated
- [ ] Secrets in environment variables (not hardcoded)
- [ ] Logging configured
- [ ] Monitoring set up
- [ ] Backup strategy in place
- [ ] Documentation complete

#### Production Workflow

```bash
# 1. Set up production environment
export MLTR_ENV=production
export MLTR_DEBUG=false

# 2. Run in Docker
docker-compose up -d

# 3. Monitor logs
docker-compose logs -f api

# 4. Check health
curl http://localhost:8000/health
```

---

## Testing Strategy

### Test Pyramid

```
        /\
       /E2E\     (5%) - End-to-end tests
      /------\
     /Integr.\  (15%) - Integration tests
    /----------\
   /   Unit     \ (80%) - Unit tests
  /--------------\
```

### Writing Tests

**Unit Test Example**:
```python
# tests/unit/features/test_indicators.py
import pytest
import pandas as pd
from src.features.technical.indicators import calculate_rsi

def test_rsi_range():
    """RSI should be between 0 and 100"""
    prices = pd.Series([100, 102, 101, 105, 107, 106, 108, 110])
    rsi = calculate_rsi(prices, period=14)
    assert (rsi >= 0).all()
    assert (rsi <= 100).all()

def test_rsi_extreme_uptrend():
    """RSI should approach 100 in strong uptrend"""
    prices = pd.Series(range(100, 120))  # Strong uptrend
    rsi = calculate_rsi(prices, period=14)
    assert rsi.iloc[-1] > 70  # Should be overbought

def test_rsi_with_insufficient_data():
    """RSI should handle insufficient data gracefully"""
    prices = pd.Series([100, 102, 101])
    with pytest.raises(ValueError):
        calculate_rsi(prices, period=14)
```

**Integration Test Example**:
```python
# tests/integration/test_signal_pipeline.py
def test_full_signal_generation_pipeline(sample_data):
    """Test complete pipeline from data to signal"""
    # 1. Compute features
    features = compute_features(sample_data)
    assert not features.empty

    # 2. Load model
    model = load_model("xgboost_v1.0")
    assert model is not None

    # 3. Generate predictions
    predictions = model.predict(features)
    assert len(predictions) == len(features)

    # 4. Generate signals
    signals = generate_signals(predictions, min_confidence=0.6)
    assert all(s.confidence >= 0.6 for s in signals)

    # 5. Apply risk management
    for signal in signals:
        assert signal.stop_loss < signal.entry_price < signal.take_profit
        assert signal.position_size > 0
```

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/unit/features/test_indicators.py

# Specific test
pytest tests/unit/features/test_indicators.py::test_rsi_range

# With coverage
pytest --cov=src --cov-report=html

# Skip slow tests
pytest -m "not slow"

# Only integration tests
pytest -m integration
```

---

## Debugging Tips

### Common Issues

**Issue**: Data leakage in features
```python
# BAD - uses future data
df['future_return'] = df['close'].shift(-5).pct_change()

# GOOD - uses only past data
df['past_return'] = df['close'].pct_change(5)
```

**Issue**: Model overfitting
- Use walk-forward validation (not random split)
- Add regularization
- Reduce feature count
- Check calibration curve

**Issue**: Slow backtest
- Use vectorbt (not pandas loops)
- Pre-compute features
- Use Parquet (not CSV)
- Profile code: `python -m cProfile script.py`

### Logging

```python
from loguru import logger

# Configure logger
logger.add(
    "logs/mltr_{time}.log",
    rotation="1 day",
    retention="30 days",
    level="INFO"
)

# Usage
logger.debug("Detailed debugging info")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred")
logger.exception("Exception with traceback")
```

---

## Performance Optimization

### Database Queries

```python
# Slow: Load all data then filter
df = pd.read_parquet("data.parquet")
df_filtered = df[df['symbol'] == 'RELIANCE']

# Fast: Filter at read time
df_filtered = pd.read_parquet(
    "data.parquet",
    filters=[('symbol', '=', 'RELIANCE')]
)

# Fastest: Use DuckDB
import duckdb
conn = duckdb.connect("market.db")
df = conn.execute("""
    SELECT * FROM ohlcv
    WHERE symbol = 'RELIANCE'
    AND timestamp >= '2024-01-01'
""").df()
```

### Feature Computation

```python
# Use vectorized operations
# Slow
df['return'] = df.apply(lambda x: (x['close'] / x['close'].shift(1)) - 1, axis=1)

# Fast
df['return'] = df['close'].pct_change()

# Use polars for large datasets
import polars as pl
df = pl.read_parquet("data.parquet")
df = df.with_columns([
    pl.col("close").pct_change().alias("return")
])
```

---

## Best Practices

### 1. Configuration Management

✅ **DO**: Use config files
```python
from src.config import config
threshold = config.signals.thresholds.min_confidence
```

❌ **DON'T**: Hardcode values
```python
threshold = 0.6  # Magic number
```

### 2. Error Handling

✅ **DO**: Specific exceptions with context
```python
try:
    data = fetch_data(symbol)
except APIError as e:
    logger.error(f"API failed for {symbol}: {e}")
    raise
```

❌ **DON'T**: Bare except
```python
try:
    data = fetch_data(symbol)
except:
    pass  # Silent failure
```

### 3. Documentation

✅ **DO**: Clear docstrings
```python
def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """Calculate Relative Strength Index.

    Args:
        prices: Series of closing prices
        period: RSI period (default: 14)

    Returns:
        Series of RSI values (0-100)

    Raises:
        ValueError: If period invalid or prices too short
    """
```

❌ **DON'T**: No documentation
```python
def calc_rsi(p, n=14):
    # Calculate RSI
    ...
```

---

## Resources

### Learning Materials

- [Advances in Financial Machine Learning](https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086) by Marcos López de Prado
- [Machine Learning for Algorithmic Trading](https://github.com/stefan-jansen/machine-learning-for-trading)
- [VectorBT Documentation](https://vectorbt.dev/)
- [LangChain Documentation](https://python.langchain.com/)

### Tools

- **Data**: yfinance, pandas, polars, DuckDB
- **ML**: scikit-learn, XGBoost, LightGBM
- **Backtesting**: vectorbt
- **LLM**: llama.cpp, Ollama, LangChain
- **Testing**: pytest, hypothesis
- **Code Quality**: black, isort, flake8, mypy

---

## Getting Help

- **Documentation**: See `docs/` directory
- **Issues**: Open a GitHub issue
- **Discussions**: Use GitHub Discussions
- **Code Review**: Submit a PR for review

---

**Happy coding!** 🚀
