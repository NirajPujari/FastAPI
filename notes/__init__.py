from datetime import datetime, timezone
from bson import ObjectId
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from db import get_collection
from type.notes import Note, NoteCreate, NoteUpdate
from util.security import verify_access

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="notes")
api_key_scheme = APIKeyHeader(name="X-API-Key")


# Endpoint to create a new note
@router.post("")
async def create_note(
    note: NoteCreate,
    token: str = Depends(oauth2_scheme),
    key: str = Depends(api_key_scheme),
):
    user_id = verify_access(token, key)
    notes = get_collection("notes")
    new_note = Note(
        user_id=user_id,
        title=note.title,
        content=note.content,
        created_at=datetime.now(timezone.utc),
        updated_at=None,
        shared=[],
    )
    result = notes.insert_one(new_note.model_dump(exclude={"id"}))
    return {
        "id": str(result.inserted_id),
        "message": "Note created successfully",
    }


# Endpoint to create a new notes
@router.post("/bulk")
async def create_notes(
    note: list[NoteCreate],
    token: str = Depends(oauth2_scheme),
    key: str = Depends(api_key_scheme),
):
    user_id = verify_access(token, key)
    notes = get_collection("notes")
    new_notes = []
    time = datetime.now(timezone.utc)
    for n in note:
        new_note = Note(
            user_id=user_id,
            title=n.title,
            content=n.content,
            created_at=time,
            updated_at=None,
            shared=[],
        )
        new_notes.append(new_note.model_dump(exclude={"id"}))
    result = notes.insert_many(new_notes)
    return {
        "ids": [str(id) for id in result.inserted_ids],
        "message": "Notes created successfully",
    }


# Endpoint to fetch a specific note by ID
@router.get("/{id}")
async def get_note(
    id: str, token: str = Depends(oauth2_scheme), key: str = Depends(api_key_scheme)
):
    user_id = verify_access(token, key)
    notes = get_collection("notes")

    note = notes.find_one({"_id": ObjectId(id), "user_id": user_id})
    if not note:
        raise HTTPException(status_code=404, detail="Note not found.")

    note["id"] = str(note["_id"])
    del note["_id"]
    return Note(**note)


# Endpoint to fetch all the notes
@router.get("")
async def get_notes(
    token: str = Depends(oauth2_scheme), key: str = Depends(api_key_scheme)
):
    user_id = verify_access(token, key)
    notes = get_collection("notes")

    user_notes = notes.find({"user_id": user_id}).sort({"created_at": -1})
    shared_notes = notes.find({"shared": user_id}).sort({"created_at": -1})
    user_notes = list(user_notes) + list(shared_notes)
    result = []
    for note in user_notes:
        note["id"] = str(note["_id"])
        del note["_id"]
        result.append(Note(**note))

    return result


# Endpoint to update a specific note by ID
@router.put("/{id}")
async def update_note(
    id: str,
    note: NoteUpdate,
    token: str = Depends(oauth2_scheme),
    key: str = Depends(api_key_scheme),
):
    user_id = verify_access(token, key)
    notes = get_collection("notes")
    users = get_collection("users")

    # Check if the note exists and belongs to the user
    existing_note = notes.find_one({"_id": ObjectId(id), "user_id": user_id})
    if not existing_note:
        raise HTTPException(status_code=404, detail="Note not found.")

    if not (note.title or note.content or note.shared):
        raise HTTPException(status_code=400, detail="No fields to update provided.")

    if note.shared:
        for share_with_user_id in note.shared:
            # Check if the user to share with exists
            share_with_user = users.find_one({"_id": ObjectId(share_with_user_id)})
            if not share_with_user:
                raise HTTPException(
                    status_code=404, detail="User to share with not found."
                )
            if share_with_user_id in note.get("shared", []):
                raise HTTPException(
                    status_code=400, detail="Note already shared with this user."
                )

    # Update the note
    updated_note = Note(
        id=id,
        user_id=user_id,
        title=note.title if note.title is not None else existing_note["title"],
        content=note.content if note.content is not None else existing_note["content"],
        created_at=existing_note["created_at"],
        updated_at=datetime.now(timezone.utc),
        shared=existing_note.get("shared", [])
        + (note.shared if note.shared is not None else []),
    )

    notes.update_one(
        {"_id": ObjectId(id)}, {"$set": updated_note.model_dump(exclude={"id"})}
    )

    return {"message": "Note updated successfully."}


