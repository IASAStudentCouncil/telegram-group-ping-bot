# Docs
- [File Structure](#file-structure)
- [Details](#file-structure)

## File Structure
Here’s an overview of the `src` directory structure:

```plaintext
📂src
 ┣ 📂bot
 ┃ ┗ 📜__init__.py             # Bot setup
 ┣ 📂config
 ┃ ┣ 📜config.py               # Loads environment variables from .env
 ┃ ┣ 📜logging_config.py       # Sets up logging
 ┃ ┣ 📜logging_config.yaml     # YAML config for logging
 ┃ ┣ 📜text_config.py          # Manages bot messages and text templates
 ┃ ┗ 📜__init__.py             
 ┣ 📂db
 ┃ ┣ 📜db.py                   # Database operations and classes
 ┃ ┣ 📜schema_validators.py    # MongoDB schema validation
 ┃ ┗ 📜__init__.py             
 ┣ 📂keyboards
 ┃ ┣ 📜inline_keyboards.py     # Defines inline keyboards
 ┃ ┣ 📜keyboards.py            # Defines reply keyboards
 ┃ ┗ 📜__init__.py             
 ┣ 📂routers
 ┃ ┣ 📂callback_routers
 ┃ ┃ ┣ 📜group_callbacks.py    # Handles group callbacks
 ┃ ┃ ┣ 📜private_callbacks.py  # Handles private chat callbacks
 ┃ ┃ ┗ 📜__init__.py           
 ┃ ┣ 📂message_routers
 ┃ ┃ ┣ 📜group_messages.py     # Handles group messages
 ┃ ┃ ┣ 📜private_messages.py   # Handles private chat messages
 ┃ ┃ ┗ 📜__init__.py           
 ┃ ┗ 📜__init__.py             
 ┗ 📜main.py                   # Starts the bot
```

## Details

- [`bot/`](./bot/)
  - [`__init__.py`](./bot/__init__.py): This file initializes the bot, setting up core functionality like token handling.

- [`config/`](./config/)
  - [`config.py`](./config/config.py): Loads critical environment variables from the `.env` file, such as tokens and database connection strings.
  - [`logging_config.py`](./config/logging_config.py): Configures Python logging to capture and format log messages.
  - [`logging_config.yaml`](./config/logging_config.yaml): Provides a **YAML**-based configuration for more complex logging setups.
  - [`text_config.py`](./config/text_config.py): Stores text templates, including multilingual support, used by the bot for responses.
  - [`__init__.py`](./config/__init__.py): Prepares the `config` directory as a module for easy import of configuration settings.

- [`db/`](./db/)
  - [`db.py`](./db/db.py): Contains classes and methods for interacting with the **MongoDB** database, handling user and group data.
  - [`schema_validators.py`](./db/schema_validators.py): Defines JSON schemas to validate the structure of documents in **MongoDB** collections.
  - [`__init__.py`](./db/__init__.py): Initializes the `db` module for use across the bot.

- [`keyboards/`](./keyboards/)
  - [`inline_keyboards.py`](./keyboards/inline_keyboards.py): Defines inline keyboards that appear within messages, allowing users to interact without sending new messages.
  - [`keyboards.py`](./keyboards/keyboards.py): Contains standard reply keyboards that show up at the bottom of the chat, giving users preset response options.
  - [`__init__.py`](./keyboards/__init__.py): Makes the `keyboards` directory a module, enabling its contents to be easily imported.

- [`routers/`](./routers/)
  - [`callback_routers/`](./routers/callback_routers/)
    - [`group_callbacks.py`](./routers/callback_routers/group_callbacks.py): Handles callback queries specific to group-related interactions, such as button presses in group chats.
    - [`private_callbacks.py`](./routers/callback_routers/private_callbacks.py): Manages callback queries in private chats, facilitating user-specific interactions.
    - [`__init__.py`](./routers/callback_routers/__init__.py): Sets up the `callback_routers` module for use in routing callback queries.
  - [`message_routers/`](./routers/message_routers/)
    - [`group_messages.py`](./routers/message_routers/group_messages.py): Processes and responds to messages sent in group chats, including commands and text messages.
    - [`private_messages.py`](./routers/message_routers/private_messages.py): Handles incoming messages in private chats, providing personalized responses and guidance.
    - [`__init__.py`](./routers/message_routers/__init__.py): Initializes the `message_routers` module, integrating message handling across the bot.
  - [`__init__.py`](./routers/__init__.py): Prepares the `routers` directory as a module, linking together all routing logic.

- [`main.py`](./main.py): The entry point for the bot. It initializes all components, starts the event loop, and begins processing updates from **Telegram**.
