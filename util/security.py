from fastapi import HTTPException
from bson import ObjectId
from passlib.context import CryptContext

from db import get_collection
from util.jwt import verify_access_token
from util.key import key_validiator

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_access(
    token: str, key: str
):
    payload = verify_access_token(token)
    if not payload or not key_validiator(key):
        raise HTTPException(status_code=401, detail="Unauthorized access.")
    
    users = get_collection("users")
    user_id = payload["sub"]
    if not users.find_one({"_id": ObjectId(user_id), "key": key}):
        raise HTTPException(status_code=401, detail="Invalid API key for user.")
    
    return user_id

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_hash(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
