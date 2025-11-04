# Contributing to MLTR

Thank you for your interest in contributing to the LLM-Integrated ML Trading Research & Intelligence System!

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How Can I Contribute?](#how-can-i-contribute)
3. [Development Setup](#development-setup)
4. [Development Workflow](#development-workflow)
5. [Testing Guidelines](#testing-guidelines)
6. [Code Standards](#code-standards)
7. [Pull Request Process](#pull-request-process)
8. [Safety & Governance](#safety--governance)

---

## Code of Conduct

This project adheres to a code of professional conduct:

- Be respectful and constructive
- Focus on technical merit
- Welcome diverse perspectives
- Provide helpful feedback
- Prioritize system safety and integrity

---

## How Can I Contribute?

### Reporting Bugs

**Before submitting a bug report:**
- Check existing issues to avoid duplicates
- Collect relevant information (version, OS, error messages)
- Try to reproduce the issue consistently

**Bug report should include:**
- Clear, descriptive title
- Steps to reproduce
- Expected vs actual behavior
- Environment details (Python version, OS, dependencies)
- Relevant logs or screenshots

### Suggesting Features

**Feature suggestions should include:**
- Clear use case and motivation
- Expected behavior and benefits
- Potential implementation approach
- Performance/safety considerations

**Priority areas for contributions:**
- New technical indicators
- Additional data sources
- ML model improvements
- Dashboard enhancements
- Documentation improvements
- Test coverage expansion

### Improving Documentation

Documentation improvements are always welcome:
- Fix typos or clarify unclear sections
- Add examples or tutorials
- Improve API documentation
- Update outdated information

---

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
git clone https://github.com/yourusername/mltr.git
cd mltr
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Development Dependencies

```bash
# Install all dependencies including dev tools
pip install -r requirements.txt
pip install -e ".[dev]"

# Or using pyproject.toml
pip install -e ".[dev,llm,all]"
```

### 4. Set Up Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

### 5. Configure Environment

```bash
cp .env.example .env
cp configs/config.example.yaml configs/config.yaml

# Edit .env and config.yaml with your settings
```

### 6. Download Sample Data

```bash
python scripts/setup_data.py --symbols NIFTY50 --days 365
```

### 7. Run Tests

```bash
pytest tests/
```

---

## Development Workflow

### Branch Naming Convention

- `feature/short-description` - New features
- `fix/issue-description` - Bug fixes
- `refactor/component-name` - Code refactoring
- `docs/what-changed` - Documentation updates
- `test/what-testing` - Test additions/improvements

### Typical Workflow

1. **Create a branch**
   ```bash
   git checkout -b feature/new-indicator
   ```

2. **Make changes**
   - Write code following standards (see below)
   - Add tests for new functionality
   - Update documentation if needed

3. **Run tests and linters**
   ```bash
   # Format code
   black src/ tests/
   isort src/ tests/

   # Run linters
   flake8 src/ tests/
   pylint src/

   # Run tests
   pytest tests/ --cov=src
   ```

4. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: add RSI divergence indicator"
   ```

   **Commit message format:**
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `refactor:` - Code refactoring
   - `test:` - Adding tests
   - `docs:` - Documentation
   - `chore:` - Maintenance tasks

5. **Push and create PR**
   ```bash
   git push origin feature/new-indicator
   ```

---

## Testing Guidelines

### Test Structure

```
tests/
├── unit/              # Unit tests for individual functions
├── integration/       # Integration tests for module interactions
└── e2e/              # End-to-end tests for full workflows
```

### Writing Tests

**Example unit test:**
```python
# tests/unit/features/test_technical.py
import pytest
import pandas as pd
from src.features.technical.indicators import calculate_rsi

def test_rsi_calculation():
    # Arrange
    prices = pd.Series([100, 102, 101, 105, 107, 106, 108])

    # Act
    rsi = calculate_rsi(prices, period=14)

    # Assert
    assert not rsi.isna().all()
    assert (rsi >= 0).all() and (rsi <= 100).all()

def test_rsi_with_invalid_period():
    prices = pd.Series([100, 102, 101])

    with pytest.raises(ValueError):
        calculate_rsi(prices, period=-1)
```

**Example integration test:**
```python
# tests/integration/test_signal_generation.py
def test_full_signal_pipeline(sample_data):
    # Test feature computation → ML prediction → signal generation
    features = compute_features(sample_data)
    predictions = model.predict(features)
    signals = generate_signals(predictions)

    assert len(signals) > 0
    assert all(s.confidence >= 0.6 for s in signals)
```

### Test Markers

Use pytest markers to categorize tests:

```python
@pytest.mark.slow
def test_full_backtest():
    # Long-running test
    pass

@pytest.mark.integration
def test_database_connection():
    # Integration test
    pass

@pytest.mark.llm
def test_llm_query():
    # Requires LLM
    pass
```

**Run specific test categories:**
```bash
pytest -m "not slow"          # Skip slow tests
pytest -m integration         # Only integration tests
pytest tests/unit/            # Only unit tests
```

### Test Coverage

- Aim for >80% coverage for core modules
- 100% coverage for critical paths (risk management, data validation)
- Mock external dependencies (APIs, databases)

---

## Code Standards

### Python Style Guide

Follow **PEP 8** with these specifics:

- **Line length:** 100 characters
- **Indentation:** 4 spaces
- **Imports:** Organized with isort (stdlib → third-party → local)
- **Docstrings:** Google style

**Example:**
```python
def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """Calculate Relative Strength Index (RSI).

    Args:
        prices: Series of closing prices
        period: RSI period (default: 14)

    Returns:
        Series of RSI values (0-100)

    Raises:
        ValueError: If period is invalid or prices too short

    Example:
        >>> prices = pd.Series([100, 102, 101, 105])
        >>> rsi = calculate_rsi(prices, period=14)
    """
    if period <= 0:
        raise ValueError(f"Period must be positive, got {period}")

    if len(prices) < period:
        raise ValueError(f"Need at least {period} prices")

    # Implementation...
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return rsi
```

### Type Hints

Use type hints for all public functions:

```python
from typing import List, Dict, Optional, Union
import pandas as pd

def fetch_ohlcv(
    symbol: str,
    start_date: str,
    end_date: Optional[str] = None
) -> pd.DataFrame:
    """Fetch OHLCV data."""
    pass

def generate_signals(
    predictions: pd.DataFrame,
    min_confidence: float = 0.6
) -> List[Dict[str, Union[str, float]]]:
    """Generate trading signals."""
    pass
```

### Error Handling

- Use specific exceptions
- Provide helpful error messages
- Log errors appropriately

```python
from loguru import logger

def validate_data(df: pd.DataFrame) -> None:
    """Validate OHLCV data."""
    required_cols = ['open', 'high', 'low', 'close', 'volume']

    missing = set(required_cols) - set(df.columns)
    if missing:
        error_msg = f"Missing required columns: {missing}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    if df.empty:
        raise ValueError("DataFrame is empty")

    if df.isnull().any().any():
        logger.warning("Data contains null values, will be forward-filled")
```

### Logging

Use `loguru` for consistent logging:

```python
from loguru import logger

logger.info(f"Fetching data for {symbol} from {start} to {end}")
logger.debug(f"Feature computation took {elapsed:.2f}s")
logger.warning(f"Low liquidity detected for {symbol}")
logger.error(f"Failed to fetch data: {e}")
```

### Configuration

- Use config files for parameters (not hardcoded)
- Support environment variable overrides
- Validate configuration on startup

```python
from src.config import config

# Good
rsi_period = config.features.technical.momentum.rsi_periods[0]

# Bad
rsi_period = 14  # Hardcoded
```

---

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated if needed
- [ ] No hardcoded secrets or API keys
- [ ] Commit messages are clear

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Refactoring
- [ ] Documentation
- [ ] Test improvement

## Testing
Describe testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No breaking changes (or documented)

## Related Issues
Closes #123
```

### Review Process

1. **Automated checks** run (tests, linters)
2. **Code review** by maintainer(s)
3. **Revisions** if requested
4. **Approval** and merge

**Review criteria:**
- Code quality and readability
- Test coverage
- Performance impact
- Safety considerations (no data leakage, proper validation)
- Documentation clarity

---

## Safety & Governance

### Critical Rules

⚠️ **NEVER commit:**
- API keys or secrets
- Real trading credentials
- Personal data
- Production database backups

⚠️ **ALWAYS:**
- Validate inputs (prevent data leakage)
- Add tests for risk-critical code
- Document assumptions
- Consider edge cases

### Feature Gating

New features that affect trading signals:

1. **Mark as experimental** in config
2. **Sandbox testing** with ablation analysis
3. **Statistical significance** check (>5% Sharpe improvement)
4. **Human review** before production

### Backtest Integrity

- No future data leakage
- Realistic transaction costs
- Walk-forward validation only
- Document all assumptions

### Code Review Focus Areas

**For data features:**
- Is there any look-ahead bias?
- Are NaN values handled correctly?
- Is computation efficient?

**For ML models:**
- Is train/test split time-aware?
- Are probabilities calibrated?
- Is overfitting prevented?

**For signals:**
- Are risk limits enforced?
- Is position sizing correct?
- Are edge cases handled?

---

## Questions?

- **General questions:** Open a GitHub Discussion
- **Bug reports:** Open an Issue
- **Security concerns:** Email directly (do not create public issue)

---

**Thank you for contributing to MLTR!** 🚀
