from passlib.context import CryptContext

passwd_context = CryptContext(
    schemes=['bcrypt']
)

def generate_passwd_hash(password:str)-> str:
    hash_pass = passwd_context.hash(password)

    return hash_pass

def verify_passwd(password: str, hash: str)-> bool:
    return passwd_context.verify(password, hash)