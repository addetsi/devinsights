"""Blob storage sink that writes consumed messages to Azure Blob Storage"""

import json
import logging
from datetime import UTC, datetime
from typing import Any

from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient

logger = logging.getLogger("consumer")


class BlobSink:
    """Writes messages to date-partitioned append blobs in an Azure container"""

    def __init__(self, connection_string: str, container: str = "raw") -> None:
        self.service = BlobServiceClient.from_connection_string(connection_string)
        self.container = container

    def write(self, message: dict[str, Any]) -> None:
        """Append a message as a JSONL line to a date-partitioned append blob"""
        message_type = message.get("message_type", "unknown")
        now = datetime.now(UTC)
        blob_path = f"github/{message_type}/{now.strftime('%Y/%m/%d')}/data.jsonl"

        blob_client = self.service.get_blob_client(container=self.container, blob=blob_path)

        try:
            blob_client.create_append_blob()
        except ResourceExistsError:
            logger.debug("Resource already exists")

        line = (json.dumps(message) + "\n").encode("utf-8")
        blob_client.append_block(line)

        logger.debug("Wrote %s message to %s", message_type, blob_path)
