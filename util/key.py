from db import db
import secrets

def key_validiator(provided_key: str) -> bool:
    db_keys = db["users"]
    key_entry = db_keys.find_one({"key": provided_key})
    return key_entry is not None

def generate_user_key() -> str:
    return secrets.token_hex(128)