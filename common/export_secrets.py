"""Fetch SQL secrets from Key Vault and write shell exports to a file (never stdout)."""

import sys

from common.secrets import get_secret


def main() -> None:
    """Write export statements for SQL credentials to the path given as argv[1]."""
    out_path = sys.argv[1]
    server = get_secret("sql-server-fqdn", "SQL_SERVER")
    password = get_secret("sql-admin-password", "SQL_PASSWORD")

    lines = [
        f"export SQL_SERVER='{server}'",
        "export SQL_DATABASE='sqldb-devinsights-dev'",
        "export SQL_USER='sqladmin'",
        f"export SQL_PASSWORD='{password}'",
    ]
    with open(out_path, "w") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
