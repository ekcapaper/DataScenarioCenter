from typing import TypeVar, Generic, Optional
from pydantic import BaseModel

T = TypeVar('T')

class ResponseDSC(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
