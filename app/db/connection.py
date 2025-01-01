from app.config.config import cfg
from contextlib import asynccontextmanager
import psycopg
from psycopg.rows import dict_row

@asynccontextmanager
async def get_db_connection():
    conn = await psycopg.AsyncConnection.connect(cfg.DATABASE_URL, autocommit=True, row_factory=dict_row)
    try:
        yield conn.cursor()
    finally:
        await conn.close()