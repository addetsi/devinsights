"""DevInsights dashboard - GitHub repository compliance and DORA metrics."""

import streamlit as st
from utils.db_connection import query_df

st.set_page_config(page_title="DevInsights", layout="wide")

st.title("DevInsights")
st.caption("GitHub repository compliance and DORA metrics")


@st.cache_data(ttl=300)
def load_repo_summary():  # type: ignore[no-untyped-def]
    return query_df("SELECT * FROM dbo.repo_summary")


@st.cache_data(ttl=300)
def load_controls():  # type: ignore[no-untyped-def]
    return query_df("SELECT * FROM dbo.controls_pr_review")


@st.cache_data(ttl=300)
def load_dora():  # type: ignore[no-untyped-def]
    return query_df("SELECT * FROM dbo.metrics_dora")


repos = load_repo_summary()
dora = load_dora()
controls = load_controls()

# Top-level metrics
col1, col2, col3 = st.columns(3)
col1.metric("Repositories", len(repos))
col2.metric("Total PRs", int(repos["total_prs"].sum()))
passing = (controls["has_pr_activity"] == "PASS").sum()
col3.metric("Passing Controls", f"{passing}/{len(controls)}")

st.divider()

# Sidebar filters
st.sidebar.header("Filters")
languages = ["All", *sorted(repos["language"].dropna().unique().tolist())]
selected_lang = st.sidebar.selectbox("Language", languages)

filtered = repos if selected_lang == "All" else repos[repos["language"] == selected_lang]

# Charts row
st.subheader("Activity Overview")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.caption("Top 10 repos by total PRs")
    top_prs = filtered.nlargest(10, "total_prs").set_index("repo")["total_prs"]
    st.bar_chart(top_prs)

with chart_col2:
    st.caption("Repositories by language")
    lang_counts = repos["language"].value_counts()
    st.bar_chart(lang_counts)

st.divider()

# Filtered repo health table
st.subheader("Repository Health")
st.dataframe(filtered, use_container_width=True)

# DORA metrics
st.subheader("DORA — Lead Time")
st.dataframe(dora, use_container_width=True)

# Compliance controls
st.subheader("Compliance Controls")
st.dataframe(controls, use_container_width=True)
