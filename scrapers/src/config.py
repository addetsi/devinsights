"""Configuration loading and validation for the scraper."""

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class Endpoint:
    """A single GitHub API endpoint to scrape."""

    name: str
    path: str
    message_type: str


@dataclass
class ScraperConfig:
    """Full scraper configuration loaded from a YAML file."""

    source: str
    base_url: str
    kafka_topic: str
    bootstrap_servers: str
    repositories: list[str]
    endpoints: list[Endpoint]


def load_config(path: Path) -> ScraperConfig:
    """Load and parse a scraper config YAML file into a typed object."""
    with path.open() as f:
        raw = yaml.safe_load(f)

    endpoints = [
        Endpoint(name=e["name"], path=e["path"], message_type=e["message_type"])
        for e in raw["endpoints"]
    ]

    return ScraperConfig(
        source=raw["source"],
        base_url=raw["api"]["base_url"],
        kafka_topic=raw["kafka"]["topic"],
        bootstrap_servers=raw["kafka"]["bootstrap_servers"],
        repositories=raw["repositories"],
        endpoints=endpoints,
    )
