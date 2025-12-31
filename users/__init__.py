from datetime import datetime, timezone
from fastapi import HTTPException
from bson import ObjectId
from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from type.user import GetUser, UpdateUser

from db import get_collection
from util.key import generate_user_key
from util.security import hash_password, verify_access

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="notes")
api_key_scheme = APIKeyHeader(name="X-API-Key")


# Endpoint to fetch a specific user data by ID
@router.get("")
def get_user(
    token: str = Depends(oauth2_scheme), key: str = Depends(api_key_scheme)
):
    user_id = verify_access(token, key)
    users = get_collection("users")
    user = users.find_one({"_id": ObjectId(user_id)})
    if not user or not user.get("is_active", True):
        raise HTTPException(status_code=404, detail="User not found.")
    user["id"] = str(user["_id"])
    del user["_id"]
    return GetUser(**user)


# Endpoint to update a specific user data by ID
@router.put("")
def update_user(
    updated_user: UpdateUser,
    token: str = Depends(oauth2_scheme),
    key: str = Depends(api_key_scheme),
):
    user_id = verify_access(token, key)
    users = get_collection("users")
    if updated_user.email:
        existing_user = users.find_one({"email": updated_user.email})
        if existing_user and str(existing_user["_id"]) != user_id:
            raise HTTPException(status_code=400, detail="Email already exists.")
    if updated_user.password:
        updated_user.password = hash_password(updated_user.password)
        
    update_user = updated_user.model_dump(exclude_unset=True)
    update_user["updated_at"] = datetime.now(timezone.utc)
    update_user["password_hash"] = updated_user.password
    del update_user["password"]
    if not update_user:
        raise HTTPException(status_code=400, detail="No fields to update.")
    
    result = users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_user},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found.")
    return {"message": "User updated successfully."}


# Endpoint to delete a specific user data by ID
@router.delete("")
def delete_user(
    token: str = Depends(oauth2_scheme), key: str = Depends(api_key_scheme)
):
    user_id = verify_access(token, key)
    users = get_collection("users")
    result = users.update_one(
        {"_id": ObjectId(user_id)}, {"$set": {"is_active": False}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found.")
    return {"message": "User deleted successfully."}
