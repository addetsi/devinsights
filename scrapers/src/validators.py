"""Validation of GitHub API responses against JSON schemas"""

import logging
from typing import Any

from jsonschema import ValidationError, validate

from scrapers.src.schemas import SCHEMAS

logger = logging.getLogger("scraper")


def validate_message(message_type: str, data: dict[str, Any]) -> bool:
    """
    Validate data against the schema for its message type.
    Returns True if valid, False if invalid or no schema exists.
    Logs a warning on validation failure or missing schema.
    """
    schema = SCHEMAS.get(message_type)

    if schema is None:
        logger.warning("No schema for message_type '%s'; skipping validation", message_type)
        return False

    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError as err:
        logger.warning("Validation failed for '%s': %s", message_type, err.message)
        return False
