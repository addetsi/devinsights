"""Tests for the GitHub client."""

import responses

from scrapers.src.github_client import GitHubClient


@responses.activate
def test_get_returns_json() -> None:
    """A successful GET request returns the expected JSON data."""
    responses.add(
        responses.GET,
        "https://api.github.com/repos/owner/repo",
        json={"full_name": "owner/repo", "stargazers_count": 42},
        status=200,
    )

    client = GitHubClient("https://api.github.com")
    result = client.get("/repos/owner/repo")

    assert result["full_name"] == "owner/repo"
    assert result["stargazers_count"] == 42


@responses.activate
def test_get_raises_on_error() -> None:
    """A GET that receives an error status raises an exception."""
    import pytest
    import requests

    responses.add(
        responses.GET,
        "https://api.github.com/repos/owner/missing",
        status=404,
    )

    client = GitHubClient("https://api.github.com")
    with pytest.raises(requests.HTTPError):
        client.get("/repos/owner/missing")
