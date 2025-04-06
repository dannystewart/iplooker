# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog], and this project adheres to [Semantic Versioning].

## [Unreleased]

### Changed

- Updates `polykit` dependency to v0.7.3 for improved compatibility.

## [0.1.12] (2025-04-05)

### Added

- Adds unit tests for the `IPLookup` class, covering core methods like `get_ip_info`, `standardize_country`, and `perform_ip_lookup` with isolated testing through mocking.
- Integrates `pytest` and `pytest-cov` for testing and coverage reporting. Updates `.vscode/settings.json` for pytest support and disables unittest. Adds dependencies for pytest and related plugins to enhance testing capabilities.

### Changed

- Updates `polykit` dependency to version 0.7.1 for compatibility with the latest improvements.
- Changes import and usage of `ArgParser` to the renamed `PolyArgs` class from the `polykit.cli` module to align with the updated library.

### Fixed

- Fixes logic in `IPLookup` to ensure accurate ISP and organization name comparisons by preserving original values.

### Improved

- Enhances type annotations in IP lookup tests with `Literal` and more specific types, improving type safety and maintainability.

## [0.1.11] (2025-04-05)

### Changed

- Updates `polykit` to version 0.7.0 to incorporate new features and improve dependency management.
- Modifies `pyproject.toml` and `poetry.lock` to reflect updated and new dependencies.
- Updates changelog for v0.1.10 with details on dependency updates, import path adjustments, and new conventional commit scope settings.
- Updates version links in the changelog for the v0.1.10 release.

### Removed

- Removes unused packages to improve maintainability.

## [0.1.10] (2025-04-05)

### Changed

- Updates dependencies by removing unused packages and upgrading `polykit` to version 0.6.0.
- Updates import paths from `polykit.parsers` to `polykit.formatters` for improved clarity and functionality.

### Added

- Adds settings for conventional commit scopes to improve commit consistency.

### Removed

- Removes unused packages to streamline the codebase.

## [0.1.9] (2025-04-04)

### Added

- Adds settings to support conventional commit scopes, improving commit message standardization.

### Changed

- Updates imports to use `polykit.formatters` instead of `polykit.parsers` for improved code organization.

### Removed

- Removes unused packages to streamline dependencies.
- Removes support for older versions of `polykit` and updates the library to version 0.6.0.

## [0.1.8] (2025-04-04)

### Added

- Adds `arguer` package as a development dependency in `pyproject.toml`

### Changed

- Replaces `arguer` and `shelper` with `polykit` components in `ip_lookup` module

## [0.1.7] (2025-04-01)

### Added

- Restores interrupt handler functionality with the `handle_interrupt` feature.

<!-- Links -->
[Keep a Changelog]: https://keepachangelog.com/en/1.1.0/
[Semantic Versioning]: https://semver.org/spec/v2.0.0.html

<!-- Versions -->
[unreleased]: https://github.com/dannystewart/iplooker/compare/v0.1.12...HEAD
[0.1.12]: https://github.com/dannystewart/iplooker/compare/v0.1.11...v0.1.12
[0.1.11]: https://github.com/dannystewart/iplooker/compare/v0.1.10...v0.1.11
[0.1.10]: https://github.com/dannystewart/iplooker/compare/v0.1.9...v0.1.10
[0.1.9]: https://github.com/dannystewart/iplooker/releases/tag/v0.1.9
[0.1.8]: https://github.com/dannystewart/iplooker/compare/v0.1.9...v0.1.8
