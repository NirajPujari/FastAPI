from db import db


def key_validiator(provided_key: str) -> bool:
    db_keys = db["keys"]
    key_entry = db_keys.find_one({"key": provided_key})
    return key_entry is not None