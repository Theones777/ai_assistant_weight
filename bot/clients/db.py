from alembic import command
from alembic.config import Config as AlembicConfig
from sqlalchemy.ext.asyncio import create_async_engine

from bot.log import logger
from config import Config


class DBClient:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.engine = None
    
    def create_engine(self):
        return create_async_engine(self.db_url, future=True)
    
    @staticmethod
    def create_db_scheme():
        """Upgrade db"""
        try:
            alembic_config = AlembicConfig("alembic.ini")
            alembic_config.set_main_option("sqlalchemy.url", Config.POSTGRES_DSN)
            command.upgrade(alembic_config, "head")
            logger.info('apply "alembic upgrade head"')
        
        except Exception as exc:
            logger.error(f'Error apply "alembic upgrade head"\nError: {exc}')


    async def open(self):
        """
        Start DB client
        """
        self.create_db_scheme()

        try:
            self.engine = self.create_engine()
            connection = await self.engine.connect()
            await connection.close()
            await self.engine.dispose()
            logger.info("Establishment connect to db.")
        
        except Exception as exc:
            logger.error(f"Error connection to db. Error:{exc}")
