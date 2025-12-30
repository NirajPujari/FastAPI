from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Note(BaseModel):
    id: Optional[str] = None
    user_id: str
    title: str
    content: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    shared: list[str] = []

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    shared: Optional[list[str]] = None