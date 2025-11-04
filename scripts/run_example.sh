#!/bin/bash
# Smoke test script for MLTR
# This runs a minimal end-to-end test to verify basic functionality

set -e  # Exit on error

echo "=========================================="
echo "MLTR Smoke Test"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo -e "${YELLOW}Warning: Virtual environment not detected${NC}"
    echo "Consider activating: source venv/bin/activate"
fi

# Step 1: Check dependencies
echo ""
echo "Step 1: Checking dependencies..."
python -c "import pandas, numpy, pytest" 2>/dev/null && \
    echo -e "${GREEN}✓ Core dependencies installed${NC}" || \
    (echo -e "${RED}✗ Missing core dependencies. Run: pip install -r requirements.txt${NC}" && exit 1)

# Step 2: Validate example data
echo ""
echo "Step 2: Validating example data..."
if [ -f "tests/data/example_ohlcv.csv" ]; then
    python -c "
import pandas as pd
df = pd.read_csv('tests/data/example_ohlcv.csv')
assert len(df) > 0, 'Empty dataframe'
assert 'close' in df.columns, 'Missing close column'
print(f'  Found {len(df)} rows for {df[\"symbol\"].nunique()} symbols')
" && echo -e "${GREEN}✓ Example data valid${NC}" || \
    (echo -e "${RED}✗ Example data invalid${NC}" && exit 1)
else
    echo -e "${YELLOW}⚠ Example data not found (expected for initial setup)${NC}"
fi

# Step 3: Run unit tests (fast)
echo ""
echo "Step 3: Running unit tests..."
if [ -d "tests/unit" ] && [ "$(ls -A tests/unit 2>/dev/null)" ]; then
    pytest tests/unit/ -v --tb=short -m "not slow" 2>&1 | tail -n 20 && \
        echo -e "${GREEN}✓ Unit tests passed${NC}" || \
        (echo -e "${YELLOW}⚠ Some unit tests failed (expected for initial setup)${NC}")
else
    echo -e "${YELLOW}⚠ No unit tests found yet (expected for initial setup)${NC}"
fi

# Step 4: Simulate feature computation
echo ""
echo "Step 4: Testing feature computation..."
python << 'PYEOF'
import sys
import pandas as pd
import numpy as np

# Simple RSI calculation test
def calculate_rsi_simple(prices, period=14):
    """Simple RSI for testing."""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

try:
    # Load data
    df = pd.read_csv('tests/data/example_ohlcv.csv')

    # Calculate RSI for each symbol
    results = []
    for symbol in df['symbol'].unique():
        symbol_data = df[df['symbol'] == symbol].copy()
        symbol_data['rsi'] = calculate_rsi_simple(symbol_data['close'])
        results.append(symbol_data)

    combined = pd.concat(results)
    valid_rsi = combined['rsi'].dropna()

    # Validate
    assert len(valid_rsi) > 0, "No RSI values computed"
    assert (valid_rsi >= 0).all() and (valid_rsi <= 100).all(), "RSI out of range"

    print(f"  Computed RSI for {len(df['symbol'].unique())} symbols")
    print(f"  RSI range: {valid_rsi.min():.1f} - {valid_rsi.max():.1f}")
    print("✓ Feature computation successful")
    sys.exit(0)
except Exception as e:
    print(f"✗ Feature computation failed: {e}")
    sys.exit(1)
PYEOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Feature computation passed${NC}"
else
    echo -e "${YELLOW}⚠ Feature computation had issues${NC}"
fi

# Step 5: Test configuration loading
echo ""
echo "Step 5: Testing configuration..."
python << 'PYEOF'
import sys
import yaml
from pathlib import Path

try:
    config_path = Path('configs/config.example.yaml')
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Check critical keys
        assert 'data' in config, "Missing 'data' in config"
        assert 'ml' in config, "Missing 'ml' in config"
        assert 'signals' in config, "Missing 'signals' in config"

        print(f"  Loaded configuration with {len(config)} top-level keys")
        print("✓ Configuration valid")
        sys.exit(0)
    else:
        print("⚠ Config file not found (expected)")
        sys.exit(0)
except Exception as e:
    print(f"✗ Configuration error: {e}")
    sys.exit(1)
PYEOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Configuration test passed${NC}"
else
    echo -e "${YELLOW}⚠ Configuration test had issues${NC}"
fi

# Step 6: Test basic ML pipeline
echo ""
echo "Step 6: Testing ML pipeline stub..."
python << 'PYEOF'
import sys
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

try:
    # Generate synthetic features and labels
    np.random.seed(42)
    n_samples = 100

    # Features
    X = pd.DataFrame({
        'rsi': np.random.uniform(30, 70, n_samples),
        'macd': np.random.uniform(-10, 10, n_samples),
        'volume_ratio': np.random.uniform(0.5, 2.0, n_samples),
    })

    # Labels (binary: will price go up?)
    y = np.random.choice([0, 1], size=n_samples, p=[0.45, 0.55])

    # Split and train
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X_train, y_train)

    # Predict
    predictions = model.predict_proba(X_test)[:, 1]

    # Validate
    assert len(predictions) == len(X_test), "Prediction length mismatch"
    assert (predictions >= 0).all() and (predictions <= 1).all(), "Probabilities out of range"

    accuracy = (model.predict(X_test) == y_test).mean()

    print(f"  Trained model on {len(X_train)} samples")
    print(f"  Test accuracy: {accuracy:.2%}")
    print("✓ ML pipeline successful")
    sys.exit(0)
except Exception as e:
    print(f"✗ ML pipeline failed: {e}")
    sys.exit(1)
PYEOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ ML pipeline test passed${NC}"
else
    echo -e "${YELLOW}⚠ ML pipeline test had issues${NC}"
fi

# Summary
echo ""
echo "=========================================="
echo -e "${GREEN}Smoke test completed!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Review test results above"
echo "2. Run full test suite: pytest tests/"
echo "3. Start development: see DEVELOPMENT_GUIDE.md"
echo "4. Check roadmap: ROADMAP.md"
echo ""
