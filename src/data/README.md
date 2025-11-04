# Data Layer

The data layer handles all data acquisition, storage, and retrieval for the MLTR system.

## Structure

```
data/
├── market/         # OHLCV market data
│   ├── fetcher.py      # Data download
│   ├── storage.py      # Parquet/DuckDB storage
│   └── database.py     # Query interface
├── news/           # News & social media
│   ├── scrapers/       # RSS, NewsAPI, Twitter
│   ├── sentiment.py    # Sentiment analysis
│   └── storage.py      # News database
└── reference/      # Static reference data
    ├── symbols.py      # Symbol universe management
    ├── calendar.py     # Market holidays
    └── sectors.py      # Sector classifications
```

## Market Data (`market/`)

### Purpose
Download, store, and serve OHLCV (Open, High, Low, Close, Volume) data for Indian stocks.

### Key Components

#### 1. Data Fetcher (`fetcher.py`)
Downloads historical and live market data.

**Example Usage:**
```python
from src.data.market.fetcher import fetch_ohlcv

# Download historical data
df = fetch_ohlcv(
    symbol="RELIANCE",
    start="2024-01-01",
    end="2024-12-31",
    source="yfinance"
)
```

**Expected Output:**
```
   symbol  timestamp      open      high       low     close    volume  delivery_pct
0  RELIANCE 2024-01-01  2450.00  2465.50  2445.25  2460.75  1250000         55.2
1  RELIANCE 2024-01-02  2461.00  2475.80  2458.00  2470.50  1320000         58.1
```

#### 2. Storage (`storage.py`)
Saves data in Parquet format for fast columnar access.

**Example:**
```python
from src.data.market.storage import save_ohlcv, load_ohlcv

# Save data
save_ohlcv(df, path="data/processed/ohlcv")

# Load data
df = load_ohlcv(
    symbols=["RELIANCE", "TCS"],
    start="2024-01-01",
    end="2024-12-31"
)
```

#### 3. Database Interface (`database.py`)
Query data using DuckDB SQL.

**Example:**
```python
from src.data.market.database import query_ohlcv

# SQL query
df = query_ohlcv("""
    SELECT symbol, timestamp, close, volume
    FROM ohlcv
    WHERE symbol IN ('RELIANCE', 'TCS')
    AND timestamp >= '2024-01-01'
    ORDER BY timestamp
""")
```

---

## News & Social Data (`news/`)

### Purpose
Collect and analyze news articles, social media posts, and other textual data for sentiment analysis.

### Key Components

#### 1. Scrapers (`scrapers/`)

**RSS Scraper:**
```python
from src.data.news.scrapers.rss import RSSFeedScraper

scraper = RSSFeedScraper(feeds=[
    "https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms"
])
articles = scraper.fetch(days=7)
```

**NewsAPI:**
```python
from src.data.news.scrapers.newsapi import NewsAPIScraper

scraper = NewsAPIScraper(api_key="your_key")
articles = scraper.fetch(
    query="Reliance Industries",
    from_date="2024-11-01",
    to_date="2024-11-03"
)
```

#### 2. Sentiment Analysis (`sentiment.py`)

```python
from src.data.news.sentiment import analyze_sentiment

text = "Company reports strong quarterly earnings"
result = analyze_sentiment(text)

# Output:
# {
#     'label': 'positive',
#     'score': 0.85,
#     'confidence': 0.92
# }
```

**Batch Processing:**
```python
results = analyze_sentiment_batch(articles['content'].tolist())
```

---

## Reference Data (`reference/`)

### Purpose
Manage static reference data like symbol universes, market calendars, and sector classifications.

#### Symbol Universe (`symbols.py`)

```python
from src.data.reference.symbols import get_symbol_universe

# Get Nifty 50 symbols
nifty50 = get_symbol_universe("NIFTY50")

# Get all symbols in a sector
it_stocks = get_symbols_by_sector("Information Technology")
```

#### Market Calendar (`calendar.py`)

```python
from src.data.reference.calendar import is_trading_day, get_trading_days

# Check if market is open
if is_trading_day("2024-11-03"):
    print("Market is open")

# Get trading days in range
trading_days = get_trading_days(
    start="2024-01-01",
    end="2024-12-31"
)
```

---

## Data Schemas

All data must conform to defined schemas for validation.

### OHLCV Schema
```python
{
    'symbol': str,          # Stock symbol
    'timestamp': datetime,  # Timestamp (IST)
    'open': float,          # Opening price
    'high': float,          # Highest price
    'low': float,           # Lowest price
    'close': float,         # Closing price
    'volume': int,          # Trading volume
    'delivery_pct': float   # Delivery percentage (optional)
}
```

