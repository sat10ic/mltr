# LLM-Integrated ML Trading Research & Intelligence System
## Project Plan v2.0

---

## Executive Summary

A self-learning, multi-source AI framework for the Indian stock market (NSE/BSE cash segment) that combines:
- Classical ML for price/volume prediction
- NLP for news/social sentiment analysis
- Local LLM as intelligent research orchestrator
- Continuous learning from market data and research papers

**Goal**: Deliver transparent, data-driven trading signals that improve over time without compromising model integrity.

---

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                          │
│  ┌──────────────────────┐    ┌─────────────────────────┐       │
│  │  Streamlit Dashboard │    │   FastAPI REST API      │       │
│  └──────────────────────┘    └─────────────────────────┘       │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│              LLM ORCHESTRATION & RESEARCH LAYER                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Local LLM (Qwen/LLaMA/Mistral)                          │  │
│  │  - Natural language query interface                       │  │
│  │  - Experiment orchestration                               │  │
│  │  - Signal explanation generation                          │  │
│  │  - Research paper ingestion (RAG)                         │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                  INTELLIGENCE & LEARNING LAYER                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐ │
│  │  ML Engine      │  │  Signal Gen     │  │  Feedback Loop │ │
│  │  - Batch Models │  │  - Risk Mgmt    │  │  - Outcome Log │ │
│  │  - Online Learn │  │  - Position Size│  │  - Meta-Learn  │ │
│  └─────────────────┘  └─────────────────┘  └────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                    FEATURE ENGINEERING LAYER                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Technical Features  │  Sentiment Features  │  Regime    │   │
│  │  - Indicators        │  - News tone         │  - Market  │   │
│  │  - Price patterns    │  - Social volume     │  - Sector  │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                               │
│  ┌───────────────┐  ┌─────────────┐  ┌────────────────────┐   │
│  │  Market Data  │  │  News/Social│  │  Knowledge Base    │   │
│  │  - OHLCV      │  │  - RSS/API  │  │  - Research Papers │   │
│  │  - Indicators │  │  - Twitter  │  │  - GitHub Repos    │   │
│  │  - DuckDB     │  │  - Reddit   │  │  - Vector DB (RAG) │   │
│  └───────────────┘  └─────────────┘  └────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Modules

### 1. Data Layer (`src/data/`)

**Purpose**: Acquire, store, and serve market and alternative data

#### 1.1 Market Data Module
- **Sources**: Dhan API, NSE official, Yahoo Finance fallback
- **Coverage**: Nifty 500, sectoral indices, FII/DII flows
- **Frequency**: Minute bars (intraday) + EOD historical
- **Storage**: Parquet files + DuckDB for queries
- **Features**:
  - Historical data downloader with retry logic
  - Live data streaming during market hours
  - Data quality checks and gap filling
  - Symbol universe management

#### 1.2 News & Social Data Module
- **Sources**:
  - News: NewsAPI, RSS feeds, GDELT
  - Social: Twitter/X (snscrape), Reddit (PRAW), Telegram
  - Optional: Google Trends, alternative datasets
- **Processing**:
  - Deduplication and timestamp normalization
  - Entity extraction (company names, sectors)
  - Credibility scoring by source
- **Storage**: DuckDB + optional ElasticSearch for text search

#### 1.3 Reference Data Module
- Sector classifications
- Market holidays calendar
- Corporate actions (splits, bonuses, dividends)
- Liquidity tiers

---

### 2. Feature Engineering Layer (`src/features/`)

**Purpose**: Transform raw data into predictive signals

#### 2.1 Technical Features
- **Momentum**: RSI, MACD, Stochastic, Rate of Change
- **Trend**: Moving averages (SMA, EMA, Hull), ADX, Supertrend
- **Volatility**: Bollinger Bands, ATR, Keltner Channel
- **Volume**: OBV, VWAP, Volume Rate of Change, Delivery %
- **Custom**: Gap analysis, candlestick patterns, support/resistance levels

#### 2.2 Sentiment Features
- `news_volume(symbol, window)`: Article count per period
- `weighted_sentiment(symbol, window)`: Reach-weighted sentiment score
- `topic_strength(symbol, topic)`: Relevance to trending themes
- `surprise_score(symbol)`: Deviation from baseline narrative
- `sector_tone(sector)`: Aggregate sector sentiment
- `macro_sentiment()`: Overall market mood

