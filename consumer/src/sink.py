"""File sink that writes consumed messages to organized local storage"""

import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger("consumer")


class FileSink:
    """Writes messages to date-partitioned JSON files under a base directory"""

    def __init__(self, base_path: str) -> None:
        self.base_path = Path(base_path)

    def write(self, message: dict[str, Any]) -> None:
        """Append a message to the appropriate date-partitioned file"""
        message_type = message.get("message_type", "unknown")
        now = datetime.now(UTC)

        target_dir = self.base_path / "github" / message_type / now.strftime("%Y/%m/%d")
        target_dir.mkdir(parents=True, exist_ok=True)

        target_file = target_dir / "data.jsonl"
        with target_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(message, ensure_ascii=False) + "\n")

        logger.debug("Wrote %s message to %s", message_type, target_file)
