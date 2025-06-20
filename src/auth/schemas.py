from pydantic import BaseModel, Field
import uuid
from datetime import datetime


class UserCreateModel(BaseModel):
    username: str = Field(max_length=10)
    email: str = Field(max_length=30, min_length=11)
    first_name: str = Field(max_length=20)
    last_name: str = Field(max_length=20)
    password: str = Field(min_length=6)

class UserModel(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime