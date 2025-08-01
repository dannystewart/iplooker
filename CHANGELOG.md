# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog], and this project adheres to [Semantic Versioning].

## [Unreleased]

## [0.3.3] (2025-08-01)

### Fixed

- Fixes IP API URL to properly include the IP parameter, ensuring the API looks up the provided IP address instead of the computer's own IP.

## [0.3.2] (2025-07-11)

### Changed

- Updates `polykit` dependency from 0.12.0b1 to 0.13.1.dev with minimum required version set to 0.13.0.
- Updates several dependencies:
  - `ruff` from 0.11.12 to 0.12.3
  - `certifi` from 2025.6.15 to 2025.7.9
  - `typing-extensions` from 4.13.2 to 4.14.1
  - `requests` from 2.32.3 to 2.32.4
  - `mypy` from 1.16.0 to 1.16.1
- Updates import paths to match new `polykit` package structure.(`polykit.formatters` → `polykit.text`, `polykit.env` → `polykit`).

## [0.3.1] (2025-06-07)

### Added

- Adds enhanced error handling for IP lookups.
- Adds new `lookup_with_reason` method that returns both lookup results and failure reasons.
- Adds detailed feedback by displaying specific failure reasons for each missing source.

### Changed

- Improves error reporting in request handling and response validation.
- Changes handling of sources without API keys to silently skip them instead of showing error messages.

## [0.3.0] (2025-05-31)

### Added

- Adds user-provided API key support via environment variables, making the tool more flexible for users with their own API keys.
- Adds `polykit` setup initialization to add standard base Polykit features.

### Changed

- Centralizes IP lookup source imports for improved code organization and maintenance.
- Renames `IPGeoLocationLookup` to `IPGeolocationLookup` for class name consistency.
- Updates dev dependencies (`mypy` to 1.16.0 and `ruff` to 0.11.12).

### Documentation

- Adds note about API key usage policy to the README.
- Updates README with security information about version 0.2.0 features.
- Adds information about IP address categorization capabilities (VPN, proxy, Tor exit node).
- Reorders README sections for better documentation flow.
- Updates the source list with the latest providers and correctly states that the application uses seven IP lookup service providers instead of six.

## [0.2.0] (2025-05-14)

Version 0.2.0 is a near total rewrite.

### Added

- No longer scrapes results from iplocation.net. Now uses proper APIs directly from seven IP lookup service providers:
  - ip-api.com
  - ipapi.co
  - ipapi.is
  - ipdata.co
  - ipgeolocation.io
  - ipinfo.io
  - iplocate.io
- Now uses an abstract base class for standardized lookup sources and results, adding modularity and making it much easier to add new sources.
- Adds security information to IP lookup results, showing whether an IP is a VPN, proxy, Tor exit node, datacenter, or anonymous IP.
- Adds rate limit detection for API requests.
- Adds secure API key management with obfuscated keys.

## [0.1.14] (2025-05-14)

### Changed

- Updates Poetry from 2.1.2 to 2.1.3 and refreshes various dependencies to their latest versions.
- Improves user experience when no IP lookup results are found by displaying a warning message with suggestions.

### Fixed

- Fixes handling of sources with errors by properly tracking them as missing sources.

## [0.1.13] (2025-04-21)

### Added

- Adds Tokyo Night theme files for the documentation. Documentation which does not currently exist, but may at some point.

### Changed

- Upgrades `polykit` requirement from >=0.8.0 to >=0.10.2.
- Updates several dependencies including `ruff` (0.11.4 → 0.11.6), `typing-extensions` (4.13.1 → 4.13.2), and `urllib3` (2.3.0 → 2.4.0).
- Updates pre-commit config formatting for consistency, because inconsistent formatting is the root of all evil.

### Fixed

- Fixed compatibility with newer versions of `polykit` now that `handle_interrupt` is in `polykit.cli`.

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
[unreleased]: https://github.com/dannystewart/iplooker/compare/v0.3.3...HEAD
[0.3.3]: https://github.com/dannystewart/iplooker/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/dannystewart/iplooker/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/dannystewart/iplooker/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/dannystewart/iplooker/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/dannystewart/iplooker/compare/v0.1.14...v0.2.0
[0.1.14]: https://github.com/dannystewart/iplooker/compare/v0.1.13...v0.1.14
[0.1.13]: https://github.com/dannystewart/iplooker/compare/v0.1.12...v0.1.13
[0.1.12]: https://github.com/dannystewart/iplooker/compare/v0.1.11...v0.1.12
[0.1.11]: https://github.com/dannystewart/iplooker/compare/v0.1.10...v0.1.11
[0.1.10]: https://github.com/dannystewart/iplooker/compare/v0.1.9...v0.1.10
[0.1.9]: https://github.com/dannystewart/iplooker/releases/tag/v0.1.9
[0.1.8]: https://github.com/dannystewart/iplooker/releases/tag/v0.1.8
