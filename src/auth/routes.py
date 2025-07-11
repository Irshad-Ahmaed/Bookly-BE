from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import UserCreateModel, UserModel, UserLoginModel, UserBooksModel
from .service import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .utils import create_access_token, verify_passwd
from fastapi.responses import JSONResponse
from datetime import timedelta, datetime
from .dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from src.db.redis import add_jti_to_blocklist

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin", "user"])


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
            'user_id': str(user.id),
            'role': user.role
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

@auth_router.get('/refresh_token')
async def access_token_with_refresh(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']
    
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            user_data=token_details['user']
        )

        return JSONResponse(
            content={
                'message': 'Successfully created access token',
                "access_token": new_access_token
            }
        )

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or Expired token")


@auth_router.get('/me', response_model=UserBooksModel)
async def current_user(user: dict = Depends(get_current_user), _: bool = Depends(role_checker)) -> dict:

    return user

@auth_router.get('/logout')
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details['jti']
    
    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={
            "message": "Logout Successfully"
        },
        status_code=status.HTTP_200_OK
    )