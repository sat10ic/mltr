# MLTR Source Code

This directory contains the main source code for the MLTR trading system.

## Module Overview

### Data Layer (`data/`)
Handles all data acquisition, storage, and retrieval.

- **`market/`** - OHLCV data fetching and storage
- **`news/`** - News scraping and sentiment analysis
- **`reference/`** - Static reference data (sectors, calendars, etc.)

[View Details](data/README.md)

---

### Feature Engineering (`features/`)
Transforms raw data into predictive signals.

- **`technical/`** - Technical indicators (RSI, MACD, etc.)
- **`sentiment/`** - NLP-based sentiment features
- **`store/`** - Feature registry and metadata

[View Details](features/README.md)

---

### Machine Learning (`ml/`)
Model training, prediction, and evaluation.

- **`models/`** - ML model implementations (XGBoost, LightGBM, etc.)
- **`labeling/`** - Target variable generation
- **`online/`** - Online/incremental learning (River)

[View Details](ml/README.md)

---

### Signal Generation (`signals/`)
Converts predictions to actionable trading signals.

- Signal generation logic
- Risk management rules
- Position sizing calculations

[View Details](signals/README.md)

---

### Backtesting (`backtest/`)
Historical testing and strategy evaluation.

- Walk-forward backtesting engine
- Indicator league table
- Performance metrics

[View Details](backtest/README.md)

---

### LLM Integration (`llm/`)
Local LLM for natural language interaction.

- LLM inference wrapper
- Function calling framework
- Prompt management

[View Details](llm/README.md)

---

### Knowledge Base (`knowledge/`)
Research paper and code ingestion via RAG.

- PDF ingestion
- GitHub repository parsing
- Vector database management

[View Details](knowledge/README.md)

---

### Feedback Loop (`feedback/`)
Trade outcome tracking and meta-learning.

- Trade logging
- Performance analysis
- Threshold tuning

[View Details](feedback/README.md)

---

### Workflow Orchestration (`workflow/`)
Scheduled task management.

- DAG definitions
- Cron schedules
- Error handling

[View Details](workflow/README.md)

---

### API (`api/`)
FastAPI REST endpoints.

- Data endpoints
- ML endpoints
- Signal endpoints

[View Details](api/README.md)

---

### Dashboard (`dashboard/`)
Streamlit web interface.

- Signal dashboard
- Backtesting interface
- Performance visualization

[View Details](dashboard/README.md)

---

## Development Workflow

### 1. Local Development

```bash
# Activate environment
source venv/bin/activate

# Install in editable mode
pip install -e ".[dev]"

# Run tests
pytest tests/

# Format code
black src/
isort src/
```

### 2. Adding a New Module

```bash
# Create module directory
mkdir -p src/newmodule

# Create files
touch src/newmodule/__init__.py
touch src/newmodule/README.md

# Add to module docs
# Update this file with new module info
```

### 3. Module Dependencies

Each module should:
- Have minimal dependencies on other modules
- Export clean APIs via `__init__.py`
- Include docstrings (Google style)
- Have corresponding tests in `tests/`

### 4. Import Structure

```python
# Good: Clean imports from module API
from src.data.market import fetch_ohlcv
from src.features.technical import calculate_rsi

# Bad: Deep internal imports
from src.data.market.fetchers.yfinance import YFinanceFetcher
```

---

## Code Standards

### Docstring Format (Google Style)

```python
def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """Calculate Relative Strength Index.

    Args:
        prices: Series of closing prices
        period: RSI period (default: 14)

    Returns:
        Series of RSI values (0-100)

    Raises:
        ValueError: If period is invalid

    Example:
        >>> prices = pd.Series([100, 102, 101, 105])
        >>> rsi = calculate_rsi(prices, period=14)
    """
    pass
```

### Type Hints

```python
from typing import List, Dict, Optional
import pandas as pd

def fetch_symbols(
    universe: str,
    start_date: str,
    end_date: Optional[str] = None
) -> pd.DataFrame:
    """Fetch data for symbol universe."""
    pass
```

### Error Handling

```python
from loguru import logger

def risky_operation(data):
    try:
        result = process(data)
        return result
    except ValueError as e:
        logger.error(f"Invalid data: {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise RuntimeError("Processing failed") from e
```

---

## Testing

Each module should have corresponding tests:

```
tests/
├── unit/
│   ├── data/
│   ├── features/
│   ├── ml/
│   └── ...
├── integration/
│   └── test_end_to_end.py
└── conftest.py
```

Run tests:
```bash
# All tests
pytest tests/

# Specific module
pytest tests/unit/features/

# With coverage
pytest tests/ --cov=src --cov-report=html
```

---

## Common Patterns

### Configuration

```python
from src.config import config

# Access config values
rsi_period = config.features.technical.momentum.rsi_periods[0]
```

### Logging

```python
from loguru import logger

logger.info("Processing started")
logger.debug(f"Parameters: {params}")
logger.warning("Low liquidity detected")
logger.error(f"Failed to fetch data: {e}")
```

### Database Access

```python
from src.data.database import get_connection

with get_connection() as conn:
    df = conn.execute("SELECT * FROM ohlcv").df()
```

---

## Performance Tips

1. **Use vectorized operations**: Prefer pandas/numpy over loops
2. **Cache expensive computations**: Use `@lru_cache` or Redis
3. **Use DuckDB for queries**: Much faster than pandas filtering
4. **Profile before optimizing**: `python -m cProfile script.py`
5. **Consider polars**: For very large datasets (10M+ rows)

---

## Module Communication

```
┌─────────┐     ┌──────────┐     ┌─────┐
│  Data   │────▶│ Features │────▶│ ML  │
└─────────┘     └──────────┘     └─────┘
                                    │
                                    ▼
                               ┌─────────┐
                               │ Signals │
                               └─────────┘
                                    │
                                    ▼
                               ┌──────────┐
                               │ Feedback │
                               └──────────┘
```

- Data layer is independent
- Features depend only on data
- ML depends on features
- Signals depend on ML
- Feedback depends on signals

---

## Quick Reference

| Task | Command |
|------|---------|
| Run tests | `pytest tests/` |
| Format code | `black src/ && isort src/` |
| Type check | `mypy src/` |
| Lint | `ruff check src/` |
| Coverage | `pytest --cov=src --cov-report=html` |
| Build docs | `mkdocs serve` (if using) |

---

For more details, see:
- [DEVELOPMENT_GUIDE.md](../DEVELOPMENT_GUIDE.md)
- [ARCHITECTURE.md](../ARCHITECTURE.md)
- [CONTRIBUTING.md](../CONTRIBUTING.md)
