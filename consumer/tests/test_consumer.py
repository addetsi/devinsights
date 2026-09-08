"""Tests for the kafka consumer loop"""

import json
from typing import Any

from pytest_mock import MockerFixture

from consumer.src.consumer import GitHubConsumer
from consumer.src.sink import FileSink


class FakeMessage:
    """A stand-in for kafka message in tests"""

    def __init__(self, value: bytes | None, error: Any = None) -> None:
        self._value = value
        self._error = error

    def value(self) -> bytes | None:
        return self._value

    def error(self) -> Any:
        return self._error


def test_run_writes_and_commits(mocker: MockerFixture, tmp_path: Any) -> None:
    """A valid message is written to the sink and its offset committed"""
    mock_consumer_cls = mocker.patch("consumer.src.consumer.Consumer")
    mock_consumer = mock_consumer_cls.return_value

    payload = {"message_type": "repo", "repo": "owner/repo"}
    message = FakeMessage(value=json.dumps(payload).encode("utf-8"))
    mock_consumer.poll.side_effect = [message, None]

    sink = FileSink(str(tmp_path))
    consumer = GitHubConsumer("localhost:9092", "github-events", "tests-group", sink)
    consumed = consumer.run(max_messages=1)

    assert consumed == 1
    mock_consumer.commit.assert_called_once_with(message=message)

    written = list(tmp_path.glob("github/repo/*/*/*/data.jsonl"))
    assert len(written) == 1


def test_run_skips_empty_value(mocker: MockerFixture, tmp_path: Any) -> None:
    """A message with None value is skipped, not written"""
    mock_consumer_cls = mocker.patch("consumer.src.consumer.Consumer")
    mock_consumer = mock_consumer_cls.return_value

    empty = FakeMessage(value=None)
    mock_consumer.poll.side_effect = [empty, None]

    sink = FileSink(str(tmp_path))
    consumer = GitHubConsumer("localhost:9092", "github-events", "tests-group", sink)
    consumed = consumer.run(max_messages=1)
    assert consumed == 0
    written = list(tmp_path.glob("github/**/data.jsonl"))
    assert len(written) == 0
