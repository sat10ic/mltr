# MLTR - ML Trading Research & Intelligence System

**A self-learning, multi-source AI framework for the Indian stock market**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Overview

MLTR is an adaptive, data-driven platform built to continuously study the Indian equity market (NSE/BSE, cash segment) across price, volume, sentiment, and narrative data. It combines:

- **Classical Machine Learning** for price/indicator-based predictions
- **Natural Language Processing** for news, social, and macro narrative analysis
- **Local LLM** acting as an intelligent research agent that orchestrates, explains, and evolves the system

The result is a self-improving trading intelligence engine that learns from price action, social narratives, and new research — delivering transparent, data-driven buy/sell signals.

---

## Features

✨ **Multi-Dimensional Learning**
- Price action + technical indicators
- News sentiment + social media analysis
- Market regime detection
- Sector rotation signals

🧠 **AI-Powered Intelligence**
- Local LLM for natural language queries
- Automatic signal explanation generation
- Research paper ingestion via RAG
- Experiment orchestration

📊 **Robust Backtesting**
- Walk-forward validation
- 100+ indicator performance league
- Ablation testing framework
- Monte Carlo simulation

🔄 **Continuous Learning**
- Daily batch retraining
- Intraday online learning
- Feedback loop from trade outcomes
- Meta-learning for threshold optimization

