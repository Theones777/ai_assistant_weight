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
    POSTGRES_POOL_SIZE = getenv("POSTGRES_POOL_SIZE", 10)
    POSTGRES_MAX_OVERFLOW = getenv("POSTGRES_MAX_OVERFLOW", 20)

    LLM_API_KEY = getenv("LLM_API_KEY")
    LLM_MAX_TOKENS = getenv("LLM_MAX_TOKENS", 2000)
    LLM_BASE_URL = getenv("LLN_BASE_URL", "https://api.deepseek.com/v1")
    LLM_MODEL = getenv("LLM_MODEL", "deepseek-chat")
