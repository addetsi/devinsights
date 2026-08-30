"""Kafka consumer that reads messages and writes them via a sink."""

import json
import logging
import os
from typing import Any

from confluent_kafka import Consumer, KafkaError

from consumer.src.sink import FileSink

logger = logging.getLogger("consumer")


class GitHubConsumer:
    """Consumes messages from a Kafka topic and writes them to a sink."""

    def __init__(self, bootstrap_servers: str, topic: str, group_id: str, sink: FileSink) -> None:
        self.topic = topic
        self.sink = sink
        self.consumer = Consumer(
            {
                "bootstrap.servers": bootstrap_servers,
                "group.id": group_id,
                "auto.offset.reset": "earliest",
                "enable.auto.commit": False,
            }
        )

    def run(self, max_messages: int | None = None) -> int:
        """Consume messages and write them to the sink. Returns count consumed."""
        self.consumer.subscribe([self.topic])
        consumed = 0
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)

                if msg is None:
                    if max_messages is None:
                        continue
                    break

                error = msg.error()
                if error is not None:
                    if error.code() == KafkaError._PARTITION_EOF:
                        continue
                    logger.error("Consumer error: %s", error)
                    continue

                value = msg.value()
                if value is None:
                    logger.warning("Recieved message with empty value; skipping")
                    continue

                data: dict[str, Any] = json.loads(value.decode("utf-8"))
                self.sink.write(data)
                self.consumer.commit(message=msg)
                consumed += 1

        finally:
            self.consumer.close()

        logger.info("Consumed %d messages", consumed)
        return consumed


def main() -> None:
    """Entry point: build consumer and run it."""
    from scrapers.src.logging_config import setup_logging

    setup_logging()
    bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    sink = FileSink(os.getenv("LANDING_PATH", "/tmp/devinsights-landing"))
    consumer = GitHubConsumer(bootstrap, "github-events", "github-consumer", sink)
    consumer.run()


if __name__ == "__main__":
    main()
