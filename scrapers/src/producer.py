"""Kafka producer for publishing scraped GitHub data to Kafka topics."""

import json
import os
from typing import Any

from confluent_kafka import Producer

from scrapers.src.logging_config import setup_logging

logger = setup_logging()


class GitHubProducer:
    """Publishes JSON messages to a Kafka topic."""

    def __init__(self, bootstrap_servers: str, topic: str) -> None:
        self.topic = topic
        config: dict[str, Any] = {"bootstrap.servers": bootstrap_servers}

        connection_string = os.getenv("EVENTHUB_CONNECTION_STRING")
        if connection_string:
            config.update(
                {
                    "security.protocol": "SASL_SSL",
                    "sasl.mechanism": "PLAIN",
                    "sasl.username": "$ConnectionString",
                    "sasl.password": connection_string,
                }
            )

        self.producer = Producer(config)

    def publish(self, message: dict[str, Any], key: str) -> None:
        """Serialize a message to JSON and publish it to the topic"""
        self.producer.produce(
            topic=self.topic,
            key=key.encode("utf-8"),
            value=json.dumps(message).encode("utf-8"),
            callback=self._delivery_report,
        )
        self.producer.poll(0)  # Trigger delivery report callbacks

    def flush(self) -> None:
        """Wait for all queued messages to be delivered"""
        self.producer.flush()

    @staticmethod
    def _delivery_report(err: Any, msg: Any) -> None:
        """Callback invoked once per message to report success or failure"""
        if err is not None:
            logger.error("Message delivery failed: %s", err)
        else:
            logger.info("Sent to %s [%d] at offset %d", msg.topic(), msg.partition(), msg.offset())
