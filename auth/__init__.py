from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Header
from db import get_collection
from type.user import Login, SignUp
from util.jwt import create_access_token, verify_access_token
from util.password import hash_password, verify_hash
from util.key import key_validiator

router = APIRouter()


@router.post("/signup")
async def create_user(user: SignUp):
    users = get_collection("users")

    if users.find_one({"email": user.email}):
        raise HTTPException(status_code=409, detail="User already exists.")

    user_dict = user.model_dump()
    user_dict["password"] = hash_password(user_dict["password"])

    user_dict.update(
        {
            "is_active": True,
            "is_logged_in": False,
            "created_at": datetime.now(timezone.utc),
            "updated_at": None,
            "last_login": None,
            "key": user_dict["password"] + str(datetime.now(timezone.utc)),
        }
    )
    users.insert_one(user_dict)
    return {
        "key": user_dict["key"],
        "message": "User created successfully",
    }


@router.post("/login")
async def login(user: Login, key: str = Header(None)):
    if not key_validiator(key):
        raise HTTPException(status_code=401, detail="Unauthorized access.")

    users = get_collection("users")
    db_user = users.find_one({"email": user.email})

    if not db_user or not verify_hash(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    token = create_access_token(
        {
            "sub": str(db_user["_id"]),
            "email": db_user["email"],
        }
    )
    users.update_one(
        {"_id": db_user["_id"]},
        {"$set": {"last_login": datetime.now(timezone.utc), "is_logged_in": True}},
    )
    return {
        "access_token": token,
        "token_type": "bearer",
    }


# Endpoint to logout a user
@router.post("/logout")
async def logout(token: str, key: str = Header(None)):
    if not key_validiator(key):
        raise HTTPException(status_code=401, detail="Unauthorized access.")

    users = get_collection("users")
    blacklisted = get_collection("blacklisted_tokens")
    payload = verify_access_token(token)
    users.update_one({"key": key}, {"$set": {"is_logged_in": False}})
    blacklisted.insert_one(
        {
            "token": token,
            "user_id": payload["sub"],
            "revoked_at": datetime.now(timezone.utc),
        }
    )
    return {"message": "User logged out successfully"}
