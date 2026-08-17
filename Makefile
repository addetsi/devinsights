.PHONY: install lint format test check

install:
	uv sync --all-extras --dev
	pre-commit install

lint:
	uv run ruff check .

format:
	uv run ruff format .

fix:
	uv run ruff check --fix .
	uv run ruff format .

test:
	uv run pytest

check: lint test
	uv run mypy .
