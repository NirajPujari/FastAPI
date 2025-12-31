from datetime import datetime, timezone
from bson import ObjectId
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from type.user import Login, SignUp, User

from db import get_collection
from util.jwt import create_access_token, verify_access_token
from util.security import hash_password, verify_hash
from util.key import generate_user_key, key_validiator

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
api_key_scheme = APIKeyHeader(name="X-API-Key")

@router.post("/signup")
async def create_user(user: SignUp):
    users = get_collection("users")

    if users.find_one({"email": user.email}):
        raise HTTPException(status_code=409, detail="User already exists.")

    user_dict = user.model_dump()
    hassedPassword = hash_password(user_dict["password"])
    time = datetime.now(timezone.utc)

    new_User = User(
        email=user_dict["email"],
        password_hash=hassedPassword,
        is_active=True,
        is_logged_in=False,
        created_at=time,
        updated_at=None,
        last_login=None,
        key=generate_user_key(),
    )

    result = users.insert_one(new_User.model_dump(exclude={"id"}))
    return {
        "key": new_User.key,
        "id": str(result.inserted_id),
        "message": "User created successfully",
    }


@router.post("/login")
async def login(user: Login, key: str = Depends(api_key_scheme)):
    if not key_validiator(key):
        raise HTTPException(status_code=401, detail="Unauthorized access.")

    users = get_collection("users")
    raw_user = users.find_one({"email": user.email})
    if not raw_user:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    db_user = User(id=str(raw_user["_id"]), **raw_user)
    if not verify_hash(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    if db_user.is_logged_in:
        raise HTTPException(status_code=400, detail="User already logged in.")
    
    print(db_user.id)

    token = create_access_token(
        {
            "sub": str(db_user.id),
            "email": db_user.email,
        }
    )
    result = users.update_one(
        {"_id": raw_user["_id"]},
        {"$set": {"last_login": datetime.now(timezone.utc), "is_logged_in": True}},
    )
    print(result)
    return {
        "access_token": token,
        "token_type": "bearer",
    }


# Endpoint to logout a user
@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme), key: str = Depends(api_key_scheme)):
    print(token, "\n", key)
    if not key_validiator(key):
        raise HTTPException(status_code=401, detail="Unauthorized access.")
    
    payload = verify_access_token(token)
    users = get_collection("users")
    blacklisted = get_collection("blacklisted_tokens")
    users.update_one({"_id": ObjectId(payload["sub"])}, {"$set": {"is_logged_in": False}})
    blacklisted.insert_one(
        {
            "token": token,
            "user_id": payload["sub"],
            "revoked_at": datetime.now(timezone.utc),
        }
    )
    return {"message": "User logged out successfully"}
