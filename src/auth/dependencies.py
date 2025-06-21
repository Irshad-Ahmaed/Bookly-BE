from fastapi import Request, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .utils import decode_token

class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request)-> HTTPAuthorizationCredentials | None:
        credentials = await super().__call__(request)

        token = credentials.credentials
        
        token_data = decode_token(token)

        if not self.valid_token:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid or Expired Token')
        
        if token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Provide an Access Token')
        
        return token_data
    
    def valid_token(self, token: str)-> bool:
        token_data =  decode_token(token)

        return True if token_data is not None else False