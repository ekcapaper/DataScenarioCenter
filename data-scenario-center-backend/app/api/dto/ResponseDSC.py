from typing import TypeVar, Generic, Optional
from pydantic import BaseModel
from app.api.dto.CamelModel import CamelModel

T = TypeVar('T')

class ResponseDSC(CamelModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
