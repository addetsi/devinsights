# DevInsights

A DevOps analytics platform on Azure. It collects public
GitHub repository data, streams it through a message broker, lands
it in cloud storage, transforms it through a medallion architecture,
and surfaces compliance and DORA metrics in a dashboard with
AI-generated reports.

> Status: in active development. Built phase by phase.

## Tech stack

- **Language:** Python 3.12 (managed with uv)
- **Infrastructure:** Terraform on Azure
- **Streaming:** Azure Event Hubs (Kafka protocol)
- **Storage:** Azure Blob Storage
- **Warehouse:** Azure SQL Database
- **Transformation:** DBT Core
- **Dashboard:** Streamlit
- **CI/CD:** GitHub Actions
- **Quality:** ruff, mypy, pre-commit, gitleaks

## Development setup

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12.

```bash
# Install dependencies and git hooks
make install

# Run quality checks
make check
```

## Workflow

All changes go through a pull request to `main`. CI must pass
(lint, format, type check, tests, pre-commit) before merging.
Commits follow [Conventional Commits](https://www.conventionalcommits.org/).

## License

MIT — see [LICENSE](LICENSE).
