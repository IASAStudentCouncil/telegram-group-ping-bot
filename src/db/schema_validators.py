# Validator schema for the "users" collection in MongoDB
user_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["_id", "username", "first_name", "language"],
        "properties": {
            "_id": {
                "bsonType": ["int", "long"],
                "description": "Must be int or long and is required"
            },
            "username": {
                "bsonType": ["string", "null"],
                "description": "Must be a string or null and is required"
            },
            "first_name": {
                "bsonType": "string",
                "description": "Must be a string and is required"
            },
            "language": {
                "bsonType": "string",
                "description": "Must be a string and is required"
            }
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

"""
"subgroups": {
    "bsonType": "array",
    "description": "Must be an array of subgroups and is required",
    "items": {
        "bsonType": "object",
        "required": ["subgroup_name", "users"],
        "properties": {
            "names": {
                "bsonType": "string",
                "description": "Must be a string representing the subgroup name"
            },
            "users": {
                "bsonType": "array",
                "description": "Must be an array of user IDs",
                "items": {
                    "bsonType": "int",
                    "description": "Each item must be a string representing a user ID"
                }
            }
        }
    }
}
"""