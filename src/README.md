## File Structure
Here’s an overview of the `src` directory structure:

```plaintext
📂src
 ┣ 📂bot
 ┃ ┗ 📜__init__.py             # Initializes the bot module.
 ┣ 📂config
 ┃ ┣ 📜config.py               # Bot configuration settings.
 ┃ ┣ 📜logging_config.py       # Logging configuration.
 ┃ ┣ 📜logging_config.yaml     # YAML file for logging configuration.
 ┃ ┣ 📜text_config.py          # Text templates and messages.
 ┃ ┗ 📜__init__.py             # Initializes the config module.
 ┣ 📂db
 ┃ ┣ 📜db.py                   # Database operations and classes.
 ┃ ┣ 📜schema_validators.py    # MongoDB schema validators.
 ┃ ┗ 📜__init__.py             # Initializes the db module.
 ┣ 📂keyboards
 ┃ ┣ 📜inline_keyboards.py     # Inline keyboard definitions.
 ┃ ┣ 📜keyboards.py            # General keyboard definitions.
 ┃ ┗ 📜__init__.py             # Initializes the keyboards module.
 ┣ 📂routers
 ┃ ┣ 📂callback_routers
 ┃ ┃ ┣ 📜group_callbacks.py    # Group callback handlers.
 ┃ ┃ ┣ 📜private_callbacks.py  # Private chat callback handlers.
 ┃ ┃ ┗ 📜__init__.py           # Initializes the callback routers module.
 ┃ ┣ 📂message_routers
 ┃ ┃ ┣ 📜group_messages.py     # Group message handlers.
 ┃ ┃ ┣ 📜private_messages.py   # Private chat message handlers.
 ┃ ┃ ┗ 📜__init__.py           # Initializes the message routers module.
 ┃ ┗ 📜__init__.py             # Initializes the routers module.
 ┗ 📜main.py                   # Main entry point for the bot.
```