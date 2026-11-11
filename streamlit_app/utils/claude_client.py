"""Client for generating compliance report narratives via the Claude API."""

import json
from typing import Any

from anthropic import Anthropic

from common.secrets import get_secret

MODEL = "claude-opus-5-5"

REPORT_PROMPT = """You are a DevOps compliance analyst. Based on the repository \
metrics data below, write a professional compliance report narrative.

Use these section headings exactly (as markdown ## headings):
## Executive Summary
## Compliance Overview
## DORA Metrics Summary
## Anomaly Alerts

Write in clear paragraphs. Use bullet points (- ) for lists. Do NOT create \
markdown tables. Do NOT invent data not present below. Reference actual numbers. \
Keep it concise and professional.

DATA:
{data}
"""

REPO_PROMPT = """You are a DevOps compliance analyst. Write a focused compliance \
report for a single repository based on the data below.

Use these markdown ## headings:
## Repository Overview
## Compliance Status
## Activity & DORA
## Anomalies

Write clear paragraphs, use - bullets for lists, no markdown tables. Reference \
actual numbers. Do not invent data. Keep it concise.

DATA:
{data}
"""

FLAGGED_PROMPT = """You are a DevOps compliance analyst. Write a report focused on \
repositories flagged for anomalous activity, based on the data below.

Use these markdown ## headings:
## Summary
## Flagged Repositories
## Recommended Actions

Write clear paragraphs, use - bullets, no markdown tables. Reference actual numbers. \
Do not invent data. Keep it concise.

DATA:
{data}
"""


def generate_report_narrative(data: dict[str, Any], prompt_template: str = REPORT_PROMPT) -> str:
    """Send data to Claude with the given prompt template, return the narrative."""
    api_key = get_secret("anthropic-api-key", "ANTHROPIC_API_KEY")
    if api_key is None:
        raise RuntimeError("ANTHROPIC_API_KEY not available")

    client = Anthropic(api_key=api_key)
    prompt = prompt_template.format(data=json.dumps(data, indent=2, default=str))
    message = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(block.text for block in message.content if block.type == "text")
