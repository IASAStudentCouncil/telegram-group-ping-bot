# Validator schema for the "users" collection in MongoDB
user_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["_id", "language"],
        "properties": {
            "_id": {
                "bsonType": ["int", "long"],
                "description": "Must be an integer or long and is required."
            },
            "language": {
                "bsonType": "string",
                "description": "The preferred language of the user. Must be a valid language code and is required."
            },
        }
    }
}

# Validator schema for the "groups" collection in MongoDB
group_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["_id", "users", "language"],
        "properties": {
            "_id": {
                "bsonType": ["int", "long"],
                "description": "Must be an integer or long and is required."
            },
            "users": {
                "bsonType": "array",
                "description": "An array of user objects. Must be an array and is required.",
                "items": {
                    "bsonType": "object",
                    "required": ["user_id", "can_be_pinged"],
                    "properties": {
                        "user_id": {
                            "bsonType": ["int", "long"],
                            "description": "Must be an integer or long and is required."
                        },
                        "can_be_pinged": {
                            "bsonType": "bool",
                            "description": "Indicates if the user can be pinged. Must be a boolean and is required."
                        }
                    }
                }
            },
            "language": {
                "bsonType": "string",
                "description": "The default language of the group. Must be a valid language code and is required."
            }
        },
        "additionalProperties": False
    }
}
