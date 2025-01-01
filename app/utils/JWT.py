# from app.config.config import cfg
import jwt
import datetime
import uuid
from fastapi import HTTPException

class Config:
    JWT_SECRET = 'myjwtsecret'

cfg = Config()

def create_jwt_token(payload: dict) -> str:
    return jwt.encode(payload, cfg.JWT_SECRET, algorithm='HS256')

def verify_jwt_token(token: str, type: str) -> dict:
    try:
        claims = jwt.decode(token, cfg.JWT_SECRET, algorithms=['HS256'], verify=True)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if claims['type'] != type:
        raise HTTPException(status_code=401, detail="Invalid token type")
    
    return claims

def generate_tokens(user_id: uuid.UUID, user_role: str, access_exp_date: datetime, refresh_exp_date: datetime) -> dict:
    access_token = create_jwt_token({"uid": str(user_id), 'type': 'access', 'role': user_role, 'exp': access_exp_date})
    refresh_token = create_jwt_token({"uid": str(user_id), 'type': 'refresh', 'role': user_role, 'exp': refresh_exp_date})

    return {"access_token": access_token, "refresh_token": refresh_token}