import uuid

# Temporary in-memory storage
api_keys_db = {}

def create_api_key(store_name):
    key = str(uuid.uuid4())
    api_keys_db[key] = {
        "store": store_name,
        "usage": 0,
        "limit": 50  # free plan limit
    }
    return key

def validate_api_key(key):
    return api_keys_db.get(key)

def increment_usage(key):
    if key in api_keys_db:
        api_keys_db[key]["usage"] += 1
