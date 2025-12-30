from http.client import HTTPException
from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from db import get_collection
from util.security import verify_access


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="search")
api_key_scheme = APIKeyHeader(name="X-API-Key")


# Endpoint to search the notes
@router.get("/")
async def search_notes(
    q: str,
    token: str = Depends(oauth2_scheme),
    key: str = Depends(api_key_scheme),
):
    user_id = verify_access(token, key)

    if not q.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    notes = get_collection("notes")

    cursor = notes.find(
        {"user_id": user_id, "$text": {"$search": q}},
        {"score": {"$meta": "textScore"}},
    ).sort([("score", {"$meta": "textScore"})])

    results = []
    for note in cursor:
        results.append(
            {
                "id": str(note["_id"]),
                "title": note["title"],
                "content": note["content"],
                "created_at": note["created_at"],
                "updated_at": note.get("updated_at"),
                "shared": note.get("shared", []),
            }
        )

    return {
        "query": q,
        "count": len(results),
        "results": results,
    }
