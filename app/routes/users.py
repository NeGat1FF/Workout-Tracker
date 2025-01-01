from app.service.user import *
from app.utils.JWT import *
from app.utils.password import *
from app.schema.user import *
from fastapi import APIRouter

user_router = APIRouter(tags=["user"], prefix="/api/v1")

@user_router.post("/register", status_code=201, summary="Register a new user")
async def register(user: UserCreate):
    user_id = await create_user(user)
    return generate_tokens(user_id, 'user', datetime.datetime.now() + datetime.timedelta(hours=1), datetime.datetime.now() + datetime.timedelta(days=7))

@user_router.post("/login", status_code=200, summary="Login a user")
async def login(user: UserLogin) -> dict:
    db_user = await get_user_by_email(user.email)
    if not user or not verify_password(db_user.password_hash, user.password):
        return {"error": "Invalid credentials"}
    
    return generate_tokens(db_user.user_id, db_user.role, datetime.datetime.now() + datetime.timedelta(hours=1), datetime.datetime.now() + datetime.timedelta(days=7))

@user_router.post("/refresh", status_code=200, summary="Refresh a user's tokens")
async def refresh(refresh_token: RefreshToken):
    claims = verify_jwt_token(refresh_token.refresh_token, 'refresh')
    
    return generate_tokens(claims['uid'], claims['role'], datetime.datetime.now() + datetime.timedelta(hours=1), datetime.datetime.now() + datetime.timedelta(days=7))

@user_router.get("/me", status_code=200, summary="Get a user's information")
async def me(token: str):
    token = verify_jwt_token(token, 'access')
    user = await get_user_by_id(token['user_id'])
    return user
