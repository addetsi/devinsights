#!/bin/bash
set -euo pipefail   # -e exit on error, -u error on unset var, -o pipefail catch pipe failures

cd /app

echo "=== Fetching SQL credentials from Key Vault ==="
SECRET_FILE=$(mktemp)
uv run python -m common.export_secrets "$SECRET_FILE"
set -a            # auto-export everything sourced
source "$SECRET_FILE"
set +a
rm -f "$SECRET_FILE"

# Verify critical vars loaded before proceeding
: "${SQL_SERVER:?SQL_SERVER not set after sourcing secrets}"

echo "=== Loader: Blob -> SQL ==="
uv run python -m loader.src.load_blob_to_sql

echo "=== DBT: transform ==="
export DBT_PROFILES_DIR=/app/dbt_project
(cd /app/dbt_project && uv run dbt run && uv run dbt test)

echo "=== ML: train + predict ==="
cd /app
uv run python -m ml.train_anomaly_model
uv run python -m ml.predict

echo "=== Transform pipeline complete ==="
