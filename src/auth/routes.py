from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import UserCreateModel, UserModel, UserLoginModel
from .service import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .utils import create_access_token, decode_token, verify_passwd
from fastapi.responses import JSONResponse
from datetime import timedelta

auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXP = 2

@auth_router.post('/signup', response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    
    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User already exists')
    
    new_user = await user_service.create_user(user_data, session)

    return new_user

@auth_router.post('/login')
async def login_users(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User not exists')
    
    pass_valid = verify_passwd(password, user.password)
    if not pass_valid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')
    
    access_token = create_access_token(
        user_data={
            'email': email,
            'user_id': str(user.id)
        }
    )

    refresh_token =  create_access_token(
        user_data={
            'email': email,
            'user_id': str(user.id)
        },
        refresh=True,
        expiry = timedelta(days=REFRESH_TOKEN_EXP)
    )
    
    return JSONResponse(
        content={
            "message": "Login success",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                'email': email,
                'user_id': str(user.id)
            }
        }
    )
