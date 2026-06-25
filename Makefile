.PHONY: install lint format test check

install:
	uv sync --all-extras --dev
	pre-commit install

lint:
	uvx ruff check .

format:
	uvx ruff format .

test:
	uv run pytest

check: lint test
	uvx mypy .
