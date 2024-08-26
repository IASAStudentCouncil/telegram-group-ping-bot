# Database Architecture

## Overview
The `db` directory is a crucial part of the bot's backend, managing interactions with the MongoDB database. 
This directory contains the logic for handling users and groups within the bot, 
ensuring data consistency and efficient querying through schema validation and indexing.

## MongoDB Collections

### 1. `users` Collection
This collection stores data related to individual users who interact with the bot. Each document represents a user and includes essential fields such as their unique Telegram ID and language preferences.

#### Document Structure:
```json
{
  "_id": 123456789,
  "language": "en"
}
```

#### Schema Validator:
The schema ensures that every document in the users collection 
contains a valid `_id` (user's Telegram ID) and a language field.

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

### 2. groups Collection
This collection maintains information about the groups where the bot is active. 
Each document in this collection includes the group’s ID, a list of users within the group, and the group’s default language.

#### Document Structure:
```json
{
  "_id": 987654321,
  "users": [
    {
      "user_id": 123456789,
      "can_be_pinged": true
    }
  ],
  "language": "en"
}
```

#### Schema Validator:
The schema ensures that each group document includes a valid `_id` (group's Telegram ID), 
a users array containing user IDs and ping permissions, and a language field.

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

### Indexes in users Collection:
Primary Index on `_id`: Ensures that each user's Telegram ID is unique and allows fast lookups.
### Indexes in groups Collection:
Primary Index on `_id`: Guarantees that each group’s Telegram ID is unique.
Compound Index on `users.user_id`: Facilitates efficient querying of users within a group.

## Database Operations
The db.py file defines two key classes: `User` and `Group`.
- **User Class:** Handles operations such as validating user existence, changing language, and inserting or updating user data in the users collection.
- **Group Class:** Manages the creation, validation, and update of group data. Supports adding and removing users, managing ping permissions, and retrieving user data within groups.

## Conclusion
The `db` directory provides a well-structured approach to managing the bot's data, ensuring consistency, performance, and scalability. 
By leveraging MongoDB’s capabilities with proper schema validation and indexing, the bot can efficiently handle the operations needed for group and user management.