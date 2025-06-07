# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Enhanced button clicking functionality:
  - Support for clicking buttons by text (case-insensitive)
  - Support for clicking buttons by position (row/column)
  - Optional message ID parameter (defaults to last message)
  - Better error handling and feedback
- Improved documentation:
  - Comprehensive command reference
  - JSON output format examples
  - Multiple usage examples for each command
  - Clear explanation of optional parameters

### Changed
- Made `--msg-id` parameter optional in `click-button` command
- Improved button text matching to be case-insensitive
- Enhanced error messages for better user feedback
- Updated README with detailed command documentation

### Fixed
- Fixed button clicking in second row and beyond
- Corrected Telethon button click implementation
- Fixed handling of @ prefix in button text

## [0.1.0] - 2024-03-19

### Added
- Initial release
- Basic CLI interface for BotFather interaction
- Session management and authentication
- Message sending and receiving
- Button clicking functionality
- Project documentation and structure

## v2.0.1 (June 2025) — Workspace Cleanup & Flattening
- Moved `