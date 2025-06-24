from sqlmodel import SQLModel, Column, Field, ForeignKey, func
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid
from typing import Optional

class Book(SQLModel, table=True):

    __tablename__ = 'books'

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            nullable=False,
            default=uuid.uuid4,
            index=True
        )
    )
    title: str = Field(sa_column=Column(pg.TEXT, nullable=False, index=True))
    author: str = Field(sa_column=Column(pg.TEXT, nullable=False, index=True))
    publisher: str = Field(sa_column=Column(pg.TEXT, nullable=False, index=True))
    published_date: datetime = Field(sa_column=Column(pg.DATE, nullable=False))
    page_count: int = Field(sa_column=Column(pg.INTEGER, nullable=False))
    language: str = Field(sa_column=Column(pg.TEXT, nullable=False))
    user_id: Optional[uuid.UUID] = Field(sa_column=Column(pg.UUID, ForeignKey("users.id"), nullable=True), default=None)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now(), nullable=False), default_factory=datetime.utcnow,)
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), server_onupdate=func.now(), server_default=func.now(), nullable=False), default_factory=datetime.utcnow,)

    def __repr__(self):
        return f"<Book {self.title}>"