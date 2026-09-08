FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY consumer/ ./consumer/
COPY scrapers/ ./scrapers/

CMD ["uv", "run", "python", "-m", "consumer.src.consumer"]
