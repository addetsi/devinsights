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

COMMIT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["sha", "commit"],
    "properties": {
        "sha": {"type": "string"},
        "commit": {"type": "object"},
    },
}

RELEASE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["id", "tag_name"],
    "properties": {
        "id": {"type": "integer"},
        "tag_name": {"type": "string"},
        "published_at": {"type": ["string", "null"]},
    },
}

BRANCH_PROTECTION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "required_pull_request_reviews": {"type": "object"},
        "enforce_admins": {"type": "object"},
    },
}

SCHEMAS: dict[str, dict[str, Any]] = {
    "repo": REPO_SCHEMA,
    "pull_request": PULL_REQUEST_SCHEMA,
    "commit": COMMIT_SCHEMA,
    "release": RELEASE_SCHEMA,
    "branch_protection": BRANCH_PROTECTION_SCHEMA,
}
