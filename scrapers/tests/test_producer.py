"""Tests for the Kafka producer."""

import pytest
from pytest_mock import MockerFixture

from scrapers.src.producer import GitHubProducer


@pytest.fixture(autouse=True)
def mock_secrets(mocker: MockerFixture) -> None:
    mocker.patch("scrapers.src.producer.get_secret", return_value=None)


def test_publish_produces_encoded_message(mocker: MockerFixture) -> None:
    """publish() serializes the message and calls the underlying producer."""

    mock_producer = mocker.patch("scrapers.src.producer.Producer")

    producer = GitHubProducer("localhost:9092", "test-topic")
    producer.publish({"repo": "owner/repo", "stars": 42}, key="owner/repo")

    instance = mock_producer.return_value
    instance.produce.assert_called_once()

    call_kwargs = instance.produce.call_args.kwargs
    assert call_kwargs["topic"] == "test-topic"
    assert call_kwargs["key"] == b"owner/repo"
    assert b'"repo": "owner/repo"' in call_kwargs["value"]


def test_flush_calls_underlying_flush(mocker: MockerFixture) -> None:
    """ "flush() calls the underlying producer's flush method."""

    mock_producer = mocker.patch("scrapers.src.producer.Producer")

    producer = GitHubProducer("localhost:9092", "test-topic")
    producer.flush()

    mock_producer.return_value.flush.assert_called_once()
