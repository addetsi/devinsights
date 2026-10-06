"""Score weekly repo activity for anomalies using the trained Isolation Forest model."""

import logging

import joblib
import pandas as pd

from ml.train_anomaly_model import FEATURE_COLS, MODEL_PATH, SCALER_PATH, build_features
from streamlit_app.utils.db_connection import get_engine, query_df

logger = logging.getLogger("ml")

RESULTS_TABLE = "anomaly_scores"


def predict() -> pd.DataFrame:
    """Load the saved model, score all weekly activity, return flagged anomalies."""
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    df = query_df(
        "SELECT repo, yr, wk, commits_per_week, prs_opened_per_week FROM dbo.gold_weekly_activity"
    )
    df = build_features(df)

    x = df[FEATURE_COLS].fillna(0)
    x_scaled = scaler.transform(x)

    # -1 = anomaly, 1 = normal; score_samples gives the raw anomaly score
    df["is_anomaly"] = model.predict(x_scaled)
    df["anomaly_score"] = model.score_samples(x_scaled)
    df["flagged"] = df["is_anomaly"] == -1

    logger.info("Scored %d rows, flagged %d anomalies", len(df), int(df["flagged"].sum()))
    return df


def write_results(df: pd.DataFrame) -> None:
    """Write anomaly scores back to SQL for the dashboard to read."""
    engine = get_engine()
    out = df[
        ["repo", "yr", "wk", "commits_per_week", "prs_opened_per_week", "anomaly_score", "flagged"]
    ]
    out.to_sql(RESULTS_TABLE, engine, schema="dbo", if_exists="replace", index=False)
    logger.info("Wrote %d rows to %s", len(out), RESULTS_TABLE)


def main() -> None:
    from scrapers.src.logging_config import setup_logging

    setup_logging()
    df = predict()
    write_results(df)


if __name__ == "__main__":
    main()
