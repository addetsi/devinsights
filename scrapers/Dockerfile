FROM python:3.12-slim

#install uv (the package manager) from its official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directoy inside the container
WORKDIR /app

# copy dependency files first fro layer caching
COPY pyproject.toml uv.lock ./

# Inatall dependencies into the container
RUN uv sync --frozen --no-dev

# Copy the scraper source code and config
COPY scrapers/ ./scrapers/

#Run the scraper when the container starts
CMD ["uv", "run", "python", "-m", "scrapers.src.scraper"]
