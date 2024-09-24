# Database Architecture

## Overview
The `db` directory is a crucial part of the bot's backend, managing interactions with the MongoDB database. 
It contains the logic for handling users and groups within the bot, ensuring efficient querying, schema validation and indexing.

## MongoDB Collections

### 1. `users` collection
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
                "description": "Unique identifier for the user, typically their Telegram ID. Must be an integer or long type and is required for unique identification."
            },
            "language": {
                "bsonType": "string",
                "enum": ["en", "uk"],
                "description": "Specifies the user's preferred language for bot interactions. Ensuring the bot communicates in a supported language."
            }
        }
    }
}
```

### 2. `groups` collection
Maintains information about the groups where the bot is active or have ever been. 
Each document in this collection includes the group’s chat Telegram ID, a list of users within the group, and the group’s language. 
Also, it includes custom tags.

#### Document Structure:

```json
{
  "_id": -987654321000,
  "language": "en",
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
  "custom_tags": [
    {
      "name": "designers",
      "user_ids": [
        123456789,
        101010101
      ]
    }
  ]
}
```

#### Schema Validator:

```json
{
  "$jsonSchema": {
          "bsonType": "object",
          "required": ["_id", "users", "language", "custom_tags"],
          "properties": {
              "_id": {
                  "bsonType": ["int", "long"],
                  "description": "Unique identifier for the group, usually the Telegram chat ID. This field is essential for distinguishing between different groups."
              },
              "language": {
                  "bsonType": "string",
                  "enum": ["en", "uk"],
                  "description": "Defines the default communication language of the group. Required to ensure messages from the bot are understood by the group members."
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
                              "description": "The user's unique Telegram ID within the group. Necessary for identifying individual users."
                          },
                          "can_be_pinged": {
                              "bsonType": "bool",
                              "description": "Indicating whether the user has opted in to be pinging. This is crucial for respecting user preferences."
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
          "additionalProperties": false
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
  - Indexes on `custom_tags.name` and `custom_tags.user_ids` for fast custom tags look up.

## Database Operations
The [`db.py`](db.py) file defines two key classes: `User` and `Group`.
- **User:** Operations such as validating user existence, changing language, and inserting user data in the users collection.
- **Group:** Creation, validation, and update of group data. 
Supports adding and removing users, managing ping permissions, and retrieving user data within groups.

## Schema Validators
The [`schema_validators.py`](schema_validators.py) include both schemas for user and group collections inside `SchemaValidators` class.

## Conclusion
By using MongoDB’s capabilities, the bot can efficiently handle the operations needed for group and user management.