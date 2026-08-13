"""Kafka producer for publishing scraped GitHub data to Kafka topics."""

import json
from typing import Any

from confluent_kafka import Producer

from scrapers.src.logging_config import setup_logging

logger = setup_logging()


class GitHubProducer:
    """Publishes JSON messages to a Kafka topic."""

    def __init__(self, bootstrap_servers: str, topic: str) -> None:
        self.topic = topic
        self.producer = Producer({"bootstrap.servers": bootstrap_servers})

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
