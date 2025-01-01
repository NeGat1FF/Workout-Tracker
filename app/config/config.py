from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str


    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

cfg = Settings()

