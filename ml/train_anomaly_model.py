"""Train an Isolation forest anomaly detection model on weekly repo activity."""

import logging
import os

import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from streamlit_app.utils.db_connection import query_df

logger = logging.getLogger("ml")

MODEL_PATH = "ml/models/anomaly_model.joblib"
SCALER_PATH = "ml/models/scaler.joblib"
FEATURE_COLS = [
    "commits_per_week",
    "pr_opened_per_week",
    "commits_rolling_avg",
    "commits_wow_change",
]


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Engineer features from raw weekly activity."""
    df = df.sort_values(["repo", "yr", "wk"]).copy()

    # Rolling average of comits per repo (4-weeek window)
    df["commits_rolling_avg"] = df.groupby("repo")["commits_per_week"].transform(
        lambda s: s.rolling(window=4, min_periods=1).mean()
    )
    # Week-over-week change in commits per repo
    # Week-over-week change in commits per repo
    df["commits_wow_change"] = df.groupby("repo")["commits_per_week"].transform(
        lambda s: s.diff().fillna(0)
    )

    return df


def train() -> None:
    """Load weekly activity, engineer features, fit Isolation Forest, save artifacts."""
    df = query_df(
        "SELECT repo, yr, wk, commits_per_week, prs_opened_per_week FROM dbo.gold_weekly_activity"
    )
    logger.info("Loaded %d weekly activity rows", len(df))

    df = build_features(df)
    x = df[FEATURE_COLS].fillna(0)

    # Scale features so no single feature dominates by magnitude
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)

    # Isolation Forest: unsupervised anomaly detection
    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42,
    )
    model.fit(x_scaled)
    logger.info("Model trained on %d samples", len(x))

    os.makedirs("ml/models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    logger.info("Saved model to %s", MODEL_PATH)


def main() -> None:
    from scrapers.src.logging_config import setup_logging

    setup_logging()
    train()


if __name__ == "__main__":
    main()