### News Schema
```python
{
    'article_id': str,           # Unique article ID
    'source': str,               # Source name
    'title': str,                # Article title
    'content': str,              # Full text
    'published_at': datetime,    # Publication time
    'sentiment_score': float,    # -1 to 1
    'sentiment_label': str,      # positive/negative/neutral
    'symbols_mentioned': list    # Ticker symbols found
}
```

---

## Configuration

Data sources are configured in `configs/config.yaml`:

```yaml
data:
  market:
    provider: "yfinance"
    fallback_provider: "nse_official"
    universe: "NIFTY500"

  news:
    newsapi:
      enabled: true
      api_key: "${NEWSAPI_KEY}"
    rss:
      enabled: true
      feeds:
        - "https://economictimes.indiatimes.com/..."
```

---

## Data Quality

### Validation
All incoming data is validated:

```python
from src.data.schemas import validate_ohlcv

# Raises SchemaError if invalid
validated_df = validate_ohlcv(raw_df)
```

### Quality Checks
- No missing timestamps
- High >= Low, High >= Open/Close, Low <= Open/Close
- Volume >= 0
- No duplicate (symbol, timestamp) pairs
- Sentiment scores in [-1, 1]

---

## Storage Architecture

### Parquet Files
```
data/
└── processed/
    └── ohlcv/
        ├── date=2024-01-01/
        │   ├── RELIANCE.parquet
        │   └── TCS.parquet
        ├── date=2024-01-02/
        └── ...
```

**Advantages:**
- Fast columnar access
- Excellent compression
- Schema enforcement
- Efficient filtering

### DuckDB Database
```sql
-- ohlcv table
CREATE TABLE ohlcv (
    symbol VARCHAR,
    timestamp TIMESTAMP,
    open DECIMAL(10,2),
    high DECIMAL(10,2),
    low DECIMAL(10,2),
    close DECIMAL(10,2),
    volume BIGINT,
    delivery_pct DECIMAL(5,2)
);

CREATE INDEX idx_symbol_timestamp ON ohlcv(symbol, timestamp);
```

---

## Performance Considerations

### 1. Batch Operations
```python
# Good: Batch fetch
symbols = ["RELIANCE", "TCS", "INFY"]
df = fetch_ohlcv_batch(symbols, start, end)

# Bad: Loop fetch
for symbol in symbols:
    df = fetch_ohlcv(symbol, start, end)
```

### 2. Filtering at Read Time
```python
# Good: Filter in Parquet read
df = pd.read_parquet(
    "data.parquet",
    filters=[('symbol', '=', 'RELIANCE')]
)

# Bad: Load then filter
df = pd.read_parquet("data.parquet")
df = df[df['symbol'] == 'RELIANCE']
```

### 3. Use DuckDB for Complex Queries
```python
# Good: DuckDB SQL
df = conn.execute("""
    SELECT symbol, AVG(close) as avg_close
    FROM ohlcv
    WHERE timestamp >= '2024-01-01'
    GROUP BY symbol
    HAVING AVG(close) > 1000
""").df()

# Bad: Pandas operations
df = pd.read_parquet("data.parquet")
df = df[df['timestamp'] >= '2024-01-01']
df = df.groupby('symbol')['close'].mean()
df = df[df > 1000]
```

---

## Testing

### Unit Tests
```bash
pytest tests/unit/data/
```

### Schema Tests
```bash
pytest tests/unit/data/test_schemas.py
```

### Integration Tests
```bash
pytest tests/integration/test_data_pipeline.py
```

---

## Error Handling

### API Failures
```python
from src.data.market.fetcher import fetch_ohlcv
from src.data.exceptions import DataFetchError

try:
    df = fetch_ohlcv("RELIANCE", start, end)
except DataFetchError as e:
    logger.error(f"Failed to fetch data: {e}")
    # Fall back to cached data or alternative source
```

### Data Quality Issues
```python
from src.data.quality import check_data_quality

issues = check_data_quality(df)
if issues:
    logger.warning(f"Data quality issues: {issues}")
    # Handle gaps, outliers, etc.
```

---

## Next Steps

1. **Implement fetchers**: Start with `market/fetcher.py`
2. **Add storage layer**: Parquet + DuckDB in `storage.py`
3. **Build scrapers**: RSS and NewsAPI in `news/scrapers/`
4. **Add sentiment**: Transformer model in `news/sentiment.py`
5. **Write tests**: Schema validation and integration tests

---

## Related Documentation

- [ARCHITECTURE.md](../../ARCHITECTURE.md) - System architecture
- [DEVELOPMENT_GUIDE.md](../../DEVELOPMENT_GUIDE.md) - Development workflow
- [tests/unit/data/](../../tests/unit/data/) - Test examples
