# Runtime & Infrastructure Guide

## Overview

This document covers resource requirements, scaling considerations, and infrastructure setup for the MLTR system.

---

## Resource Requirements

### Development Environment

**Minimum:**
- CPU: 4 cores
- RAM: 8GB
- Storage: 50GB SSD
- Network: Stable internet for data fetching

**Recommended:**
- CPU: 8 cores
- RAM: 16GB
- Storage: 100GB SSD
- GPU: Optional (for LLM inference acceleration)

### Production Environment

**API Server:**
- CPU: 8-16 cores
- RAM: 32GB
- Storage: 200GB SSD (for databases)
- Network: Low latency for market data

**Worker Nodes (for backtesting/training):**
- CPU: 16+ cores
- RAM: 64GB
- Storage: 500GB SSD
- GPU: Optional (speeds up training 2-3x)

**LLM Inference:**
- CPU: 8 cores OR
- GPU: 8GB VRAM (RTX 3060 Ti / A4000)
- RAM: 16GB
- Storage: 50GB (for model files)

---

## Streaming Components

### News Scraping (Real-time)

#### Without Message Queue (Simple)

```python
# Polling-based scraper
import time
from src.data.news.scrapers import RSSFeedScraper

scraper = RSSFeedScraper()

while True:
    articles = scraper.fetch_recent(minutes=5)
    if articles:
        process_articles(articles)
    time.sleep(300)  # Poll every 5 minutes
```

**Resource Usage:**
- CPU: ~5-10% (single core)
- RAM: ~100-200MB
- Network: ~1-5 MB/hour

#### With Redis (Medium Scale)

```python
# Producer
import redis
import json

r = redis.Redis(host='localhost', port=6379)

while True:
    articles = scraper.fetch_recent()
    for article in articles:
        r.lpush('news_queue', json.dumps(article))
    time.sleep(60)

# Consumer
while True:
    article_json = r.brpop('news_queue', timeout=5)
    if article_json:
        article = json.loads(article_json[1])
        analyze_sentiment(article)
```

**Redis Requirements:**
- RAM: 512MB - 2GB (depending on queue size)
- Storage: Minimal (data in memory)

#### With Kafka (High Scale)

When to use:
- Processing >1000 articles/hour
- Multiple consumers
- Need replay capability
- Distributed processing

```python
from kafka import KafkaProducer, KafkaConsumer

# Producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

while True:
    articles = scraper.fetch_recent()
    for article in articles:
        producer.send('news_topic', json.dumps(article).encode())
    time.sleep(60)

# Consumer
consumer = KafkaConsumer(
    'news_topic',
    bootstrap_servers=['localhost:9092'],
    group_id='sentiment_analyzer'
)

for message in consumer:
    article = json.loads(message.value)
    analyze_sentiment(article)
```

**Kafka Requirements:**
- CPU: 2-4 cores
- RAM: 4-8GB
- Storage: 100GB+ (for retention)

---

### Minute-Bar Data (Intraday)

#### Polling Approach (Simple)

```python
# Poll every minute during market hours
from datetime import datetime
import time

def is_market_hours():
    now = datetime.now()
    return (
        now.hour >= 9 and now.minute >= 15 and
        now.hour < 15 and now.minute < 30 and
        now.weekday() < 5  # Monday-Friday
    )

while True:
    if is_market_hours():
        # Fetch minute bar for watchlist
        bars = fetch_minute_bars(watchlist)
        update_features(bars)
        generate_intraday_signals(bars)

    time.sleep(60)  # Wait 1 minute
```

**Resource Usage:**
- CPU: ~10-20% during market hours
- RAM: ~500MB for 100 symbols
- Network: ~10 MB/hour

#### WebSocket Approach (Real-time)

```python
import websocket
import json

def on_message(ws, message):
    """Handle incoming tick data."""
    tick = json.loads(message)
    update_minute_bar(tick)

ws = websocket.WebSocketApp(
    "wss://api.example.com/stream",
    on_message=on_message
)

ws.run_forever()
```

**Scaling Considerations:**

| Symbols | CPU | RAM | Network |
|---------|-----|-----|---------|
| 50 | 1 core | 512MB | 5 MB/hour |
| 100 | 2 cores | 1GB | 10 MB/hour |
| 500 | 4 cores | 4GB | 50 MB/hour |
| 1000+ | 8+ cores | 8GB+ | 100 MB/hour |

---

## Database Scaling

### DuckDB (Single Node)

**Good for:**
- Up to 1TB data
- Single server deployment
- Analytical queries
- Development/testing

**Limits:**
- No distributed queries
- Single-writer (multiple readers OK)
- All data must fit on one machine

**Optimization:**
```python
import duckdb

conn = duckdb.connect('market.db')

# Increase memory limit
conn.execute("SET memory_limit='16GB'")

# Enable parallel query execution
conn.execute("SET threads TO 8")

# Use Parquet partitioning
conn.execute("""
    CREATE TABLE ohlcv AS
    SELECT * FROM read_parquet('data/ohlcv/**/*.parquet', hive_partitioning=1)
""")
```

