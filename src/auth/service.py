import uuid
from fastapi import HTTPException
from src.db.models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from .schemas import UserCreateModel
from .utils import generate_passwd_hash

class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)

        user = await session.exec(statement)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user.first()
    
    async def user_exists(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        return True if user is not None else False
    
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        new_user = User(
            **user_data_dict
        )

        new_user.password = generate_passwd_hash(user_data_dict['password'])
        new_user.role = "user"

        session.add(new_user)
        await session.commit()

        return new_user


    async def verify_user_id(self, userID: uuid.UUID, user_detail_from_token: dict,  session: AsyncSession):
        token_userID = user_detail_from_token['user']['user_id']
        if not token_userID == str(userID):
            return False
        
        return True
        
            