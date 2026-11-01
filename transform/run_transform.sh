#!/bin/bash
set -euo pipefail

cd /app

echo "=== Loader: Blob -> SQL ==="
uv run python -m loader.src.load_blob_to_sql

echo "=== DBT: transform ==="
uv run python -m transform.run_dbt run
uv run python -m transform.run_dbt test

echo "=== ML: train + predict ==="
uv run python -m ml.train_anomaly_model
uv run python -m ml.predict

echo "=== Transform pipeline complete ==="
