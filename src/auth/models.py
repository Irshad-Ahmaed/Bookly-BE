from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.sql import func
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    __tablename__ = 'users'

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            nullable=False,
            default=uuid.uuid4,
            index=True
        )
    )
    username: str = Field(sa_column=Column(pg.TEXT, nullable=False, index=True))
    email: str = Field(sa_column=Column(pg.TEXT, nullable=False, index=True))
    first_name: str = Field(sa_column=Column(pg.TEXT, nullable=False, index=True))
    last_name: str = Field(sa_column=Column(pg.TEXT, nullable=False, index=True))
    role: str = Field(sa_column=Column(pg.TEXT, nullable=False, index=True, server_default="user"))
    password: str = Field(sa_column=Column(pg.TEXT, nullable=False), exclude=True)
    is_verified: bool = Field(sa_column=Column(pg.BOOLEAN, nullable=False, index=True, default=False))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now()))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), onupdate=func.now(), server_default=func.now()))

    def __repr__(self):
        return f"<User {self.username}>"