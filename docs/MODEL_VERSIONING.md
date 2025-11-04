# Model & Data Versioning Guide

## Overview

Proper versioning ensures reproducibility, enables rollback, and tracks experiments systematically.

## MLflow Integration

### Setup

```bash
# Install MLflow
pip install mlflow

# Set tracking URI
export MLFLOW_TRACKING_URI=file:///home/user/mltr/data/mlruns

# Or in code
import mlflow
mlflow.set_tracking_uri("file:///home/user/mltr/data/mlruns")
```

### Logging Experiments

```python
import mlflow
import mlflow.sklearn

# Start experiment
mlflow.set_experiment("momentum_strategy_v1")

with mlflow.start_run(run_name="xgboost_baseline"):
    # Log parameters
    mlflow.log_param("model_type", "xgboost")
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 6)

    # Train model
    model.fit(X_train, y_train)

    # Log metrics
    mlflow.log_metric("sharpe_ratio", 1.45)
    mlflow.log_metric("cagr", 0.18)
    mlflow.log_metric("max_drawdown", -0.12)

    # Log model
    mlflow.sklearn.log_model(model, "model")

    # Log artifacts
    mlflow.log_artifact("feature_importance.png")
    mlflow.log_artifact("backtest_report.html")
```

### Model Registry

```python
# Register model
model_uri = f"runs:/{run.info.run_id}/model"
mlflow.register_model(model_uri, "XGBoostMomentum")

# Transition to production
client = mlflow.tracking.MlflowClient()
client.transition_model_version_stage(
    name="XGBoostMomentum",
    version=1,
    stage="Production"
)

# Load production model
model = mlflow.pyfunc.load_model("models:/XGBoostMomentum/Production")
```

---

## DVC (Data Version Control)

### Why DVC?

- Version large datasets efficiently
- Track data pipeline dependencies
- Share data across team
- Integrate with Git

### Setup

```bash
# Install DVC
pip install dvc dvc-gdrive  # or dvc-s3, dvc-azure

# Initialize
dvc init

# Add remote storage
dvc remote add -d storage gdrive://your-folder-id
# Or S3
dvc remote add -d storage s3://mltr-data/dvc-storage
```

### Tracking Data

```bash
# Track data directory
dvc add data/raw/ohlcv
dvc add data/processed/features

# Commit .dvc files to git
git add data/raw/ohlcv.dvc data/processed/features.dvc
git commit -m "Track data with DVC"

# Push data to remote
dvc push

# Pull data on another machine
dvc pull
```

### Pipeline Tracking

```yaml
# dvc.yaml
stages:
  fetch_data:
    cmd: python scripts/fetch_data.py
    deps:
      - scripts/fetch_data.py
    outs:
      - data/raw/ohlcv

  compute_features:
    cmd: python src/features/compute.py
    deps:
      - data/raw/ohlcv
      - src/features/compute.py
    outs:
      - data/processed/features

  train_model:
    cmd: python src/ml/train.py
    deps:
      - data/processed/features
      - src/ml/train.py
    params:
      - ml.models.xgboost
    metrics:
      - metrics.json:
          cache: false
    outs:
      - data/models/xgboost_v1.pkl
```

Run pipeline:
```bash
dvc repro
```

---

## Versioning Strategy

### Semantic Versioning for Models

Format: `MAJOR.MINOR.PATCH`

- **MAJOR**: Incompatible changes (new features, different output format)
- **MINOR**: Backward-compatible improvements (better accuracy, tuning)
- **PATCH**: Bug fixes, no model changes

Examples:
- `v1.0.0` - Initial model
- `v1.1.0` - Added new features, retrained
- `v1.1.1` - Fixed calibration bug
- `v2.0.0` - Complete model redesign

### Model Naming Convention

```
{strategy}_{model_type}_v{version}

Examples:
- momentum_xgboost_v1.0.0
- mean_reversion_lightgbm_v2.1.0
- sector_rotation_rf_v1.2.1
```

### Data Versioning

```
data_{source}_{YYYYMMDD}

Examples:
- data_nse_20241103
- data_newsapi_20241103
```

---

## Experiment Tracking

### Experiment Metadata

```json
{
  "experiment_id": "exp_20241103_001",
  "model_version": "v1.2.0",
  "data_version": "data_nse_20241103",
  "features": ["rsi_14", "macd", "bb_position"],
  "hyperparameters": {
    "n_estimators": 100,
    "max_depth": 6,
    "learning_rate": 0.1
  },
  "metrics": {
    "sharpe_ratio": 1.45,
    "cagr": 0.18,
    "max_drawdown": -0.12
  },
  "training_date": "2024-11-03T16:30:00",
  "backtested_period": "2023-01-01 to 2024-10-31"
}
```

Save with each model:
```python
import json
from pathlib import Path

metadata = {...}  # As above

model_dir = Path(f"data/models/momentum_xgboost_v1.2.0")
model_dir.mkdir(exist_ok=True)

with open(model_dir / "metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)
```

