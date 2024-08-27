# Database Architecture

## Overview
The `db` directory is a crucial part of the bot's backend, managing interactions with the MongoDB database. 
It contains the logic for handling users and groups within the bot, ensuring efficient querying, schema validation and indexing.

## MongoDB Collections

### 1. `users` Collection
This collection stores data related to individual users who interact with the bot in private chats. 
Each document represents a user and includes their unique Telegram ID and language preferences.

#### Document Structure:
```json
{
  "_id": 123456789,
  "language": "en"
}
```

#### Schema Validator:
```json
{
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["_id", "language"],
        "properties": {
            "_id": {
                "bsonType": ["int", "long"],
                "description": "Must be int or long and is required"
            },
            "language": {
                "bsonType": "string",
                "description": "Must be a string and is required"
            }
        }
    }
}
```

### 2. `groups` Collection
Maintains information about the groups where the bot is active or have ever been. 
Each document in this collection includes the group’s chat Telegram ID, a list of users within the group, and the group’s language.

#### Document Structure:
```json
{
  "_id": -987654321000,
  "users": [
    {
      "user_id": 123456789,
      "can_be_pinged": true
    },
    {
      "user_id": 101010101,
      "can_be_pinged": false
    }
  ],
  "language": "en"
}
```

#### Schema Validator:

```json
{
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["_id", "users", "language"],
        "properties": {
            "_id": {
                "bsonType": ["int", "long"],
                "description": "Must be int or long and is required"
            },
            "users": {
                "bsonType": "array",
                "description": "Must be an array of users and is required",
                "items": {
                    "bsonType": "object",
                    "required": ["user_id", "can_be_pinged"],
                    "properties": {
                        "user_id": {
                            "bsonType": ["int", "long"],
                            "description": "Must be int or long and is required"
                        },
                        "can_be_pinged": {
                            "bsonType": "bool",
                            "description": "Must be a boolean indicating if the user can be pinged"
                        }
                    }
                }
            },
            "language": {
                "bsonType": "string",
                "description": "Must be a string and is required"
            }
        }
    }
}
```

## Indexing Strategy
The database uses indexing to enhance performance, especially for queries related to user and group management.

- **Indexes in `users` collection:**
    - Primary Index on `_id`: Ensures and allows fast lookups.
- **Indexes in `groups` collection:**
  - Primary Index on `_id`: Guarantees that each group’s Telegram ID is unique.
  - Compound Index on `users.user_id`: Efficient querying of users within a group.

## Database Operations
The [`db.py`](db.py) file defines two key classes: `User` and `Group`.
- **User:** Operations such as validating user existence, changing language, and inserting user data in the users collection.
- **Group:** Creation, validation, and update of group data. 
Supports adding and removing users, managing ping permissions, and retrieving user data within groups.

## Conclusion
By using MongoDB’s capabilities, the bot can efficiently handle the operations needed for group and user management.