#### 2.3 Meta Features
- **Market Regime**: Bull/Bear/Sideways classification
- **Sector Rotation**: Relative sector strength
- **Liquidity**: Average volume, bid-ask spread tier
- **Correlations**: Stock vs sector, stock vs Nifty

#### 2.4 Feature Store
- Centralized registry with metadata
- Versioning and lineage tracking
- Lag-safe computation (no future leak)
- Efficient caching for repeated calculations

---

### 3. Machine Learning Engine (`src/ml/`)

**Purpose**: Train, calibrate, and serve predictive models

#### 3.1 Batch Models (EOD Training)
- **Algorithms**: RandomForest, XGBoost, LightGBM, ElasticNet
- **Targets**:
  - Binary: Will price rise >X% in N days?
  - Regression: Expected N-day return
  - Triple-barrier: Profit/stop/timeout labeling
- **Validation**: Time-series cross-validation with purging/embargo
- **Calibration**: Platt scaling or isotonic regression for probability outputs

#### 3.2 Online Models (Intraday Adaptation)
- **Framework**: River library for incremental learning
- **Updates**: Minute-by-minute feature and prediction updates
- **Use case**: Adapt to intraday regime shifts

#### 3.3 Model Registry
- MLflow integration for experiment tracking
- Model versioning and A/B testing
- Performance metrics dashboard
- Automatic rollback on degradation

---

### 4. Signal Generation & Risk Engine (`src/signals/`)

**Purpose**: Convert predictions to actionable trades with risk controls

#### 4.1 Signal Generation
- **Input**: Calibrated probabilities from ML models
- **Thresholds**: Dynamic based on volatility and regime
- **Filters**:
  - Minimum liquidity requirement
  - Sector exposure limits
  - Sentiment-price alignment check
- **Confidence Scoring**: Combine ML probability + sentiment modifier

#### 4.2 Risk Management
- **Position Sizing**: Volatility-adjusted (ATR-based)
- **Risk Per Trade**: Max 1% of capital (configurable)
- **Stop Loss**: ATR-multiple or swing low/high
- **Take Profit**: Risk-reward ratio (1:2 minimum)
- **Trailing Stop**: EMA crossover or ATR-trail

#### 4.3 Signal Card Format
```json
{
  "symbol": "RELIANCE",
  "action": "BUY",
  "entry_price": 2450.00,
  "stop_loss": 2400.00,
  "target": 2550.00,
  "risk_reward": 2.0,
  "confidence": 0.72,
  "reasoning": "Bullish RSI divergence + positive sector sentiment",
  "ml_probability": 0.68,
  "sentiment_boost": 0.04,
  "timestamp": "2025-11-03T09:30:00"
}
```

---

### 5. Backtesting & Research Lab (`src/backtest/`)

**Purpose**: Rigorous testing and indicator research

#### 5.1 Backtesting Engine
- **Framework**: vectorbt / vectorbtpro
- **Methodology**: Walk-forward analysis with purged CV
- **Metrics**: Sharpe, Sortino, CAGR, MaxDD, Win Rate, Profit Factor
- **Slippage & Costs**: Realistic modeling (0.05% per trade)

#### 5.2 Indicator League Table
- **Function**: Test 100+ indicator combinations
- **Output**: Ranked performance table by Sharpe and robustness
- **Refresh**: Weekly or on-demand
- **Storage**: Results database for historical comparison

#### 5.3 Ablation Testing
- Remove one feature at a time
- Measure impact on out-of-sample performance
- Auto-prune redundant or harmful features

#### 5.4 Monte Carlo Simulation
- Permutation testing for statistical significance
- Robustness checks against random strategies

---

### 6. LLM Orchestration Layer (`src/llm/`)

**Purpose**: Natural language interface and intelligent automation

#### 6.1 Core Capabilities
- **Query Interface**: "Show me best momentum stocks in IT sector"
- **Experiment Runner**: "Backtest RSI 14 on Nifty 200 since 2020"
- **Signal Explainer**: Convert ML output to human language
- **Anomaly Detector**: Flag unusual market behavior
- **Research Assistant**: Summarize papers, suggest features

#### 6.2 Local LLM Setup
- **Models**: Qwen 2.5 (7B/14B), LLaMA 3, Mistral 7B
- **Inference**: llama.cpp, Ollama, or vLLM
- **Fine-tuning**: LoRA on instruction templates (NOT price data)
- **Context**: System prompts with market domain knowledge