# Endpoint to update notes in bulk
@router.put("/bulk")
async def update_notes(
    notes: list[NoteUpdate],
    ids: list[str],
    token: str = Depends(oauth2_scheme),
    key: str = Depends(api_key_scheme),
):
    if len(notes) != len(ids):
        raise HTTPException(
            status_code=400, detail="Mismatch between notes and IDs count."
        )

    user_id = verify_access(token, key)
    notes_collection = get_collection("notes")
    users = get_collection("users")
    time = datetime.now(timezone.utc)

    for i in range(len(ids)):
        id = ids[i]
        note = notes[i]

        # Check if the note exists and belongs to the user
        existing_note = notes_collection.find_one(
            {"_id": ObjectId(id), "user_id": user_id}
        )
        if not existing_note:
            raise HTTPException(status_code=404, detail=f"Note with ID {id} not found.")

        if note.shared:
            for share_with_user_id in note.shared:
                # Check if the user to share with exists
                share_with_user = users.find_one({"_id": ObjectId(share_with_user_id)})
                if not share_with_user:
                    raise HTTPException(
                        status_code=404, detail="User to share with not found."
                    )
                if share_with_user_id in note.get("shared", []):
                    raise HTTPException(
                        status_code=400, detail="Note already shared with this user."
                    )

        # Update the note
        updated_note = Note(
            id=id,
            user_id=user_id,
            title=note.title if note.title is not None else existing_note["title"],
            content=(
                note.content if note.content is not None else existing_note["content"]
            ),
            created_at=existing_note["created_at"],
            updated_at=time,
            shared=existing_note.get("shared", [])
            + (note.shared if note.shared is not None else []),
        )

        notes_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": updated_note.model_dump(exclude={"id"})}
        )

    return {"message": "Notes updated successfully."}


# Endpoint to delete a specific note by ID
@router.delete("/{id}")
async def delete_note(
    id: str, token: str = Depends(oauth2_scheme), key: str = Depends(api_key_scheme)
):
    user_id = verify_access(token, key)
    notes = get_collection("notes")

    result = notes.delete_one({"_id": ObjectId(id), "user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found.")

    return {"message": "Note deleted successfully."}


# Endpoint to note between user
@router.post("/share/{id}/{share_with_user_id}")
async def share_note(
    id: str,
    share_with_user_id: str,
    token: str = Depends(oauth2_scheme),
    key: str = Depends(api_key_scheme),
):
    user_id = verify_access(token, key)
    notes = get_collection("notes")
    users = get_collection("users")

    # Check if the note exists and belongs to the user
    note = notes.find_one({"_id": ObjectId(id), "user_id": user_id})
    if not note:
        raise HTTPException(status_code=404, detail="Note not found.")

    # Check if the user to share with exists
    share_with_user = users.find_one({"_id": ObjectId(share_with_user_id)})
    if not share_with_user:
        raise HTTPException(status_code=404, detail="User to share with not found.")

    # Update the note's shared list
    if share_with_user_id in note.get("shared", []):
        raise HTTPException(
            status_code=400, detail="Note already shared with this user."
        )

    notes.update_one({"_id": ObjectId(id)}, {"$push": {"shared": share_with_user_id}})

    return {"message": "Note shared successfully."}


# Endpoint to remove sharing of note between user
@router.post("/unshare/{id}/{share_with_user_id}")
async def unshare_note(
    id: str,
    share_with_user_id: str,
    token: str = Depends(oauth2_scheme),
    key: str = Depends(api_key_scheme),
):
    user_id = verify_access(token, key)
    notes = get_collection("notes")
    users = get_collection("users")

    # Check if the note exists and belongs to the user
    note = notes.find_one({"_id": ObjectId(id), "user_id": user_id})
    if not note:
        raise HTTPException(status_code=404, detail="Note not found.")

    # Check if the user to unshare with exists
    share_with_user = users.find_one({"_id": ObjectId(share_with_user_id)})
    if not share_with_user:
        raise HTTPException(status_code=404, detail="User to unshare with not found.")

    # Update the note's shared list
    if share_with_user_id not in note.get("shared", []):
        raise HTTPException(
            status_code=400, detail="Note is not shared with this user."
        )

    notes.update_one({"_id": ObjectId(id)}, {"$pull": {"shared": share_with_user_id}})

    return {"message": "Note unshared successfully."}
