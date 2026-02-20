from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN = getenv("BOT_TOKEN")
    POSTGRES_DSN = getenv("POSTGRES_DSN", "sqlite://data/database.db")