#### 6.3 Function Calling
- LLM outputs structured JSON for tool invocation
- Available tools:
  - `fetch_data(symbol, start, end)`
  - `run_backtest(strategy, params)`
  - `generate_signals(date)`
  - `explain_signal(signal_id)`
  - `ingest_paper(pdf_path)`
  - `search_knowledge_base(query)`

---

### 7. Knowledge Ingestion & RAG (`src/knowledge/`)

**Purpose**: Learn from external research safely

#### 7.1 Data Sources
- Research papers (PDF)
- GitHub repositories (trading strategies, ML tools)
- Technical blogs and Jupyter notebooks

#### 7.2 Ingestion Pipeline
1. **Extract**: PyMuPDF for PDFs, GitHub API for repos
2. **Chunk**: Semantic chunking (512 tokens with overlap)
3. **Embed**: sentence-transformers (all-MiniLM-L6-v2)
4. **Store**: FAISS or Milvus vector database
5. **Index**: Metadata tagging (author, date, topic)

#### 7.3 Retrieval-Augmented Generation (RAG)
- LLM queries vector DB for relevant context
- Retrieved chunks injected into prompt
- Citations included in LLM response

#### 7.4 Safety Mechanisms
- **Sandboxing**: New features tested in isolated environment
- **Canary Testing**: Small allocation before full deployment
- **Human Approval**: Statistical significance + manual review required
- **Version Control**: All experiments logged in Git + MLflow

---

### 8. Feedback & Self-Learning (`src/feedback/`)

**Purpose**: Learn from actual trade outcomes

#### 8.1 Trade Logging
- Signal → Execution → Outcome tracking
- Realized return vs predicted return
- Stop loss / take profit hit rate
- Holding period analysis

#### 8.2 Meta-Learning
- **Periodic Review**: Weekly analysis of prediction accuracy
- **Threshold Tuning**: Adjust entry/exit thresholds based on outcomes
- **Feature Reweighting**: Boost features that improve outcomes
- **Regime Detection**: Learn which market conditions favor each strategy

#### 8.3 Feedback Loop
```
Signal Generated → Trade Executed → Outcome Measured
                                         ↓
                    Feature Weights ← Meta-Learner
                                         ↓
                    Improved Predictions (next cycle)
```

---

### 9. Scheduling & Orchestration (`src/workflow/`)

**Purpose**: Automate daily/intraday workflows

#### 9.1 Schedule
| Time (IST)      | Task                                    |
|-----------------|-----------------------------------------|
| 06:00 - 08:45   | Data sync, symbol refresh, pre-market prep |
| 09:15 - 15:30   | Intraday streaming, online model updates   |
| 15:30 - 16:00   | EOD cleanup, log trades, update feedback   |
| 16:00 - 19:00   | Batch retraining, calibration, signal gen  |
| Weekly (Sunday) | Indicator league, ablation tests, reports  |

#### 9.2 Workflow Engine
- **Options**: Airflow, Prefect, or Dagster
- **DAG Structure**: Clear dependencies between tasks
- **Error Handling**: Retry logic, alerts on failure
- **Monitoring**: Grafana dashboards for pipeline health

---

### 10. API & Dashboard (`src/api/` & `src/dashboard/`)

**Purpose**: User interface for interaction and monitoring

#### 10.1 FastAPI Endpoints
- `GET /signals/today` - Current watchlist
- `POST /backtest` - Run custom backtest
- `GET /indicators/league` - Indicator performance table
- `GET /trades/review` - Post-trade analysis
- `POST /knowledge/ingest` - Upload PDF/GitHub URL
- `GET /health` - System status

#### 10.2 Streamlit Dashboard
**Tabs**:
1. **Signals Today**: Live watchlist with cards
2. **Backtesting Lab**: Interactive strategy tester
3. **Indicator League**: Visual performance rankings
4. **Post-Trade Review**: Outcome analysis
5. **Research Lab**: RAG search and paper ingestion
6. **Chat**: Natural language LLM interface

---

## Technology Stack

### Core Languages & Frameworks
- **Python 3.11+**: Primary development language
- **FastAPI**: REST API framework
- **Streamlit**: Dashboard UI

### Data Storage
- **DuckDB**: Primary analytical database
- **Parquet**: Time-series data storage
- **TimescaleDB** (optional): SQL time-series queries
- **FAISS/Milvus**: Vector database for RAG

### Machine Learning
- **scikit-learn**: Classical ML algorithms
- **XGBoost / LightGBM**: Gradient boosting
- **River**: Online/incremental learning
- **Optuna**: Hyperparameter optimization

