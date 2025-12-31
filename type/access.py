from typing import TypedDict, Union

from bson import ObjectId


class AccessError(TypedDict):
    error: str
    status_code: int

AccessResult = Union[ObjectId, AccessError]