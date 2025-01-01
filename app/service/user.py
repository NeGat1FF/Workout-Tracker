from app.db.connection import get_db_connection
from app.utils.password import hash_password, verify_password
from app.utils.JWT import *
from app.schema.user import UserCreate, User
from pydantic import EmailStr
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def create_user(user: UserCreate) -> UUID:
    pass_hash = hash_password(user.password)

    async with get_db_connection() as cur:
        await cur.execute('INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s) RETURNING user_id', (user.username, user.email, pass_hash))
        res = await cur.fetchone()
        return res['user_id']
    
async def get_user_by_email(email: EmailStr) -> User:
    async with get_db_connection() as cur:
        await cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        return User.model_validate(await cur.fetchone())
    
async def get_user_by_id(user_id: UUID) -> User:
    async with get_db_connection() as cur:
        await cur.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
        return User.model_validate(await cur.fetchone())
    
def authenticate_user(jwt: str = Depends(oauth2_scheme)) -> dict:
    claims = verify_jwt_token(jwt, 'access')
    return claims
