# Changelog
All notable changes to this project will be documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased] - 2024-##-##
### Added
- `CHANGELOG.md` and `CODE_OF_CONDUCT.md` created.
- Ruff code linter integrated.
- `ADMIN_CHAT_ID` added to `.env`.
- "ping-pong" health check for admins.
- New middleware: startup/shutdown messages for user's groups and admin-reports.
- Group size cheacking. Restricting some commands in groups with 500+ users.
- Fetching @everyone / @here in any message.
- More messages templates
### Changed
- License switched from MIT to GNU GPL v3.0.
- Improved `pyproject.toml` and documentation.
### Fixed
- Linted code with Ruff.
- Fixed schema validators and `group` collection indexes.

## [0.6] - 2024-09-01
### Added
- Notes in `.env` for better usage.
- `/admins` and `/getadmins` commands.
- User batching for large groups in `/everyone` and `/here`.
### Changed
- Documentation overhaul.
- Text resources encapsulated in classes.
- Command restrictions for non-admin members.
### Fixed
- Telethon integration for improved bot interactions.

## [0.5] - 2024-08-28
### Added
- `.env` setup instructions.
- `assets` directory for project assets like the logo.
- Full documentation for `utils` and `db` modules.
### Changed
- Reorganized file structure for clarity.
- Telethon integrated for enhanced Telegram bot functionality.
- Improved text storage for multi-language support.
### Fixed
- Database optimizations in `User` and `Group` classes.

## [0.4] - 2024-08-24
### Added
- Detailed documentation for `src` directory.
- Chat ID migration handling in `group_messages.py`.
- New messages in `text_config.py`.
- Error logging in `User` and `Group` classes.
### Changed
- README.md improvements.
- Small function updates.

## [0.3.5] - 2024-08-21
### Added
- Group event handlers.
- `Group` class in `db.py`.
### Changed
- Moved `dispatcher` to `main.py`.
- Refactored `private_messages.py`.
- Updated directory structure and `pyproject.toml`.
### Fixed
- Adjusted logging format and removed unnecessary directories.

## [0.2] - 2024-08-19
### Added
- New callback routers and group command handlers.
- Proper MongoDB connection handling.
### Changed
- Switched "language change" keyboard to inline markup.
- Reorganized `routers` directory.
- Schema validators and logging improved.
- Upgraded `aiogram` from 3.11 to 3.12.
### Fixed
- Cleaned up `.gitignore` and added comments across project.

## [0.1] - 2024-08-16
### Added
- Project files: `.env`, `.gitignore`, `LICENSE`, `pyproject.toml`, `README.md`, `requirements.txt`.
- Initial MongoDB integration.
- Command handlers for `/ping` and `/help`.
- Basic bot polling with `aiogram`.
### Changed
- Refined `logging_config.yaml`.
- Log levels for development, staging, and production.
### Fixed
- MongoDB connection and error logging.
- Loggers for `pymongo`, `motor`, and `asyncio`.