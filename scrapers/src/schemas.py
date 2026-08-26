"""JSON schemas for validating GitHub responses before publishing"""

from typing import Any

REPO_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["full_name", "stargazers_count", "default_branch"],
    "properties": {
        "full_name": {"type": "string"},
        "stargazers_count": {"type": "integer"},
        "forks_count": {"type": "integer"},
        "default_branch": {"type": "string"},
        "language": {"type": ["string", "null"]},
        "created_at": {"type": "string"},
        "updated_at": {"type": "string"},
    },
}

PULL_REQUEST_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["number", "state", "created_at"],
    "properties": {
        "number": {"type": "integer"},
        "state": {"type": "string"},
        "created_at": {"type": "string"},
        "merged_at": {"type": ["string", "null"]},
        "user": {"type": "object"},
    },
}

SCHEMAS: dict[str, dict[str, Any]] = {"repo": REPO_SCHEMA, "pull_request": PULL_REQUEST_SCHEMA}
