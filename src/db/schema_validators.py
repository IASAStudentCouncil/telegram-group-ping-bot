class SchemaValidators:
    """Defines JSON schema validators for MongoDB collections used to manage `user` and `group` data within the bot."""

    USER_VALIDATOR = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id", "language"],
            "properties": {
                "_id": {
                    "bsonType": ["int", "long"],
                    "description": ("Unique identifier for the user, typically their Telegram ID. "
                                    "Must be an integer or long type and is required for unique identification.")
                },
                "language": {
                    "bsonType": "string",
                    "enum": ["en", "uk"],
                    "description": ("Specifies the user's preferred language for bot interactions. "
                                    "Ensuring the bot communicates in a supported language.")
                },
            },
            "additionalProperties": False
        }
    }

    GROUP_VALIDATOR = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["_id", "users", "language", "custom_tags"],
            "properties": {
                "_id": {
                    "bsonType": ["int", "long"],
                    "description": ("Unique identifier for the group, usually the Telegram chat ID. "
                                    "This field is essential for distinguishing between different groups.")
                },
                "language": {
                    "bsonType": "string",
                    "enum": ["en", "uk"],
                    "description": ("Defines the default communication language of the group. "
                                    "Required to ensure messages from the bot are understood by the group members.")
                },
                "users": {
                    "bsonType": "array",
                    "description": "List of user objects, each a member of the group with specific settings.",
                    "items": {
                        "bsonType": "object",
                        "required": ["user_id", "can_be_pinged"],
                        "properties": {
                            "user_id": {
                                "bsonType": ["int", "long"],
                                "description": ("The user's unique Telegram ID within the group. "
                                                "Necessary for identifying individual users.")
                            },
                            "can_be_pinged": {
                                "bsonType": "bool",
                                "description": ("Indicating whether the user has opted in to be pinging. "
                                                "This is crucial for respecting user preferences.")
                            }
                        }
                    }
                },
                "custom_tags": {
                    "bsonType": "array",
                    "description": "Stores custom tags for categorizing specific users or topics within the group.",
                    "items": {
                        "bsonType": "object",
                        "required": ["name", "user_ids"],
                        "properties": {
                            "name": {
                                "bsonType": "string",
                                "description": "The name of the custom tag."
                            },
                            "user_ids": {
                                "bsonType": "array",
                                "description": "List of user IDs associated with this tag.",
                                "items": {
                                    "bsonType": ["int", "long"]
                                }
                            }
                        }
                    }
                }
            },
            "additionalProperties": False
        }
    }
