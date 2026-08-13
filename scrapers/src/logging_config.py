"""Centralized logging configuration for the scraper"""

import logging


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure and return a logger for the scraper."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger("scraper")
