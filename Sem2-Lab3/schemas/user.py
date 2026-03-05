from datetime import datetime
from pydantic import BaseModel, ConfigDict 

class UserCreateSchema(BaseModel):
    username: str
    email: str

class UserUpdateSchema(BaseModel):
    username: str | None = None
    email: str | None = None

class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: str
    created_at: datetime
