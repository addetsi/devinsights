"""Run dbt with SQL credentials injected in-process (secrets never written to disk)."""

import os
import subprocess
import sys

from common.secrets import get_secret


def main() -> None:
    """Fetch SQL credentials into the environment, then run the dbt commands passed as args."""
    env = os.environ.copy()
    env["SQL_SERVER"] = get_secret("sql-server-fqdn", "SQL_SERVER") or ""
    env["SQL_DATABASE"] = "sqldb-devinsights-dev"
    env["SQL_USER"] = "sqladmin"
    env["SQL_PASSWORD"] = get_secret("sql-admin-password", "SQL_PASSWORD") or ""
    env["DBT_PROFILES_DIR"] = "/app/dbt_project"

    result = subprocess.run(
        ["uv", "run", "dbt", *sys.argv[1:]],
        cwd="/app/dbt_project",
        env=env,
    )
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
