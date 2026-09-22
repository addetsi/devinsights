"""load raw JSONL data from blob storage into azure sql raw table."""

import json
import logging
import os

import pyodbc
from azure.storage.blob import BlobServiceClient

from scrapers.src.logging_config import setup_logging

logger = logging.getLogger("loader")

RAW_TABLE = "raw_github_events"

CREATE_TABLE_SQL = f"""
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{RAW_TABLE}' AND xtype ='U')
CREATE TABLE {RAW_TABLE} (
    id INT IDENTITY(1,1) PRIMARY KEY,
    message_type NVARCHAR(50),
    repo NVARCHAR(255),
    scraped_at NVARCHAR(50),
    payload NVARCHAR(MAX),
    loaded_at DATETIME2 DEFAULT SYSUTCDATETIME()
);
"""


def get_sql_connection() -> pyodbc.Connection:
    """Build a pyodbc connection to Azure SQL from environment variables."""
    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={os.environ['SQL_SERVER']};"
        f"DATABASE={os.environ['SQL_DATABASE']};"
        f"UID={os.environ['SQL_USER']};"
        f"PWD={os.environ['SQL_PASSWORD']};"
        f"Encrypt=yes;TrustServerCertificate=no;"
    )
    return pyodbc.connect(conn_str)


def load() -> int:
    """Real all JSONL blobs from the raw container and insert into SQL"""
    blob_conn = os.environ["BLOB_CONNECTION_STRING"]
    service = BlobServiceClient.from_connection_string(blob_conn)
    container = service.get_container_client("raw")

    conn = get_sql_connection()
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE_SQL)
    conn.commit()

    inserted = 0
    for blob in container.list_blobs():
        data = container.download_blob(blob.name).readall().decode("utf-8")
        for line in data.strip().split("\n"):
            if not line:
                continue
            record = json.loads(line)
            cursor.execute(
                f"INSERT INTO {RAW_TABLE} (message_type, repo, scraped_at, payload) "
                "VALUES (?, ?, ?, ?)",
                record.get("message_type"),
                record.get("repo"),
                record.get("scraped_at"),
                json.dumps(record.get("data")),
            )
            inserted += 1

    conn.commit()
    cursor.close()
    conn.close()
    logger.info("Loaded %d records into %s", inserted, RAW_TABLE)
    return inserted


def main() -> None:
    """Entry point."""
    setup_logging()
    load()


if __name__ == "__main__":
    main()
