FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY common/ ./common/
COPY consumer/ ./consumer/

CMD ["uv", "run", "python", "-m", "consumer.src.consumer"]
