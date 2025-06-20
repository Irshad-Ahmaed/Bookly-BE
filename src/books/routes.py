from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from ..db.main import get_session
from src.books.service import BookService
from src.books.schemas import Book, BookInfo, BookCreateModel, BookUpdateModel

book_router = APIRouter()
book_service = BookService()


@book_router.get('/', response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_all_books(session: AsyncSession = Depends(get_session)):
    return await book_service.get_all_books(session)


@book_router.get('/{book_uid}', response_model=BookInfo, status_code=status.HTTP_200_OK)
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    return await book_service.get_book(book_uid, session)


@book_router.post('/', response_model=BookInfo, status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session)):
    return await book_service.create_book(book_data, session)


@book_router.patch('/{book_uid}', response_model=BookInfo, status_code=status.HTTP_200_OK)
async def update_book(book_uid: str, update_data: BookUpdateModel, session: AsyncSession = Depends(get_session)):
    return await book_service.update_book(book_uid, update_data, session)


@book_router.delete('/{book_uid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    await book_service.delete_book(book_uid, session)
    return None