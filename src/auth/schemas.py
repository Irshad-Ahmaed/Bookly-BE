from typing import List
from pydantic import BaseModel, Field
import uuid
from datetime import datetime

from src.books.schemas import BookInfo


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

class UserBooksModel(UserModel):
    books: List[BookInfo]


class UserLoginModel(BaseModel):
    email: str = Field(max_length=30, min_length=11)
    password: str = Field(min_length=6)