🛡️ **Safety First**
- No future data leakage
- Statistical significance requirements
- Human-in-the-loop approval
- Feature gating and canary testing

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  USER INTERFACE                              │
│        Streamlit Dashboard  |  FastAPI REST API             │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│           LLM ORCHESTRATION (Local Qwen/LLaMA)              │
│     Natural Language → Function Calls → Explanations        │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│         INTELLIGENCE LAYER                                   │
│   ML Models | Signal Gen | Risk Mgmt | Feedback Loop        │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│         FEATURE ENGINEERING                                  │
│   Technical | Sentiment | Regime | Meta Features            │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│         DATA LAYER                                           │
│   Market Data | News/Social | Knowledge Base (RAG)          │
│   DuckDB | Parquet | FAISS Vector Store                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
mltr/
├── src/
│   ├── data/                    # Data acquisition & storage
│   │   ├── market/             # OHLCV data fetchers
│   │   ├── news/               # News & social media scrapers
│   │   └── reference/          # Sector, calendar, corporate actions
│   ├── features/               # Feature engineering
│   │   ├── technical/          # Technical indicators
│   │   ├── sentiment/          # NLP & sentiment analysis
│   │   └── store/              # Feature store & registry
│   ├── ml/                     # Machine learning
│   │   ├── models/             # RandomForest, XGBoost, LightGBM
│   │   ├── online/             # River-based online learning
│   │   └── labeling/           # Target generation
│   ├── signals/                # Signal generation & risk management
│   ├── backtest/               # Backtesting & indicator league
│   ├── llm/                    # LLM orchestration & RAG
│   ├── knowledge/              # PDF/GitHub ingestion
│   ├── feedback/               # Trade logging & meta-learning
│   ├── workflow/               # Airflow/Prefect DAGs
│   ├── api/                    # FastAPI endpoints
│   └── dashboard/              # Streamlit UI
├── tests/                      # Unit, integration, e2e tests
├── configs/                    # YAML/TOML configurations
├── data/                       # Local data storage
│   ├── raw/                    # Raw downloaded data
│   ├── processed/              # Cleaned & featured data
│   ├── models/                 # Trained model artifacts
│   └── outputs/                # Signals, reports, logs
├── notebooks/                  # Jupyter notebooks for research
├── docs/                       # Additional documentation
├── scripts/                    # Utility scripts
├── PROJECT_PLAN.md             # Detailed project plan
├── ROADMAP.md                  # Implementation roadmap
├── ARCHITECTURE.md             # Technical architecture details
├── requirements.txt            # Python dependencies
├── pyproject.toml              # Project metadata
└── README.md                   # This file
```

---

## Quick Start

### Prerequisites

- Python 3.11 or higher
- 8GB+ RAM (16GB recommended)
- 100GB+ storage for data
- (Optional) GPU for LLM inference

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/mltr.git
cd mltr
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up configuration**
```bash
cp configs/config.example.yaml configs/config.yaml
# Edit config.yaml with your API keys and preferences
```

5. **Download initial data**
```bash
python scripts/setup_data.py --symbols NIFTY500 --days 730
```

---

## Usage

### 1. Data Pipeline

**Download historical data:**
```bash
python -m src.data.market.fetcher --universe nifty500 --start 2023-01-01
```

**Scrape news and sentiment:**
```bash
python -m src.data.news.scrapers --sources newsapi,rss --date today
```

### 2. Feature Engineering

**Compute technical indicators:**
```bash
python -m src.features.technical.compute --symbols RELIANCE,TCS --indicators all
```

### 3. Model Training

**Train ML models:**
```bash
python -m src.ml.training --config configs/model_config.yaml --walkforward
```

### 4. Generate Signals

**Run signal generation:**
```bash
python -m src.signals.generator --date 2025-11-03 --min-confidence 0.6
```

### 5. Backtesting

**Run backtest:**
```bash
python -m src.backtest.engine --strategy momentum_v1 --start 2023-01-01 --end 2024-12-31
```

### 6. Dashboard

**Launch Streamlit dashboard:**
```bash
streamlit run src/dashboard/app.py
```

**Launch API server:**
```bash
uvicorn src.api.main:app --reload --port 8000
```

### 7. LLM Interface

**Start LLM chat:**
```bash
python -m src.llm.chat
```

Example queries:
- "Show me momentum stocks in IT sector with positive sentiment"
- "Backtest RSI 14 on RELIANCE since 2020"
- "Explain today's buy signal for TCS"
- "Find research papers about mean reversion strategies"

---

## Documentation

- [**PROJECT_PLAN.md**](PROJECT_PLAN.md) - Comprehensive system design and architecture
- [**ROADMAP.md**](ROADMAP.md) - 32-week implementation roadmap with phases
- [**ARCHITECTURE.md**](ARCHITECTURE.md) - Technical architecture deep-dive
- [**CONTRIBUTING.md**](CONTRIBUTING.md) - Contribution guidelines
- [**docs/**](docs/) - Additional documentation and guides

---

## Key Modules

### Data Layer
- **Market Data**: OHLCV, volume, delivery%, FII/DII flows
- **News & Social**: RSS, NewsAPI, Twitter, Reddit
- **Storage**: DuckDB (queries), Parquet (time-series)

### Feature Engineering
- **Technical**: 50+ indicators (RSI, MACD, Bollinger, etc.)
- **Sentiment**: Transformer-based sentiment + topic modeling
- **Meta**: Regime detection, liquidity, correlations

### Machine Learning
- **Batch Models**: RandomForest, XGBoost, LightGBM
- **Online Learning**: River for intraday adaptation
- **Validation**: Walk-forward, purged CV, calibration

### Signal Generation
- **Risk Management**: ATR-based stops, 1% risk per trade
- **Position Sizing**: Volatility-adjusted
- **Filters**: Liquidity, regime, sentiment alignment

### Backtesting
- **Engine**: vectorbt for high-performance testing
- **Indicator League**: Rank 100+ indicator combinations
- **Ablation Tests**: Feature importance analysis

### LLM Integration
- **Local Models**: Qwen 2.5, LLaMA 3, Mistral
- **RAG**: Ingest research papers (PDF), GitHub repos
- **Functions**: Backtest runner, signal explainer, anomaly detector

---

## Performance Targets

| Metric | Target | Stretch Goal |
|--------|--------|--------------|
| Sharpe Ratio | > 1.0 | > 1.5 |
| CAGR | > 12% | > 18% |
| Max Drawdown | < 20% | < 15% |
| Win Rate | > 52% | > 58% |
| System Uptime | > 99% | > 99.9% |

---

## Safety & Governance

✅ **Data Integrity**: No future leakage, strict time-aware features
✅ **Feature Gating**: New features tested in sandbox
✅ **Statistical Significance**: >5% Sharpe improvement required
✅ **Human Approval**: LLM suggestions need review before deployment
✅ **Version Control**: Git + MLflow for full experiment tracking

---

## Technology Stack

**Core**: Python 3.11+, FastAPI, Streamlit
**Data**: DuckDB, Parquet, Polars, Pandas
**ML**: scikit-learn, XGBoost, LightGBM, River
**Backtesting**: vectorbt, vectorbtpro
**NLP**: spaCy, Transformers, sentence-transformers
**LLM**: llama.cpp, Ollama, LangChain
**Vector DB**: FAISS, Milvus
**Workflow**: Prefect, Airflow
**Monitoring**: Grafana, Prometheus, MLflow

---

## Roadmap Highlights

**Phase 1 (Weeks 1-8)**: Data infrastructure & indicators
**Phase 2 (Weeks 9-16)**: ML models & signal generation
**Phase 3 (Weeks 17-24)**: LLM integration & RAG
**Phase 4 (Weeks 25-32)**: Self-learning & production deployment

See [ROADMAP.md](ROADMAP.md) for detailed timeline.

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Key areas for contribution**:
- New technical indicators
- Additional data sources
- ML model improvements
- Dashboard features
- Documentation

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Disclaimer

**IMPORTANT**: This system is for educational and research purposes only.

- Past performance does not guarantee future results
- Trading involves risk of financial loss
- Do not trade with money you cannot afford to lose
- Always consult a qualified financial advisor
- The authors are not responsible for any financial losses

This is NOT financial advice.

---

## Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/mltr/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/mltr/discussions)
- **Email**: your.email@example.com

---

## Acknowledgments

Built with insights from:
- Advances in Financial Machine Learning (Marcos López de Prado)
- Machine Learning for Algorithmic Trading (Stefan Jansen)
- Open-source trading community

---

**Status**: 🚧 Under Active Development
**Version**: 0.1.0-alpha
**Last Updated**: 2025-11-03
