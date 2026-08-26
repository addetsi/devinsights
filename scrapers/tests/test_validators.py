"""Tests for GitHub response validation"""

from scrapers.src.validators import validate_message


def test_valid_repo_passes() -> None:
    """A well-formed repo object validates successfully"""

    data = {
        "full_name": "owner/repo",
        "stargazers_count": 100,
        "default_branch": "main",
        "language": "python",
    }

    assert validate_message("repo", data) is True


def test_repo_missing_require_field_fails() -> None:
    """A repo object missing a required field fails validation"""

    data = {
        "full_name": "owner/repo",
        # stargazers_count is missing
        "default_branch": "main",
    }

    assert validate_message("repo", data) is False


def test_repo_wrong_type_fails() -> None:
    """A repo object with a wrong field type fails validation"""

    data = {
        "full_name": "owner/repo",
        "stargazers_count": "not a number",  # should be an int
        "default_branch": "main",
    }

    assert validate_message("repo", data) is False


def test_null_language_passes() -> None:
    """A repo with null language (valid per GitHub) passes"""

    data = {
        "full_name": "owner/repo",
        "stargazers_count": 100,
        "default_branch": "main",
        "language": None,
    }

    assert validate_message("repo", data) is True


def test_unknown_message_type_fails() -> None:
    """Validation fails for an unknown message type"""

    assert validate_message("nonexistent", {"foo": "bar"}) is False
