# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-11-15

### Added

- Ruff linter and pytest unit tests
- PR workflow running lint and tests
- Codecov integration
- GitHub Actions workflow for generating Allure test reports
- Automatic publication of Allure reports to GitHub Pages
- SonarQube Cloud integration for automated code quality analysis
- Snyk integration for automated security vulnerability scanning
- Dependabot configuration
- Dockerfile and .dockerignore for container image build
- Workflow publishing the Docker image to Quay.io on release
- Slack notifications about workflow runs via GitHub app subscription
- Keyless cosign signing and verification of the image

## [0.1.1] - 2026-10-25

### Added

- REST-сервіс на FastAPI з базовою структурою пакету
- LICENSE
- CODE_OF_CONDUCT.md
- CONTRIBUTING.md
- SECURITY.md
- Issue template
- Pull Request template
- GitHub Actions: збірка пакету на Pull Request
- GitHub Actions: автоматичний тег і реліз після злиття в main
- Scheduled and manual image scanning with Trivy, Grype and Snyk (SARIF to Code Scanning)

### Changed

- README: corrected the `GET /health` response example and documented the `GET /info` endpoint
- Release workflow triggers Docker publish explicitly via workflow_dispatch