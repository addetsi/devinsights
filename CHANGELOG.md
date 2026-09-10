# Changelog

All notable changes to this project are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/),
versioning follows [Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-06-25

### Added
- Repository structure and tooling configuration
- uv project setup (application mode, Python 3.12)
- Strict ruff and mypy configuration
- Pre-commit hooks (formatting, linting, type checking, secret scanning)
- GitHub Actions CI pipeline (lint, format, type check, tests, pre-commit)
- Branch protection and PR-based workflow
- Makefile and pull request template

## [0.2.0] - 2026-07-15

### Added
- Terraform foundation with remote state backend in Azure
- Resource group and blob storage landing zone
- Key Vault with RBAC authorization
- Event Hubs namespace with scoped producer/consumer auth rules
- Azure SQL Database with firewall rules
- Connection strings and secrets stored in Key Vault
- Terraform outputs for resource names

## [0.4.0] - 2026-09-11

### Added
- Kafka consumer with file sink, manual offset commit (at-least-once)
- Blob Storage append-blob sink for cloud landing zone
- Dockerfiles for scraper and consumer
- Unit tests for consumer, sink, and validators
- Cloud swap: Event Hubs (SASL_SSL) + Blob Storage integration

## [0.3.0] - 2026-09-5

### Added
- Config-driven GitHub scraper with Kafka producer
- JSON schema validation at ingestion boundary
- Scrape timestamp on each message
- Local-first development against containerized Kafka
