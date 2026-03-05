from typing import Sequence
from pydantic import BaseModel, SerializeAsAny

class ErrorSchema(BaseModel):
    message: str

class ResponseSchema(BaseModel):
    success: bool
    data: SerializeAsAny[BaseModel] | SerializeAsAny[Sequence[BaseModel]] | None = None
    error: ErrorSchema | None = None
