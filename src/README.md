# Docs
- [File Structure](#file-structure)
- [File Details](#file-details)

**Adittional Docs**
- [Database (MongoDB)](db/README.md)
- [Utils (Telethon)](utils/README.md)

## File Structure
Here’s an overview of the `src` directory structure:

```plaintext
📂bot
┗ 📜__init__.py             # Bot setup
📂config
┣ 📜__init__.py 
┣ 📜config.py               # Loads environment variables from .env
┣ 📂logging
┃ ┣ 📜__init__.py           
┃ ┣ 📜logging_config.py     # Sets up logging
┃ ┗ 📜logging_config.yaml   # YAML config for logging
┗ 📂text
  ┣ 📜__init__.py          
  ┣ 📜buttons_text.py       # Keyboard button text templates
  ┣ 📜group_texts.py        # Group message templates
  ┗ 📜private_texts.py      # Private message templates
📂db
┣ 📜__init__.py  
┣ 📜db.py                   # Database operations and classes
┗ 📜schema_validators.py    # MongoDB schema validation           
📂keyboards
┣ 📜__init__.py  
┣ 📜inline_keyboards.py     # Defines inline keyboards
┗ 📜keyboards.py            # Defines reply keyboards       
📂routers
┣ 📜__init__.py  
┣ 📂admin_router
┃ ┣ 📜__init__.py           # Handles special admin messages
┣ 📂callback_router
┃ ┣ 📜__init__.py  
┃ ┣ 📜group_callbacks.py    # Handles group callbacks
┃ ┗ 📜private_callbacks.py  # Handles private chat callbacks         
┗ 📂message_router
  ┣ 📜__init__.py  
  ┣ 📜group_messages.py     # Handles group messages
  ┗ 📜private_messages.py   # Handles private chat messages
📂utils
┣ 📜__init__.py  
┣ 📜telethon_client.py      # Telethon client functions and user entity parsing      
┗ 📜bot_utils.py            # Functions for informing users whether bot started or stopped      

📜main.py                   # Starts the bot
```

## File Details

- [`bot/`](./bot)
  - [`__init__.py`](./bot/__init__.py): This file initializes the `bot`, setting up core functionality like token handling.

- [`config/`](./config)
  - [`logging/`](./config/logging)
    - [`__init__.py`](./config/logging/__init__.py): Initializes the `logging` module for configuration.
    - [`logging_config.py`](config/logging/logging_config.py): Configures Python logging to capture and format log messages.
    - [`logging_config.yaml`](config/logging/logging_config.yaml): Provides a **YAML**-based configuration for more complex logging setups.
  - [`text/`](./config/text)
    - [`__init__.py`](./config/text/__init__.py): Initializes the `text` module for easy import.
    - [`buttons_text.py`](./config/text/buttons_text.py): Stores text templates for keyboard buttons.
    - [`group_texts.py`](./config/text/group_texts.py): Contains group-specific message templates for the bot.
    - [`private_texts.py`](./config/text/private_texts.py): Private chat messages and responses.
  - [`config.py`](./config/config.py): Loads critical environment variables from the `.env` file, such as tokens and database connection strings.
  - [`__init__.py`](./config/logging/__init__.py): Initializes the `config` module.
  
- [`db/`](./db)
  - [`db.py`](./db/db.py): Contains classes and methods for interacting with the **MongoDB** database, handling user and group data.
  - [`schema_validators.py`](./db/schema_validators.py): Defines JSON schemas to validate the structure of documents in **MongoDB** collections.
  - [`__init__.py`](./db/__init__.py): Initializes the `db` module for use across the bot.

- [`keyboards/`](./keyboards)
  - [`inline_keyboards.py`](./keyboards/inline_keyboards.py): Defines inline keyboards that appear within messages, allowing users to interact without sending new messages.
  - [`keyboards.py`](./keyboards/keyboards.py): Contains standard reply keyboards that show up at the bottom of the chat, giving users preset response options.
  - [`__init__.py`](./keyboards/__init__.py): Makes the `keyboards` directory a module, enabling its contents to be easily imported.

- [`routers/`](./routers)
  - [`admin_router/`](./routers/admin_router)
    - [`__init__.py`](./routers/callback_routers/__init__.py): Sets up the `admin_router` module. Manages messages from admin.
  - [`callback_router/`](./routers/callback_router)
    - [`group_callbacks.py`](./routers/callback_routers/group_callbacks.py): Handles callback queries specific to group-related interactions, such as button presses in group chats.
    - [`private_callbacks.py`](./routers/callback_routers/private_callbacks.py): Manages callback queries in private chats, facilitating user-specific interactions.
    - [`__init__.py`](./routers/callback_routers/__init__.py): Sets up the `callback_router` module for use in routing callback queries.
  - [`message_router/`](./routers/message_router)
    - [`group_messages.py`](./routers/message_routers/group_messages.py): Processes and responds to messages sent in group chats, including commands and text messages.
    - [`private_messages.py`](./routers/message_routers/private_messages.py): Handles incoming messages in private chats, providing personalized responses and guidance.
    - [`__init__.py`](./routers/message_routers/__init__.py): Initializes the `message_router` module, integrating message handling across the bot.
  - [`__init__.py`](./routers/__init__.py): Prepares the `routers` directory as a module, linking together all routing logic.

- [`utils/`](./utils)
  - [`telethon_client.py`](./utils/telethon_client.py): Contains Telethon client functions and utilities for parsing user entities.
  - [`bot_utils.py`](./utils/bot_utils.py): Informing users whether bot started or stopped.
  - [`__init__.py`](./utils/__init__.py): Initializes the `utils` module.

- [`main.py`](./main.py): The entry point for the bot. It initializes all components, starts the event loop, and begins processing updates from **Telegram**.