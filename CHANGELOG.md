# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [v0.7] - 2023-09-22
### Added
- Created CHANGELOG.md
- Add Ruff code linter
### Changed
- Switch from MIT License to GNU GENERAL PUBLIC LICENSE
- Structured [pyproject.py](pyproject.toml)
### Fixed
- Linted code with [ruff](https://astral.sh/ruff)
- Schema validators for `group` collection

## [v0.6] - 2023-08-22
### Added
- Added critical notes to the `.env` file for better clarity and usage.
- Introduced `/admins` and `/getadmins` commands for efficient admin management.
- Integrated Telethon client for enhanced Telegram bot interactions.
### Changed
- Refined and restructured text resources, encapsulating them into classes for better maintainability.
- Structured the documentation to reflect new changes and integrations.
### Fixed
- Performance optimizations for `/everyone` and `/here` commands to handle larger groups more efficiently.

## [v0.5] - 2023-08-19
### Added
- Introduced a new `assets` directory to store project assets, including the logo.
- Comprehensive documentation for `utils` and `db` modules.
### Changed
- Refined configuration management for logging and bot settings.
- Reorganized project file structure for better maintainability and readability.
### Fixed
- Improved database methods in the `User` and `Group` classes.

## [v0.4] - 2023-08-18
### Added
- Functionality in `group_messages.py` to manage chat ID migration when a group is upgraded to a supergroup or migrated.
### Changed
- Documentation and structure of the `src` directory for clarity.
- New messages added in `text_config.py`.
### Fixed
- Error logging in `User` and `Group` classes in `db.py`.

## [v0.3.5] - 2023-08-17
### Added
- Added handlers for group events.
- Added `Group` class to `db.py` for managing group data.
### Changed
- Improved comments and directory naming for better structure.
### Fixed
- Adjusted logging date format.

## [v0.3] - 2023-08-12
### Added
- MongoDB connection and logging configuration improvements.
### Changed
- Improved `logging_config.yaml` and set different log levels for environments.
- Enhanced bot polling functionality using `aiogram`.
### Fixed
- Connection issues to MongoDB with better logging for troubleshooting.

## [v0.2] - 2023-08-10
### Added
- Group-specific commands for better event handling in group chats.
### Changed
- Schema validators for MongoDB data validation.
- Directory reorganization for better code clarity.
### Fixed
- Errors in group commands mistakenly used in private chats.

## [v0.1] - 2023-08-08
### Added
- Initial release with MongoDB interaction.
- Basic command handlers for `/ping` and `/help`.
- Basic bot polling functionality using `aiogram`, allowing the bot to start receiving and responding to user messages.
### Changed
- Refined the `logging_config.yaml` file.
- Implemented different log levels for development, staging, and production environments.
### Fixed
- Established a reliable connection to MongoDB, ensuring smooth interaction with the database.
- Added logic to handle potential connection issues and provide informative logging for troubleshooting.
- Added specific loggers for `pymongo`, `motor`, and `asyncio`.