### Backtesting & Analysis
- **vectorbt / vectorbtpro**: High-performance backtesting
- **pandas / polars**: Data manipulation
- **numpy**: Numerical computing

### NLP & Sentiment
- **spaCy**: NLP processing
- **transformers**: Sentiment analysis models
- **sentence-transformers**: Text embeddings
- **BERTopic**: Topic modeling

### LLM Integration
- **llama.cpp / Ollama**: Local LLM inference
- **LangChain**: LLM orchestration framework
- **llama-index**: RAG framework

### Data Acquisition
- **yfinance**: Fallback market data
- **beautifulsoup4 / playwright**: Web scraping
- **snscrape**: Twitter scraping
- **praw**: Reddit API
- **newspaper3k**: News article extraction

### Workflow & Monitoring
- **Prefect / Airflow**: Workflow orchestration
- **MLflow**: Experiment tracking
- **Grafana / Prometheus**: Monitoring
- **Sentry**: Error tracking

---

## Safety & Governance

### 1. Data Integrity
- ✅ No future data leakage (strict time-aware features)
- ✅ Consistent data quality checks
- ✅ Audit trail for all data modifications

### 2. Model Safety
- ✅ Walk-forward validation (never train on future)
- ✅ Probability calibration (realistic confidence)
- ✅ Performance degradation alerts

### 3. Feature Gating
- ✅ All new features start in "candidate" mode
- ✅ Ablation test required for promotion
- ✅ Statistical significance threshold (>5% Sharpe improvement)

### 4. Human-in-the-Loop
- ✅ LLM suggestions require approval before deployment
- ✅ Manual review of high-impact changes
- ✅ Override capability for system-generated trades

### 5. Ethical & Legal
- ✅ Respect API rate limits and ToS
- ✅ No insider information usage
- ✅ Anonymize sensitive data
- ✅ Comply with SEBI regulations

### 6. Version Control
- ✅ Git for code versioning
- ✅ MLflow for model versioning
- ✅ Feature store for feature lineage
- ✅ Reproducible experiments

---

## Key Performance Indicators (KPIs)

### Model Performance
- **Sharpe Ratio**: Target > 1.5 (annualized)
- **CAGR**: Target > 15%
- **Max Drawdown**: Keep < 15%
- **Win Rate**: Target > 55%
- **Profit Factor**: Target > 1.5

### Operational Metrics
- **Data Freshness**: < 5 min lag during market hours
- **Prediction Latency**: < 1 second per symbol
- **System Uptime**: > 99% during market hours
- **Backtest Speed**: Full walk-forward in < 10 minutes

### Learning Metrics
- **Prediction Calibration**: Brier score < 0.20
- **Feature Stability**: Low turnover in top features
- **Feedback Loop**: 10% improvement in signal quality per quarter

---

## Risk Management

### Portfolio Level
- Max 10 concurrent positions
- Max 30% allocation to single sector
- Max 3% allocation per stock
- Daily loss limit: 2% of capital

### Position Level
- Max risk per trade: 1% of capital
- Minimum risk-reward: 1:2
- Volatility-based position sizing
- Trailing stop activation at +1R

### System Level
- Kill switch for runaway losses (-5% day)
- Manual override capability
- Fallback to cash on data feed failure
- Backup data sources

---

## Success Metrics

### Phase 1 (Foundation) - Weeks 1-8
- ✅ Data pipeline operational for 50+ stocks
- ✅ 20+ technical indicators computed correctly
- ✅ Basic ML model with Sharpe > 0.5 in backtest

### Phase 2 (Intelligence) - Weeks 9-16
- ✅ Sentiment analysis integrated
- ✅ LLM can generate backtests via natural language
- ✅ Signal generation with risk management live

### Phase 3 (Evolution) - Weeks 17-24
- ✅ RAG knowledge base with 50+ papers
- ✅ Feedback loop improving calibration by 10%
- ✅ Indicator league ranking 100+ combinations

### Phase 4 (Production) - Weeks 25-32
- ✅ Live paper trading for 1 month
- ✅ Streamlit dashboard fully functional
- ✅ Automated daily workflow running reliably

---

## Next Steps

1. **Review & Approve**: Stakeholder review of this plan
2. **Environment Setup**: Python environment, dependencies, API keys
3. **Phase 1 Kickoff**: Data layer implementation (see ROADMAP.md)
4. **Weekly Syncs**: Progress review and adjustments

---

**Document Version**: 2.0
**Last Updated**: 2025-11-03
**Status**: Planning Phase
**Owner**: Development Team
