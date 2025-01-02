from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

FAKE_USERS_DB = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("secret"),
    }
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user = FAKE_USERS_DB.get(username)
    if user and verify_password(password, user["hashed_password"]):
        return user
    return None