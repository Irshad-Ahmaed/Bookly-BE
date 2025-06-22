import redis.asyncio as aioredis
from src.config import config

JTI_EXPIRY = 3600

token_blocklist = aioredis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=0,
    decode_responses=True
)

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(
        name=jti,
        value='',
        ex=JTI_EXPIRY
    )

async def check_token_in_blocklist(jti: str)-> bool:
    jti = await token_blocklist.get(jti)

    return jti is not None 