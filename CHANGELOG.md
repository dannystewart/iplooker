# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog], and this project adheres to [Semantic Versioning].

## [Unreleased]

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
[unreleased]: https://github.com/dannystewart/iplooker/compare/v0.1.10...HEAD
[0.1.10]: https://github.com/dannystewart/iplooker/compare/v0.1.9...v0.1.10
[0.1.9]: https://github.com/dannystewart/iplooker/releases/tag/v0.1.9
[0.1.8]: https://github.com/dannystewart/iplooker/compare/v0.1.9...v0.1.8
