from passlib.context import CryptContext

passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_passwd_hash(password: str) -> str:
    return passwd_context.hash(password)


def verify_passwd(password: str, hashed_password: str) -> bool:
    return passwd_context.verify(password, hashed_password)
