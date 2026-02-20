from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN = getenv("BOT_TOKEN")
    POSTGRES_USER = getenv("POSTGRES_USER", "user")
    POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_HOST = getenv("POSTGRES_HOST", "localhost")
    POSTGRES_DB = getenv("POSTGRES_DSN", "test_db")

    POSTGRES_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"
