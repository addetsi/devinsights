"""Centralized logging configuration."""

import logging
from pathlib import Path


def setup_logging(level: int = logging.INFO, log_file: str | None = None) -> logging.Logger:
    """Configure logging to console, and optionally to a file."""
    handlers: list[logging.Handler] = [logging.StreamHandler()]

    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=handlers,
    )
    return logging.getLogger("scraper")
