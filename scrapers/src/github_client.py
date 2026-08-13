"""Client for fetching data from the GitHub REST API."""

import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


class GitHubClient:
    """Fetches data from the GitHub REST API with authentication."""

    def __init__(self, base_url: str, token: str | None = None) -> None:
        self.base_url = base_url
        self.session = requests.Session()
        auth_token = token or GITHUB_TOKEN
        if auth_token:
            self.session.headers["Authorization"] = f"Bearer {auth_token}"
        self.session.headers["Accept"] = "application/vnd.github+json"

    def get(self, path: str) -> Any:
        """Perform a GET request against a GitHub API path and return JSON."""
        url = f"{self.base_url}{path}"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.json()

    def rate_limit_remaining(self, response: requests.Response) -> int:
        """Read the remaining rate-limit quota from a response's headers."""
        return int(response.headers.get("X-RateLimit-Remaining", 0))
