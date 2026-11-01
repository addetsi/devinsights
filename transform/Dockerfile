FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl gnupg apt-transport-https \
    && curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && curl -sSL https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY common/ ./common/
COPY loader/ ./loader/
COPY ml/ ./ml/
COPY dbt_project/ ./dbt_project/
COPY streamlit_app/ ./streamlit_app/
COPY transform/ ./transform/
RUN chmod +x transform/run_transform.sh

CMD ["bash", "transform/run_transform.sh"]
