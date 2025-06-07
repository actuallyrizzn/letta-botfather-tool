# Changelog

## v2.0.0 (June 2025) — CLI-Only Refactor
- Major refactor: removed all FastAPI, Uvicorn, and web server code.
- Project is now a single, modular CLI tool using `argparse`.
- All BotFather actions (send message, get replies, authentication) are available as CLI subcommands.
- No concurrency: robust for one-off use, no "database is locked" errors.
- Telethon session access is fully serialized via a global asyncio.Lock.
- All legacy API, route, and test files removed.
- Documentation and project plans updated to reflect new architecture.
- Created to prepare for MCP-ization of the project.

## v1.2.0 (May 2025) — Dockerization & Concurrency Audit
- Added Docker support and documentation for running the relay in containers.
- Identified and documented Telethon/SQLite concurrency issues.
- Added project plan for global request queue/lock to serialize Telethon access.
- Updated README and onboarding docs with concurrency guard instructions.

## v1.1.0 (April 2025) — API Improvements & Security
- Improved error handling and logging in the FastAPI relay.
- Added bearer token authentication and rate limiting.
- Enhanced session management and troubleshooting documentation.

## v1.0.0 (March 2025) — Initial Release
- FastAPI-based relay for provisioning Telegram bots via BotFather.
- Telethon client for session management and message relay.
- Python function and CLI for sending messages to BotFather.
- Basic test suite and usage documentation. 