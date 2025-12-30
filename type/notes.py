from typing import Optional
from pydantic import BaseModel


class Note(BaseModel):
    id: Optional[  str] = None
    user_id: str
    title: str
    content: str
    created_at: str
    updated_at: Optional[str] = None
    shared: list[str] = []
