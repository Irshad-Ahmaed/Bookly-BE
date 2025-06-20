from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from sqlalchemy.exc import SQLAlchemyError
from .schemas import BookCreateModel, BookUpdateModel
from .models import Book


class BookService:

    async def get_all_books(self, session: AsyncSession):
        try:
            statement = select(Book).order_by(desc(Book.created_at))
            result = await session.exec(statement)
            return result.all()
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch books")

    async def get_book(self, book_uid: str, session: AsyncSession):
        try:
            statement = select(Book).where(Book.uid == book_uid)
            result = await session.exec(statement)
            book = result.first()
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
            return book
        except SQLAlchemyError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch book")

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        try:
            new_book = Book(**book_data.model_dump())
            session.add(new_book)
            await session.commit()
            await session.refresh(new_book)
            return new_book
        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create book")

    async def update_book(self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession):
        try:
            book_to_update = await self.get_book(book_uid, session)
            for key, value in update_data.model_dump(exclude_unset=True).items():
                setattr(book_to_update, key, value)
            await session.commit()
            await session.refresh(book_to_update)
            return book_to_update
        except HTTPException:
            raise
        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update book")

    async def delete_book(self, book_uid: str, session: AsyncSession):
        try:
            book_to_delete = await self.get_book(book_uid, session)
            await session.delete(book_to_delete)
            await session.commit()
            return {"detail": "Book deleted successfully"}
        except HTTPException:
            raise
        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete book")
