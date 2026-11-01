#!/bin/bash
set -euo pipefail

cd /app

echo "=== [1/3] Scrape: GitHub -> Event Hubs ==="
uv run python -m scrapers.src.scraper

echo "=== [2/3] Consume: Event Hubs -> Blob ==="
uv run python -m consumer.src.consumer

echo "=== [3/3] Transform: Blob -> SQL -> dbt -> ml ==="
uv run python -m loader.src.load_blob_to_sql
uv run python -m transform.run_dbt run
uv run python -m transform.run_dbt test
uv run python -m ml.train_anomaly_model
uv run python -m ml.predict

echo "=== Pipeline complete ==="
