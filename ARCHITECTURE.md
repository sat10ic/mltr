# System Architecture
## LLM-Integrated ML Trading Research & Intelligence System

---

## Table of Contents

1. [High-Level Architecture](#high-level-architecture)
2. [Data Flow](#data-flow)
3. [Module Dependencies](#module-dependencies)
4. [Database Schema](#database-schema)
5. [API Design](#api-design)
6. [LLM Integration Architecture](#llm-integration-architecture)
7. [Deployment Architecture](#deployment-architecture)
8. [Security & Compliance](#security--compliance)

---

## High-Level Architecture

### System Layers

```
┌─────────────────────────────────────────────────────────────────────┐
│                         PRESENTATION LAYER                           │
│  ┌──────────────────────┐            ┌─────────────────────────┐   │
│  │  Streamlit Dashboard │            │   FastAPI REST API      │   │
│  │  - Real-time signals │            │   - /signals            │   │
│  │  - Backtesting UI    │            │   - /backtest           │   │
│  │  - LLM chat          │            │   - /indicators         │   │
│  │  - Performance viz   │            │   - /knowledge          │   │
│  └──────────────────────┘            └─────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                  ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION LAYER                               │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │              LLM Orchestrator (Qwen/LLaMA)                   │  │
│  │  - Query parser & router                                     │  │
│  │  - Function calling engine                                   │  │
│  │  - Response generator                                        │  │
│  │  - RAG retrieval                                             │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                  ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                               │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────┐  ┌─────────────┐  │
│  │  Signal     │  │  ML Engine  │  │ Backtest │  │  Feedback   │  │
│  │  Generator  │  │  - Train    │  │  Engine  │  │  Loop       │  │
│  │  - Entry    │  │  - Predict  │  │  - Walk  │  │  - Outcome  │  │
│  │  - Risk     │  │  - Calibrate│  │    Fwd   │  │  - Meta-    │  │
│  │    Mgmt     │  │  - Online   │  │  - Metrics│  │   Learning │  │
│  └─────────────┘  └─────────────┘  └──────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                  ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      FEATURE LAYER                                   │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │              Feature Engineering Pipeline                   │    │
│  │  Technical → Sentiment → Regime → Meta → Feature Store     │    │
│  └────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                                  ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────────┐   │
│  │  Market DB  │  │  News DB    │  │  Knowledge Base          │   │
│  │  (DuckDB)   │  │  (DuckDB)   │  │  (FAISS Vector Store)    │   │
│  │  - OHLCV    │  │  - Articles │  │  - Research papers       │   │
│  │  - Features │  │  - Tweets   │  │  - GitHub repos          │   │
│  │  - Parquet  │  │  - Sentiment│  │  - Embeddings            │   │
│  └─────────────┘  └─────────────┘  └──────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. Batch Processing Flow (EOD)

```
┌──────────────┐
│  Data Fetch  │  (16:00 IST - download EOD data)
└──────┬───────┘
       ↓
┌──────────────┐
│  Data QC     │  (validate, clean, fill gaps)
└──────┬───────┘
       ↓
┌──────────────┐
│  Feature Eng │  (compute indicators, sentiment)
└──────┬───────┘
       ↓
┌──────────────┐
│  ML Training │  (walk-forward retrain)
└──────┬───────┘
       ↓
┌──────────────┐
│  Signal Gen  │  (generate next-day signals)
└──────┬───────┘
       ↓
┌──────────────┐
│  Dashboard   │  (update watchlist)
└──────────────┘
```

### 2. Intraday Processing Flow (09:15-15:30 IST)

```
┌──────────────┐
│  Live Stream │  (minute bars via API)
└──────┬───────┘
       ↓
┌──────────────┐
│  Feature Upd │  (incremental indicator update)
└──────┬───────┘
       ↓
┌──────────────┐
│  Online ML   │  (River model predict)
└──────┬───────┘
       ↓
┌──────────────┐
│  Intraday Sig│  (provisional alerts)
└──────────────┘
```

### 3. LLM Query Flow

```
User Query (NL)
       ↓
┌──────────────┐
│  LLM Parser  │  (extract intent + parameters)
└──────┬───────┘
       ↓
┌──────────────┐
│  RAG Search? │  (if knowledge query)
└──────┬───────┘
       ↓
┌──────────────┐
│  Function    │  (call: backtest, signal, etc.)
│  Execution   │
└──────┬───────┘
       ↓
┌──────────────┐
│  LLM Format  │  (generate human response)
└──────┬───────┘
       ↓
  User Response
```

---

## Module Dependencies

### Dependency Graph

```
                    ┌─────────────┐
                    │  Dashboard  │
                    │     API     │
                    └──────┬──────┘
                           ↓
                    ┌─────────────┐
                    │     LLM     │
                    │ Orchestrator│
                    └──────┬──────┘
                           ↓
         ┌─────────────────┼─────────────────┐
         ↓                 ↓                  ↓
   ┌──────────┐     ┌───────────┐     ┌───────────┐
   │ Signals  │     │  Backtest │     │ Knowledge │
   └────┬─────┘     └─────┬─────┘     └─────┬─────┘
        ↓                 ↓                   ↓
   ┌──────────┐     ┌───────────┐     ┌───────────┐
   │ ML Engine│     │ Feedback  │     │ Ingestion │
   └────┬─────┘     └─────┬─────┘     └───────────┘
        ↓                 ↓
   ┌──────────────────────┐
   │  Feature Engineering │
   └──────────┬───────────┘
              ↓
   ┌──────────────────────┐
   │     Data Layer       │
   └──────────────────────┘
```

### Module Import Rules

1. **No circular dependencies**: Enforce via pre-commit hooks
2. **Data layer** has no dependencies (pure I/O)
3. **Feature layer** depends only on data layer
4. **ML/Signals/Backtest** depend on features + data
5. **LLM orchestrator** can import all layers (top-level)
6. **Dashboard/API** import only LLM + high-level modules

---

## Database Schema

### 1. Market Data (DuckDB: `market.db`)

#### Table: `ohlcv`
```sql
CREATE TABLE ohlcv (
    symbol VARCHAR NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    open DECIMAL(10, 2),
    high DECIMAL(10, 2),
    low DECIMAL(10, 2),
    close DECIMAL(10, 2),
    volume BIGINT,
    delivery_pct DECIMAL(5, 2),
    PRIMARY KEY (symbol, timestamp)
);
```

#### Table: `features`
```sql
CREATE TABLE features (
    symbol VARCHAR NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    feature_name VARCHAR NOT NULL,
    feature_value DECIMAL(15, 6),
    PRIMARY KEY (symbol, timestamp, feature_name)
);
```

#### Table: `symbols`
```sql
CREATE TABLE symbols (
    symbol VARCHAR PRIMARY KEY,
    name VARCHAR,
    sector VARCHAR,
    industry VARCHAR,
    market_cap BIGINT,
    liquidity_tier INT,  -- 1: High, 2: Medium, 3: Low
    is_active BOOLEAN DEFAULT TRUE
);
```

### 2. News & Sentiment (DuckDB: `news.db`)

#### Table: `articles`
```sql
CREATE TABLE articles (
    article_id VARCHAR PRIMARY KEY,
    source VARCHAR,
    title TEXT,
    content TEXT,
    url VARCHAR,
    published_at TIMESTAMP,
    fetched_at TIMESTAMP,
    sentiment_score DECIMAL(5, 4),  -- -1 to +1
    sentiment_label VARCHAR,  -- positive, negative, neutral
    symbols_mentioned VARCHAR[],  -- array of tickers
    topic VARCHAR,
    credibility_score DECIMAL(3, 2)
);
```

#### Table: `social_posts`
```sql
CREATE TABLE social_posts (
    post_id VARCHAR PRIMARY KEY,
    platform VARCHAR,  -- twitter, reddit, telegram
    author VARCHAR,
    content TEXT,
    posted_at TIMESTAMP,
    fetched_at TIMESTAMP,
    sentiment_score DECIMAL(5, 4),
    symbols_mentioned VARCHAR[],
    reach INT,  -- retweets, upvotes, views
    engagement INT  -- likes, comments
);
```

### 3. ML & Signals (DuckDB: `ml.db`)

#### Table: `predictions`
```sql
CREATE TABLE predictions (
    prediction_id VARCHAR PRIMARY KEY,
    symbol VARCHAR NOT NULL,
    model_version VARCHAR NOT NULL,
    prediction_date DATE NOT NULL,
    target_date DATE NOT NULL,
    predicted_return DECIMAL(8, 4),
    probability DECIMAL(5, 4),
    confidence DECIMAL(5, 4),
    features_json JSON,
    created_at TIMESTAMP
);
```

#### Table: `signals`
```sql
CREATE TABLE signals (
    signal_id VARCHAR PRIMARY KEY,
    symbol VARCHAR NOT NULL,
    signal_date DATE NOT NULL,
    action VARCHAR,  -- BUY, SELL, HOLD
    entry_price DECIMAL(10, 2),
    stop_loss DECIMAL(10, 2),
    take_profit DECIMAL(10, 2),
    position_size DECIMAL(10, 4),
    confidence DECIMAL(5, 4),
    reasoning TEXT,
    ml_probability DECIMAL(5, 4),
    sentiment_modifier DECIMAL(5, 4),
    status VARCHAR,  -- ACTIVE, EXECUTED, CANCELLED, EXPIRED
    created_at TIMESTAMP
);
```

#### Table: `trades`
```sql
CREATE TABLE trades (
    trade_id VARCHAR PRIMARY KEY,
    signal_id VARCHAR REFERENCES signals(signal_id),
    symbol VARCHAR NOT NULL,
    entry_date DATE NOT NULL,
    entry_price DECIMAL(10, 2),
    exit_date DATE,
    exit_price DECIMAL(10, 2),
    exit_reason VARCHAR,  -- TP, SL, TIMEOUT, MANUAL
    quantity INT,
    realized_return DECIMAL(8, 4),
    realized_pnl DECIMAL(12, 2),
    holding_days INT
);
```

### 4. Knowledge Base (FAISS + Metadata DB)

#### Table: `documents` (DuckDB: `knowledge.db`)
```sql
CREATE TABLE documents (
    doc_id VARCHAR PRIMARY KEY,
    doc_type VARCHAR,  -- pdf, github_repo, blog
    title VARCHAR,
    source_url VARCHAR,
    author VARCHAR,
    published_date DATE,
    ingested_at TIMESTAMP,
    num_chunks INT,
    tags VARCHAR[],
    summary TEXT
);
```

#### Table: `document_chunks`
```sql
CREATE TABLE document_chunks (
    chunk_id VARCHAR PRIMARY KEY,
    doc_id VARCHAR REFERENCES documents(doc_id),
    chunk_index INT,
    content TEXT,
    embedding_id INT,  -- reference to FAISS index
    metadata JSON
);
```

---

## API Design

### FastAPI Endpoints

#### 1. Data Endpoints

```python
GET /api/v1/data/symbols
    Query: sector, liquidity_tier, limit
    Response: List[Symbol]

GET /api/v1/data/ohlcv/{symbol}
    Query: start_date, end_date, interval
    Response: OHLCV[]

GET /api/v1/data/features/{symbol}
    Query: start_date, end_date, features[]
    Response: Features[]
```

#### 2. Signal Endpoints

```python
GET /api/v1/signals/today
    Query: min_confidence, sectors[], limit
    Response: Signal[]

GET /api/v1/signals/{signal_id}
    Response: SignalDetail

POST /api/v1/signals/generate
    Body: {date, symbols[], strategy}
    Response: Signal[]
```

#### 3. Backtesting Endpoints

```python
POST /api/v1/backtest/run
    Body: {
        strategy: str,
        symbols: List[str],
        start_date: date,
        end_date: date,
        params: dict
    }
    Response: BacktestResult

GET /api/v1/backtest/{backtest_id}
    Response: BacktestResult

GET /api/v1/indicators/league
    Query: sort_by, limit
    Response: IndicatorRanking[]
```

#### 4. ML Endpoints

```python
POST /api/v1/ml/train
    Body: {model_type, symbols[], params}
    Response: TrainingJob

GET /api/v1/ml/models
    Response: ModelRegistry[]

POST /api/v1/ml/predict
    Body: {model_version, symbol, date}
    Response: Prediction
```

#### 5. Knowledge Endpoints

```python
POST /api/v1/knowledge/ingest
    Body: {source_type, url_or_path}
    Response: IngestionJob

GET /api/v1/knowledge/search
    Query: query, top_k
    Response: SearchResult[]

GET /api/v1/knowledge/documents
    Query: doc_type, tags[], limit
    Response: Document[]
```

#### 6. LLM Endpoints

```python
POST /api/v1/llm/query
    Body: {query: str, context?: dict}
    Response: {response: str, function_calls: [], citations: []}

POST /api/v1/llm/explain_signal
    Body: {signal_id: str}
    Response: {explanation: str}
```

---

## LLM Integration Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│                    LLM Integration Layer                     │
│                                                               │
│  ┌───────────────┐  ┌───────────────┐  ┌─────────────────┐ │
│  │  Prompt Mgr   │  │  Function Reg │  │  RAG Retriever  │ │
│  │  - Templates  │  │  - Registry   │  │  - Vector Query │ │
│  │  - Variables  │  │  - Validator  │  │  - Reranking    │ │
│  └───────────────┘  └───────────────┘  └─────────────────┘ │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │         LLM Inference Engine (llama.cpp)              │  │
│  │  - Model: Qwen 2.5 7B / LLaMA 3 8B                    │  │
│  │  - Context: 8K tokens                                 │  │
│  │  - Format: JSON function calling                      │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌───────────────┐  ┌───────────────┐  ┌─────────────────┐ │
│  │  Response Gen │  │  Citation Fmt │  │  Error Handler  │ │
│  │  - Formatter  │  │  - References │  │  - Fallbacks    │ │
│  │  - Validator  │  │  - Links      │  │  - Logging      │ │
│  └───────────────┘  └───────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Function Calling Schema

```json
{
  "functions": [
    {
      "name": "run_backtest",
      "description": "Run a backtest for a trading strategy",
      "parameters": {
        "type": "object",
        "properties": {
          "strategy": {"type": "string"},
          "symbols": {"type": "array", "items": {"type": "string"}},
          "start_date": {"type": "string", "format": "date"},
          "end_date": {"type": "string", "format": "date"},
          "params": {"type": "object"}
        },
        "required": ["strategy", "symbols", "start_date"]
      }
    },
    {
      "name": "fetch_data",
      "description": "Fetch market data for symbols",
      "parameters": {
        "type": "object",
        "properties": {
          "symbols": {"type": "array", "items": {"type": "string"}},
          "start_date": {"type": "string", "format": "date"},
          "end_date": {"type": "string", "format": "date"}
        },
        "required": ["symbols"]
      }
    }
    // ... more functions
  ]
}
```

### RAG Pipeline

```
User Query
    ↓
┌─────────────────┐
│ Query Embedding │  (sentence-transformers)
└────────┬────────┘
         ↓
┌─────────────────┐
│ Vector Search   │  (FAISS top-K retrieval)
└────────┬────────┘
         ↓
┌─────────────────┐
│ Reranking       │  (cross-encoder optional)
└────────┬────────┘
         ↓
┌─────────────────┐
│ Context Inject  │  (add to LLM prompt)
└────────┬────────┘
         ↓
┌─────────────────┐
│ LLM Generation  │  (with citations)
└────────┬────────┘
         ↓
    Response
```

---

## Deployment Architecture

### Development Environment

```
┌─────────────────────────────────────────────┐
│          Developer Laptop / Workstation     │
│                                             │
│  ┌──────────────┐      ┌─────────────────┐ │
│  │  Python 3.11 │      │  DuckDB (local) │ │
│  │  virtualenv  │      │  Parquet files  │ │
│  └──────────────┘      └─────────────────┘ │
│                                             │
│  ┌──────────────┐      ┌─────────────────┐ │
│  │  Jupyter     │      │  LLM (llama.cpp)│ │
│  │  Notebooks   │      │  Qwen 7B        │ │
│  └──────────────┘      └─────────────────┘ │
└─────────────────────────────────────────────┘
```

### Production Environment (Option 1: Local Server)

```
┌─────────────────────────────────────────────┐
│         Local Server (Ubuntu 22.04)         │
│         RAM: 64GB | CPU: 16 cores           │
│                                             │
│  ┌────────────────────────────────────────┐ │
│  │           Docker Compose               │ │
│  │  ┌──────────┐  ┌──────────┐           │ │
│  │  │  API     │  │Dashboard │           │ │
│  │  │Container │  │Container │           │ │
│  │  └──────────┘  └──────────┘           │ │
│  │  ┌──────────┐  ┌──────────┐           │ │
│  │  │  Worker  │  │  LLM     │           │ │
│  │  │Container │  │Container │           │ │
│  │  └──────────┘  └──────────┘           │ │
│  └────────────────────────────────────────┘ │
│                                             │
│  ┌────────────────────────────────────────┐ │
│  │          Persistent Storage            │ │
│  │  - /data/market (Parquet)              │ │
│  │  - /data/models (MLflow)               │ │
│  │  - /data/db (DuckDB)                   │ │
│  └────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

### Production Environment (Option 2: Cloud)

```
┌──────────────────────────────────────────────────────────────┐
│                        AWS / GCP / Azure                     │
│                                                              │
│  ┌────────────────────┐       ┌────────────────────────┐   │
│  │  Load Balancer     │──────▶│  API Server (ECS/GKE)  │   │
│  │  (ALB/GCLB)        │       │  - FastAPI             │   │
│  └────────────────────┘       │  - Gunicorn            │   │
│                                └────────────────────────┘   │
│                                                              │
│  ┌────────────────────┐       ┌────────────────────────┐   │
│  │  Streamlit         │       │  Workflow Orchestrator │   │
│  │  (App Service)     │       │  (Prefect Cloud)       │   │
│  └────────────────────┘       └────────────────────────┘   │
│                                                              │
│  ┌────────────────────┐       ┌────────────────────────┐   │
│  │  Object Storage    │       │  Database              │   │
│  │  (S3/GCS/Blob)     │       │  (RDS/CloudSQL)        │   │
│  │  - Parquet files   │       │  - TimescaleDB opt     │   │
│  └────────────────────┘       └────────────────────────┘   │
│                                                              │
│  ┌────────────────────┐       ┌────────────────────────┐   │
│  │  LLM Inference     │       │  Monitoring            │   │
│  │  (GPU instance)    │       │  (Grafana/Prometheus)  │   │
│  │  - Qwen 7B         │       │  - MLflow              │   │
│  └────────────────────┘       └────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

---

## Security & Compliance

### 1. Data Security

- **At Rest**: Encryption for all databases (AES-256)
- **In Transit**: TLS 1.3 for all API communications
- **Credentials**: Stored in AWS Secrets Manager / HashiCorp Vault
- **Backups**: Daily encrypted backups with 30-day retention

### 2. API Security

- **Authentication**: JWT tokens with 1-hour expiry
- **Rate Limiting**: 100 requests/minute per user
- **Input Validation**: Pydantic schemas for all endpoints
- **CORS**: Whitelist allowed origins

### 3. LLM Safety

- **Prompt Injection**: Input sanitization and validation
- **Output Validation**: Schema enforcement for function calls
- **Sandboxing**: New features tested in isolated environment
- **Human Approval**: High-risk actions require confirmation

### 4. Compliance

- **SEBI Regulations**: No insider trading, proper disclosures
- **API ToS**: Respect rate limits and usage policies
- **Data Privacy**: Anonymize personal data, GDPR-compliant
- **Audit Logs**: All user actions and system decisions logged

---

## Performance Considerations

### 1. Database Optimization

- **DuckDB**: Columnar storage, vectorized queries (10x faster than pandas)
- **Parquet**: Compressed, partitioned by date and symbol
- **Indexes**: B-tree indexes on (symbol, timestamp)
- **Caching**: Redis for frequently accessed data

### 2. ML Inference

- **Batch Prediction**: Process 100+ symbols in <10 seconds
- **Model Quantization**: INT8 for faster inference (minimal accuracy loss)
- **Feature Caching**: Pre-compute indicators for next-day signals
- **Parallel Processing**: Multi-core for backtesting

### 3. LLM Inference

- **Model Size**: 7B parameters (balanced speed vs capability)
- **Quantization**: Q4_K_M (4-bit) for 3x speed improvement
- **Context Management**: Sliding window for long conversations
- **Batch Processing**: Multiple queries in single inference

### 4. Scalability

- **Horizontal**: Stateless API servers (scale with demand)
- **Vertical**: Database on high-memory instance
- **Async**: FastAPI async endpoints for I/O-bound tasks
- **Queues**: Celery for long-running jobs (backtests, training)

---

## Monitoring & Observability

### Metrics to Track

**System Health**:
- API response time (p50, p95, p99)
- Database query latency
- LLM inference time
- Memory & CPU utilization

**Data Quality**:
- Missing data points per symbol
- Data freshness (lag from market close)
- Outlier detection alerts

**Model Performance**:
- Prediction accuracy (daily)
- Calibration drift
- Feature importance shifts
- Signal win rate

**Business Metrics**:
- Signals generated per day
- Backtest requests per week
- LLM query success rate
- User engagement (dashboard views)

---

**Document Version**: 1.0
**Last Updated**: 2025-11-03
