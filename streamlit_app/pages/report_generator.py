"""Streamlit page: generate and download AI compliance reports."""

from datetime import datetime

import streamlit as st

from common.db_connection import query_df
from streamlit_app.utils.claude_client import (
    FLAGGED_PROMPT,
    REPO_PROMPT,
    REPORT_PROMPT,
    generate_report_narrative,
)
from streamlit_app.utils.doc_generator import build_report_docx
from streamlit_app.utils.report_data import (
    build_flagged_report_summary,
    build_repo_report_summary,
    build_report_summary,
)

st.set_page_config(page_title="Report Generator", layout="wide")
st.title("Compliance Report Generator")

report_type = st.radio(
    "Report type",
    ["Organization-wide", "Single repository", "Flagged repositories"],
)

selected_repo = None
if report_type == "Single repository":
    repos = query_df("SELECT repo FROM dbo.repo_summary ORDER BY repo")["repo"].tolist()
    selected_repo = st.selectbox("Repository", repos)

if st.button("Generate Report", type="primary"):
    with st.spinner("Aggregating data..."):
        if report_type == "Organization-wide":
            summary = build_report_summary()
            prompt = REPORT_PROMPT
        elif report_type == "Single repository":
            if selected_repo is None:
                st.error("Please select a repository.")
                st.stop()
            summary = build_repo_report_summary(str(selected_repo))
            prompt = REPO_PROMPT
        else:
            summary = build_flagged_report_summary()
            prompt = FLAGGED_PROMPT

    with st.spinner("Generating narrative with Claude..."):
        narrative = generate_report_narrative(summary, prompt)

    st.subheader("Report Narrative")
    st.markdown(narrative)

    with st.spinner("Building Word document..."):
        docx_bytes = build_report_docx(narrative, summary)

    st.download_button(
        label="Download Report (.docx)",
        data=docx_bytes,
        file_name=f"devinsights_report_{datetime.now().strftime('%Y%m%d')}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    st.success("Report generated.")