---

## Feature Store Versioning

### Feature Definitions

```python
# src/features/registry.py

FEATURE_REGISTRY = {
    "rsi_14": {
        "version": "v1.0",
        "function": "calculate_rsi",
        "params": {"period": 14},
        "dependencies": ["close"],
        "created": "2024-01-15",
        "deprecated": None
    },
    "macd": {
        "version": "v1.1",  # Updated calculation
        "function": "calculate_macd",
        "params": {"fast": 12, "slow": 26, "signal": 9},
        "dependencies": ["close"],
        "created": "2024-01-15",
        "deprecated": None
    }
}
```

### Feature Lineage

Track which features went into which model:

```python
# Track feature versions used in model
model_features = {
    "model_version": "v1.2.0",
    "features": [
        {"name": "rsi_14", "version": "v1.0"},
        {"name": "macd", "version": "v1.1"},
        {"name": "sentiment_7d", "version": "v2.0"}
    ]
}
```

---

## Rollback Strategy

### Rolling Back Models

```python
# List model versions
versions = client.search_model_versions("name='XGBoostMomentum'")

# Rollback to previous version
client.transition_model_version_stage(
    name="XGBoostMomentum",
    version=2,  # Previous version
    stage="Production",
    archive_existing_versions=True
)
```

### Rolling Back Data

```bash
# Check data history
dvc diff HEAD~1

# Rollback data
git checkout HEAD~1 data/processed/features.dvc
dvc checkout
```

---

## Best Practices

### 1. Always Log These Items

- Model hyperparameters
- Training data version
- Feature list and versions
- Performance metrics (in-sample & out-of-sample)
- Training duration
- Code commit hash

### 2. Tag Important Versions

```bash
# Tag model version in git
git tag -a model-v1.2.0 -m "Production model v1.2.0"
git push origin model-v1.2.0
```

### 3. Archive Old Models

Keep models for at least 6 months:

```python
# Archive policy
if model_age_days > 180 and model_stage == "Archived":
    archive_to_cold_storage(model)
```

### 4. Document Changes

Maintain a CHANGELOG for models:

```markdown
# Model Changelog

## v1.2.0 (2024-11-03)
### Added
- New sentiment features (7-day aggregation)
- ATR-based volatility features

### Changed
- Increased tree depth from 4 to 6
- Retrained on extended dataset (3 years)

### Fixed
- Calibration curve now properly trained

### Performance
- Sharpe: 1.25 → 1.45
- Max DD: -18% → -12%
```

---

## Production Deployment

### Model Promotion Pipeline

```
Experiment → Staging → Canary → Production

1. Experiment: Initial training and validation
2. Staging: Further validation on hold-out set
3. Canary: Deploy to 10% of signals for 1 week
4. Production: Full deployment if canary successful
```

### Deployment Checklist

- [ ] Model passes all unit tests
- [ ] Out-of-sample Sharpe > baseline
- [ ] Calibration check passed
- [ ] Canary test completed (1 week minimum)
- [ ] Metadata and documentation complete
- [ ] Rollback plan documented
- [ ] Monitoring alerts configured

---

## Monitoring Model Drift

```python
# Track prediction distribution over time
from scipy import stats

def check_prediction_drift(current_preds, reference_preds):
    """Check if prediction distribution has drifted."""
    statistic, p_value = stats.ks_2samp(current_preds, reference_preds)

    if p_value < 0.05:
        logger.warning(f"Prediction drift detected (p={p_value:.4f})")
        # Trigger retraining

    return p_value
```

---

## Tools Summary

| Tool | Purpose | When to Use |
|------|---------|-------------|
| **MLflow** | Experiment tracking, model registry | All ML experiments |
| **DVC** | Data versioning, pipeline tracking | Large datasets, team collaboration |
| **Git** | Code versioning, feature definitions | All code changes |
| **Model Registry** | Production model management | Model deployment |
| **Feature Store** | Feature versioning, lineage | Production features |

---

## Example Workflow

```bash
# 1. Create experiment branch
git checkout -b exp/momentum-v2

# 2. Add/modify features
# Edit src/features/technical/indicators.py

# 3. Track data
dvc add data/processed/features

# 4. Train model with MLflow
python src/ml/train.py --experiment momentum_v2

# 5. Evaluate
mlflow ui  # View results

# 6. If successful, register model
python scripts/register_model.py --model-name MomentumV2 --run-id <run_id>

# 7. Commit everything
git add .
git commit -m "Add momentum v2 model"
dvc push
git push

# 8. Deploy to staging
python scripts/deploy.py --model MomentumV2 --stage Staging
```

---

For more details:
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [DVC User Guide](https://dvc.org/doc)
- [DEVELOPMENT_GUIDE.md](../DEVELOPMENT_GUIDE.md)
