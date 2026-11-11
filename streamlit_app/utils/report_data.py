"""Aggregate gold-layer data into a summary for report generation."""

from typing import Any

from common.db_connection import query_df


def build_report_summary() -> dict[str, Any]:
    """Query gold tables and aggregate into a compact summary for the LLM."""
    repos = query_df("SELECT * FROM dbo.repo_summary")
    controls = query_df("SELECT * FROM dbo.controls_pr_review")
    dora = query_df("SELECT * FROM dbo.metrics_dora")
    anomalies = query_df(
        "SELECT repo, yr, wk, commits_per_week, anomaly_score "
        "FROM dbo.anomaly_scores WHERE flagged = 1 ORDER BY anomaly_score ASC"
    )

    passing = int((controls["has_pr_activity"] == "PASS").sum())

    return {
        "total_repositories": len(repos),
        "total_pull_requests": int(repos["total_prs"].sum()),
        "compliance": {
            "controls_evaluated": len(controls),
            "passing": passing,
            "failing": len(controls) - passing,
            "pass_rate_pct": round(100 * passing / len(controls), 1) if len(controls) else 0,
        },
        "dora": {
            "avg_lead_time_hours": round(float(dora["avg_lead_time_hours"].mean()), 1)
            if len(dora)
            else None,
            "repos_with_merged_prs": len(dora),
        },
        "anomalies": {
            "flagged_count": len(anomalies),
            "flagged_repos": anomalies.head(10).to_dict(orient="records"),
        },
        "top_repos_by_prs": repos.nlargest(5, "total_prs")[["repo", "total_prs", "stars"]].to_dict(
            orient="records"
        ),
    }


def build_repo_report_summary(repo: str) -> dict[str, Any]:
    """Aggregate data for a single repository."""
    p = {"repo": repo}
    repo_row = query_df("SELECT * FROM dbo.repo_summary WHERE repo = :repo", p)
    control = query_df("SELECT * FROM dbo.controls_pr_review WHERE repo = :repo", p)
    dora = query_df("SELECT * FROM dbo.metrics_dora WHERE repo = :repo", p)
    anomalies = query_df(
        "SELECT repo, yr, wk, commits_per_week, anomaly_score "
        "FROM dbo.anomaly_scores WHERE repo = :repo AND flagged = 1 "
        "ORDER BY anomaly_score ASC",
        p,
    )
    return {
        "repository": repo,
        "metrics": repo_row.to_dict(orient="records")[0] if len(repo_row) else {},
        "compliance": control.to_dict(orient="records")[0] if len(control) else {},
        "dora": dora.to_dict(orient="records")[0] if len(dora) else {},
        "anomalies": anomalies.to_dict(orient="records"),
    }


def build_flagged_report_summary() -> dict[str, Any]:
    """Aggregate data for all anomaly-flagged repositories."""
    anomalies = query_df(
        "SELECT repo, yr, wk, commits_per_week, anomaly_score "
        "FROM dbo.anomaly_scores WHERE flagged = 1 ORDER BY anomaly_score ASC"
    )
    flagged_repos = anomalies["repo"].unique().tolist()
    return {
        "flagged_repository_count": len(flagged_repos),
        "flagged_repositories": flagged_repos,
        "total_flagged_weeks": len(anomalies),
        "anomaly_details": anomalies.to_dict(orient="records"),
    }
