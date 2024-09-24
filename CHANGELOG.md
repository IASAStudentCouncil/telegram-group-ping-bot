# Changelog
All notable changes to this project will be documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.7] - 2024-09-24
### Added
- `CHANGELOG.md` and `CODE_OF_CONDUCT.md`.
- Ruff linter integrated.
- `ADMIN_CHAT_ID` added to `.env`.
- Health check for admins ("ping-pong").
- Middleware for startup/shutdown messages and admin reports.
- Group size checking (restrictions for 500+ users).
- Additional message templates.
### Changed
- License updated to GNU GPL v3.0.
- Improved `pyproject.toml` and documentation.
### Fixed
- Linted code with Ruff.
- Schema validators and `group` collection indexes.

## [0.6] - 2024-09-01
### Added
- Notes in `.env` for better usage.
- `/admins` and `/getadmins` commands.
- User batching for large groups in `/everyone` and `/here`.
- Telethon integration 
### Changed
- Documentation overhaul.
- Text resources encapsulated in classes.
- Command restrictions for non-admins.

## [0.5] - 2024-08-28
### Added
- `.env` setup instructions.
- `assets` directory for project assets.
- Full documentation for `utils` and `db`.
### Changed
- Reorganized file structure.
- Multi-language support improvements.
### Fixed
- Database optimizations in `User` and `Group` classes.

## [0.4] - 2024-08-24
### Added
- Documentation for `src`.
- Chat ID migration handling.
- New messages in `text_config.py`.
### Changed
- README improvements.
- Function updates.
### Fixed
- Error logging in `User` and `Group` classes.

## [0.3.5] - 2024-08-21
### Added
- Group event handlers.
- `Group` class in `db.py`.
### Changed
- Moved `dispatcher` to `main.py`.
- Refactored `private_messages.py`.
### Fixed
- Adjusted logging format.

## [0.2] - 2024-08-19
### Added
- Callback routers and group command handlers.
- MongoDB connection handling.
### Changed
- Switched "language change" keyboard to inline markup.
- Reorganized `routers`.
### Fixed
- Logging and schema validators.

## [0.1] - 2024-08-16
### Added
- Initial project files (`.env`, `.gitignore`, `LICENSE`, `README.md`).
- MongoDB integration.
- Basic bot polling with `aiogram`.
### Fixed
- MongoDB connection and logging issues.