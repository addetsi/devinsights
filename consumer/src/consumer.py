"""Kafka consumer that reads messages and writes them via a sink."""

import json
import logging
import os
from typing import Any

from confluent_kafka import Consumer, KafkaError

from consumer.src.sink import FileSink
from scrapers.src.logging_config import setup_logging

logger = logging.getLogger("consumer")


class GitHubConsumer:
    """Consumes messages from a Kafka topic and writes them to a sink."""

    def __init__(self, bootstrap_servers: str, topic: str, group_id: str, sink: Any) -> None:
        self.topic = topic
        self.sink = sink
        config: dict[str, Any] = {
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": False,
        }

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
        self.consumer = Consumer(config)

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

    setup_logging()
    bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

    blob_conn = os.getenv("BLOB_CONNECTION_STRING")
    sink: Any
    if blob_conn:
        from consumer.src.blob_sink import BlobSink

        sink = BlobSink(blob_conn)
    else:
        sink = FileSink(os.getenv("LANDING_PATH", "/tmp/devinsights-landing"))

    consumer = GitHubConsumer(bootstrap, "github-events", "github-consumer-v3", sink)
    consumer.run()


if __name__ == "__main__":
    main()
