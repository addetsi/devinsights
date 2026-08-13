"""Tests for scraper config loading."""

from pathlib import Path

from scrapers.src.config import load_config


def test_load_config_parses_expected_fields(tmp_path: Path) -> None:
    """A well-formed config file loads into a typed ScraperConfig."""
    config_text = """
source: github
api:
  base_url: https://api.github.com
  auth: token
kafka:
  topic: github-events
  bootstrap_servers: localhost:9092
repositories:
  - owner/repo-one
  - owner/repo-two
endpoints:
  - name: repo_metadata
    path: /repos/{repo}
    message_type: repo
"""

    config_file = tmp_path / "test_config.yml"
    config_file.write_text(config_text)

    config = load_config(config_file)

    assert config.source == "github"
    assert config.kafka_topic == "github-events"
    assert len(config.repositories) == 2
    assert config.endpoints[0].name == "repo_metadata"
    assert config.endpoints[0].message_type == "repo"