### TimescaleDB (When to Scale)

**Consider when:**
- Data > 1TB
- Need real-time ingestion + queries
- Want time-series specific features (continuous aggregates)
- Multiple concurrent writers

**Setup:**
```sql
-- Create hypertable
CREATE TABLE ohlcv (
    symbol VARCHAR(20),
    timestamp TIMESTAMPTZ NOT NULL,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume BIGINT
);

SELECT create_hypertable('ohlcv', 'timestamp');

-- Create continuous aggregate (pre-computed hourly bars)
CREATE MATERIALIZED VIEW ohlcv_1h
WITH (timescaledb.continuous) AS
SELECT
    symbol,
    time_bucket('1 hour', timestamp) AS hour,
    first(open, timestamp) AS open,
    max(high) AS high,
    min(low) AS low,
    last(close, timestamp) AS close,
    sum(volume) AS volume
FROM ohlcv
GROUP BY symbol, hour;
```

**Resource Requirements:**
- CPU: 8+ cores
- RAM: 32GB+ (higher for in-memory queries)
- Storage: SSD recommended (10x faster than HDD)

---

## LLM Inference

### CPU Inference (llama.cpp)

**Model Size vs Performance:**

| Model | Quantization | RAM | CPU Speed (tokens/sec) | Quality |
|-------|--------------|-----|------------------------|---------|
| Qwen 2.5 7B | Q4_K_M | 4GB | 8-15 | Good |
| Qwen 2.5 7B | Q5_K_M | 5GB | 6-12 | Better |
| Qwen 2.5 7B | Q8_0 | 8GB | 4-8 | Best |
| LLaMA 3 8B | Q4_K_M | 5GB | 7-14 | Good |

**CPU Optimization:**
```bash
# Build with optimizations
cd llama.cpp
make LLAMA_OPENBLAS=1 LLAMA_NATIVE=1

# Run with multiple threads
./main -m model.gguf -t 8 -c 4096 -p "Your prompt"
```

**Python API:**
```python
from llama_cpp import Llama

llm = Llama(
    model_path="models/qwen2.5-7b-q4_k_m.gguf",
    n_ctx=4096,       # Context window
    n_threads=8,      # CPU threads
    n_batch=512,      # Batch size
)

response = llm("Explain RSI indicator")
```

### GPU Inference

**Performance Boost:** 3-10x faster than CPU

**Requirements:**
- CUDA-capable GPU (NVIDIA)
- 8GB+ VRAM for 7B models
- CUDA Toolkit installed

**Setup:**
```bash
# Install llama-cpp-python with CUDA
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python

# Use GPU layers
llm = Llama(
    model_path="model.gguf",
    n_gpu_layers=35,  # Offload layers to GPU
    n_ctx=4096
)
```

**Expected Speed (7B model, RTX 3080):**
- ~50-80 tokens/sec (vs 8-15 on CPU)

---

## Workflow Orchestration

### Prefect (Recommended)

**Why Prefect:**
- Python-native (no YAML/XML)
- Easy local development
- Good observability
- Cloud offering available

**Resource Usage:**
- Prefect Server: 1 core, 1GB RAM
- Per flow run: Minimal overhead

**Example DAG:**
```python
from prefect import flow, task
from datetime import timedelta

@task(retries=3, retry_delay_seconds=60)
def fetch_eod_data():
    """Fetch end-of-day data."""
    return fetch_ohlcv(symbols=watchlist, date=today)

@task
def compute_features(data):
    """Compute technical indicators."""
    return calculate_all_features(data)

@task
def train_models(features):
    """Retrain ML models."""
    return train_walkforward(features)

@task
def generate_signals(models):
    """Generate next-day signals."""
    return generate_signal_cards(models)

@flow(name="eod_pipeline")
def eod_workflow():
    data = fetch_eod_data()
    features = compute_features(data)
    models = train_models(features)
    signals = generate_signals(models)
    return signals

# Schedule
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule

deployment = Deployment.build_from_flow(
    flow=eod_workflow,
    name="eod_daily",
    schedule=CronSchedule(cron="0 16 * * 1-5", timezone="Asia/Kolkata")
)

deployment.apply()
```

### Airflow (Alternative)

**When to use:**
- Need battle-tested solution
- Complex DAG dependencies
- Large team familiar with Airflow

**Resource Usage:**
- Airflow components: 4GB+ RAM
- Webserver + Scheduler + Workers
- Requires PostgreSQL/MySQL

**Trade-offs vs Prefect:**
- ✅ More mature, larger community
- ✅ Rich ecosystem of operators
- ❌ Heavier resource footprint
- ❌ Steeper learning curve
- ❌ More operational complexity

---

## Scaling Strategies

### Horizontal Scaling (Multiple Machines)

