"""Generate a Word document compliance report from narrative and data."""

import io
from datetime import UTC, datetime
from typing import Any

from docx import Document
from docx.document import Document as DocumentType


def build_report_docx(narrative: str, summary: dict[str, Any]) -> bytes:
    """Build a Word report combining the LLM narrative and a data table. Returns bytes."""
    doc = Document()

    doc.add_heading("DevInsights Compliance Report", level=0)

    date_para = doc.add_paragraph()
    date_run = date_para.add_run(
        f"Generated: {datetime.now(UTC).strftime('%B %d, %Y at %H:%M UTC')}"
    )
    date_run.italic = True
    # Narrative sections from Claude
    _add_narrative(doc, narrative)

    # Summary metrics table
    doc.add_heading("Key Metrics", level=1)
    table = doc.add_table(rows=1, cols=2)
    table.style = "Light Grid Accent 1"
    table.rows[0].cells[0].text = "Metric"
    table.rows[0].cells[1].text = "Value"

    if "total_repositories" in summary:
        metrics = [
            ("Total Repositories", summary["total_repositories"]),
            ("Total Pull Requests", summary["total_pull_requests"]),
            ("Compliance Pass Rate", f"{summary['compliance']['pass_rate_pct']}%"),
            (
                "Controls Passing",
                f"{summary['compliance']['passing']}/{summary['compliance']['controls_evaluated']}",
            ),
            ("Avg Lead Time (hours)", summary["dora"]["avg_lead_time_hours"]),
            ("Anomalies Flagged", summary["anomalies"]["flagged_count"]),
        ]
    else:
        metrics = []
    for name, value in metrics:
        row = table.add_row().cells
        row[0].text = name
        row[1].text = str(value)

    # Return as bytes for download
    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer.getvalue()


def _add_narrative(doc: DocumentType, narrative: str) -> None:
    """Parse markdown-ish narrative into Word headings, bullets, and paragraphs."""
    for raw_line in narrative.split("\n"):
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            doc.add_heading(line.lstrip("#").strip(), level=1)
        elif line.startswith("- ") or line.startswith("* "):
            p = doc.add_paragraph(style="List Bullet")
            _add_formatted_text(p, line[2:].strip())
        else:
            p = doc.add_paragraph()
            _add_formatted_text(p, line)


def _add_formatted_text(paragraph: Any, text: str) -> None:
    """Add text to a paragraph, converting **bold** markdown to bold runs."""
    import re

    parts = re.split(r"(\*\*.+?\*\*)", text)
    for part in parts:
        if part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
        elif part:
            paragraph.add_run(part)
