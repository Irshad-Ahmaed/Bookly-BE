from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .utils import decode_token
from src.db.redis import check_token_in_blocklist
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import UserService

user_service = UserService()

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request)-> HTTPAuthorizationCredentials | None:
        # Get the scheme, and credentials
        credentials = await super().__call__(request)

        token = credentials.credentials
        # Check if the token is valid one
        token_data = decode_token(token)

        if not self.valid_token(token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
                "error": 'Invalid or Expired Token',
                "resolution": "Please get new token"
            })

        # Check if token jti present in redis - If present means it's already revoked
        if await check_token_in_blocklist(token_data['jti']):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
                "error":'This Token is Invalid or Revoked',
                "resolution": "Please get new token"
            })
        
        # This method will override by child class
        self.verify_token_data(token_data)

        return token_data
    
    def valid_token(self, token: str)-> bool:
        token_data =  decode_token(token)

        return True if token_data is not None else False
    
    def verify_token_data(self, token_data):
        raise NotImplementedError("Please Override this method in child classes")
    
    
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Provide an Access Token')


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Provide a Refresh Token')
        


async def get_current_user(token_details: dict = Depends(AccessTokenBearer()), session: AsyncSession = Depends(get_session)):
    user_email = token_details['user']['email']

    user = await user_service.get_user_by_email(user_email, session)

    return user