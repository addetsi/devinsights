"""Database connection for the Streamlit dashboard."""

from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from common.secrets import get_secret


def get_engine() -> Engine:
    """Create a SQLAlchemy engine for Azure SQL from environment variables."""
    server = get_secret("sql-server-fqdn", "SQL_SERVER") or ""
    database = "sqldb-devinsights-dev"
    user = "sqladmin"
    password = get_secret("sql-admin-password", "SQL_PASSWORD") or ""

    params = quote_plus(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={{{password}}};"
        f"Encrypt=yes; TrustServerCertificate=no; Connection Timeout=60;"
    )
    return create_engine(f"mssql+pyodbc:///?odbc_connect={params}")


def query_df(query: str) -> pd.DataFrame:
    """Run a SQL query and return the result as a DataFrame."""
    engine = get_engine()
    with engine.connect() as connection:
        return pd.read_sql(query, connection)
