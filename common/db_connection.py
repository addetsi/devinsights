"""Database connection for the Streamlit dashboard."""

import os
from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def get_engine() -> Engine:
    """Create a SQLAlchemy engine for Azure SQL from environment variables."""
    server = os.environ["SQL_SERVER"]
    database = os.environ["SQL_DATABASE"]
    user = os.environ["SQL_USER"]
    password = os.environ["SQL_PASSWORD"]

    params = quote_plus(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={password};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=no;"
        f"Connection Timeout=30;"
    )
    return create_engine(f"mssql+pyodbc:///?odbc_connect={params}")


def query_df(query: str) -> pd.DataFrame:
    """Run a SQL query and return the result as a DataFrame."""
    engine = get_engine()
    with engine.connect() as connection:
        return pd.read_sql(query, connection)