```
┌────────────────┐     ┌─────────────────┐
│   API Server   │────▶│  Load Balancer  │
│  (Stateless)   │     └─────────────────┘
└────────────────┘            │
                              │
      ┌───────────────────────┼───────────────────────┐
      │                       │                       │
┌─────▼─────┐         ┌───────▼──────┐        ┌──────▼─────┐
│ Worker 1  │         │  Worker 2    │        │  Worker 3  │
│ (Backtest)│         │  (Training)  │        │  (Signals) │
└───────────┘         └──────────────┘        └────────────┘
```

**When to scale:**
- API server at >70% CPU
- Backtests taking >30 minutes
- Queue backlog growing

### Vertical Scaling (Bigger Machine)

**When to scale up:**
- Single large backtest (parallelization limited)
- In-memory datasets approaching RAM limit
- Single-threaded bottlenecks (DuckDB queries)

**Cost Comparison:**

| Approach | Cost | Setup Complexity | When to Use |
|----------|------|------------------|-------------|
| Vertical | $$ | Low | Development, prototyping |
| Horizontal | $$$ | High | Production, high availability |

---

## Monitoring & Alerts

### System Metrics

```python
# Prometheus metrics
from prometheus_client import Counter, Histogram, Gauge

# API metrics
api_requests = Counter('api_requests_total', 'API requests')
api_latency = Histogram('api_latency_seconds', 'API latency')

# Data metrics
data_lag = Gauge('data_lag_minutes', 'Data freshness lag')
prediction_count = Counter('predictions_total', 'Predictions generated')

# Resource metrics
cpu_usage = Gauge('cpu_usage_percent', 'CPU usage')
memory_usage = Gauge('memory_usage_mb', 'Memory usage')
```

### Critical Alerts

1. **Data Feed Down**
   - No data for >10 minutes during market hours
   - Alert: Slack/Email immediately

2. **Model Prediction Failure**
   - Unable to generate signals
   - Alert: Within 5 minutes

3. **High Error Rate**
   - >5% of API requests failing
   - Alert: Within 2 minutes

4. **Resource Exhaustion**
   - RAM >90% for >5 minutes
   - CPU >95% for >5 minutes
   - Disk >85%

---

## Backup & Disaster Recovery

### Data Backup

```bash
# Daily backup script
#!/bin/bash

DATE=$(date +%Y%m%d)
BACKUP_DIR=/backups/$DATE

# Backup databases
duckdb market.db ".backup $BACKUP_DIR/market_$DATE.db"
duckdb news.db ".backup $BACKUP_DIR/news_$DATE.db"

# Backup models
tar -czf $BACKUP_DIR/models_$DATE.tar.gz data/models/

# Backup to cloud
aws s3 sync $BACKUP_DIR s3://mltr-backups/$DATE/

# Cleanup old backups (keep 30 days)
find /backups -mtime +30 -delete
```

### Recovery Time Objectives (RTO)

| Component | Target RTO | Procedure |
|-----------|------------|-----------|
| API Server | 5 minutes | Restart from Docker image |
| Database | 30 minutes | Restore from backup |
| Models | 15 minutes | Download from S3 |
| Full System | 1 hour | Automated deployment script |

---

## Cost Estimation

### Cloud Hosting (AWS/GCP/Azure)

**Development (Single instance):**
- Compute: t3.xlarge (4 vCPU, 16GB) ~ $120/month
- Storage: 100GB SSD ~ $10/month
- Data transfer: ~$5/month
- **Total: ~$135/month**

**Production (HA setup):**
- API servers (2x t3.large): $140/month
- Worker nodes (2x c5.2xlarge): $490/month
- Database (r5.xlarge): $175/month
- Load balancer: $20/month
- Storage (500GB): $50/month
- Data transfer: $20/month
- **Total: ~$895/month**

### On-Premise

**Initial Investment:**
- Server (32GB RAM, 16 cores): $2000-3000
- Storage (1TB SSD): $200
- UPS: $200
- **Total: ~$2400-3400**

**Monthly Costs:**
- Electricity (~200W × 730h): $20/month
- Internet (static IP): $50/month
- **Total: ~$70/month**

**Break-even:** ~27-40 months

---

## Quick Reference

### Port Assignments

| Service | Port | Purpose |
|---------|------|---------|
| FastAPI | 8000 | REST API |
| Streamlit | 8501 | Dashboard |
| MLflow | 5000 | Experiment tracking |
| Prometheus | 9090 | Metrics |
| Grafana | 3000 | Visualization |
| Redis | 6379 | Caching/Queue |
| PostgreSQL | 5432 | Database (if used) |

### Health Check Endpoints

```bash
# API health
curl http://localhost:8000/health

# Database connection
curl http://localhost:8000/health/database

# Model loaded
curl http://localhost:8000/health/model
```

---

For more details:
- [ARCHITECTURE.md](../ARCHITECTURE.md)
- [DEVELOPMENT_GUIDE.md](../DEVELOPMENT_GUIDE.md)
- [Prefect Docs](https://docs.prefect.io/)
