""" "Tests for the file sink"""

import json
from pathlib import Path

from consumer.src.sink import FileSink


def test_write_creates_partitioned_file(tmp_path: Path) -> None:
    """A written message lands in a data-partitioned JSONL file"""
    sink = FileSink(str(tmp_path))
    message = {"message_type": "repo", "repo": "owner/repo", "data": {"stars": 10}}

    sink.write(message)

    written = list(tmp_path.glob("github/repo/*/*/*/data.jsonl"))
    assert len(written) == 1

    content = written[0].read_text().strip()
    assert json.loads(content) == message


def test_write_appends_multiple_messages(tmp_path: Path) -> None:
    """Multiple writes append as separate JSONL lines"""
    sink = FileSink(str(tmp_path))
    sink.write({"message_type": "repo", "id": 1})
    sink.write({"message_type": "repo", "id": 2})

    written = list(tmp_path.glob("github/repo/*/*/*/data.jsonl"))
    lines = written[0].read_text().strip().split("\n")
    assert len(lines) == 2
    assert json.loads(lines[0])["id"] == 1
    assert json.loads(lines[1])["id"] == 2


def test_write_separate_message_types(tmp_path: Path) -> None:
    """Different message types are written to separate files"""
    sink = FileSink(str(tmp_path))
    sink.write({"message_type": "repoid", "id": 1})
    sink.write({"message_type": "pull_request", "id": 2})

    repo_files = list(tmp_path.glob("github/repoid/*/*/*/data.jsonl"))
    pr_files = list(tmp_path.glob("github/pull_request/*/*/*/data.jsonl"))
    assert len(repo_files) == 1
    assert len(pr_files) == 1
