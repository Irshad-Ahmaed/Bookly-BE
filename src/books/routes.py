from typing import List
from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from ..db.main import get_session
from src.books.service import BookService
from src.books.schemas import Book, BookInfo, BookCreateModel, BookUpdateModel
from src.auth.dependencies import AccessTokenBearer, RoleChecker
import uuid

book_router = APIRouter()
book_service = BookService()
role_checker = Depends(RoleChecker(["admin", "user"]))
access_token_bearer = AccessTokenBearer()

@book_router.get('/', response_model=List[Book], status_code=status.HTTP_200_OK, dependencies=[role_checker])
async def get_all_books(session: AsyncSession = Depends(get_session), user_detail_from_token: dict = Depends(access_token_bearer)) -> List[dict]:
    return await book_service.get_all_books(session)


@book_router.get('/user/{user_id}', response_model=List[BookInfo], status_code=status.HTTP_200_OK, dependencies=[role_checker])
async def get_user_books(userID: uuid.UUID, session: AsyncSession = Depends(get_session), user_detail_from_token: dict = Depends(access_token_bearer)) -> List[dict]:
    return await book_service.get_user_books(userID, user_detail_from_token, session)


@book_router.get('/{book_uid}', response_model=BookInfo, status_code=status.HTTP_200_OK, dependencies=[role_checker])
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session), user_detail_from_token: dict = Depends(access_token_bearer)) -> dict:
    return await book_service.get_book(book_uid, session)


@book_router.post('/', response_model=BookInfo, status_code=status.HTTP_201_CREATED, dependencies=[role_checker])
async def create_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session), user_detail_from_token: dict = Depends(access_token_bearer)):
    userID = user_detail_from_token.get('user')['user_id']
    return await book_service.create_book(userID, book_data, session)


@book_router.patch('/{book_uid}', response_model=BookInfo, status_code=status.HTTP_200_OK, dependencies=[role_checker])
async def update_book(book_uid: str, update_data: BookUpdateModel, session: AsyncSession = Depends(get_session), user_detail_from_token: dict = Depends(access_token_bearer)):
    return await book_service.update_book(book_uid, update_data, session)


@book_router.delete('/{book_uid}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session), user_detail_from_token: dict = Depends(access_token_bearer)):
    await book_service.delete_book(book_uid, session)
    return None