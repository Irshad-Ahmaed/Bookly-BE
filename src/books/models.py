from sqlmodel import SQLModel, Column, Field
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
from sqlalchemy.sql import func
import uuid

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
    published_date: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.date, nullable=False))
    page_count: int = Field(sa_column=Column(pg.INTEGER, nullable=False))
    language: str = Field(sa_column=Column(pg.TEXT, nullable=False))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now()))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), onupdate=func.now(), server_default=func.now()))

    def __repr__(self):
        return f"<Book {self.title}>"