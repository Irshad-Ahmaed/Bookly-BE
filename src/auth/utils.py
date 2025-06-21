from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from src.config import config
import uuid
import logging

passwd_context = CryptContext(
    schemes=['bcrypt']
)

ACCESS_TOKEN_EXPIRY = 3600

def generate_passwd_hash(password:str)-> str:
    hash_pass = passwd_context.hash(password)

    return hash_pass

def verify_passwd(password: str, hash: str)-> bool:
    return passwd_context.verify(password, hash)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    payload = {}

    payload['user'] = user_data
    payload['exp'] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['jti'] = str(uuid.uuid4())

    payload['refresh'] = refresh

    token = jwt.encode(
        payload=payload,
        key=config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGO
    )

    return token

def decode_token(token: str)-> dict:
    try:
        token_data = jwt.decode(
            token=token,
            key=config.JWT_SECRET_KEY,
            algorithms=[config.JWT_ALGO]
        )

        return token_data
    except jwt.PyJWTError as err:
        logging.exception(err)
        return None