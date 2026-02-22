from alembic import command
from alembic.config import Config as AlembicConfig
from tiktoken import encoding_for_model

from bot.log import logger
from bot.models.db import User, UserRequest
from config import Config
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from sqlalchemy import select
from typing import Optional


class DBClient:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.engine = create_async_engine(
            self.db_url,
            echo=False,
            future=True,
            pool_size=Config.POSTGRES_POOL_SIZE,
            max_overflow=Config.POSTGRES_MAX_OVERFLOW,
            pool_pre_ping=True
        )
        self.session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession
        )
        self.create_db_scheme()

    def create_db_scheme(self):
        """Apply migrations"""
        try:
            alembic_config = AlembicConfig("alembic.ini")
            alembic_config.set_main_option("sqlalchemy.url", self.db_url)
            command.upgrade(alembic_config, "head")
            logger.info('apply "alembic upgrade head"')

        except Exception as exc:
            logger.error(f"Alembic error: {exc}")

    async def create_user(
        self,
        id: int,
        name: str,
        gender: str,
        age: int,
        height: int,
        weight: int
    ) -> User:
        async with self.session_factory() as session:
            async with session.begin():
                user = User(
                    id=id,
                    name=name,
                    gender=gender,
                    age=age,
                    height=height,
                    weight=weight
                )
                session.add(user)
            return user

    async def get_user(self, user_id: int) -> Optional[User]:
        async with self.session_factory() as session:
            result = await session.execute(
                select(User).where(User.id == user_id)
            )
            return result.scalar_one_or_none()

    async def create_user_request(
        self,
        user_id: int,
        request_text: str,
        response_text: str
    ) -> UserRequest:
        async with self.session_factory() as session:
            async with session.begin():
                req = UserRequest(
                    user_id=user_id,
                    request_text=request_text,
                    response_text=response_text
                )
                session.add(req)
            return req

    async def get_dialog_history_for_llm(
            self,
            user_id: int,
    ) -> list[dict]:
        """
        Возвращает историю диалога для LLM в формате [{"role": "user/assistant", "content": "..."}]
        Ограничивает суммарное количество токенов.
        """
        # Подсчёт токенов
        enc = encoding_for_model(Config.LLM_MODEL)

        async with self.session_factory() as session:
            result = await session.execute(
                select(UserRequest)
                .where(UserRequest.user_id == user_id)
                .order_by(UserRequest.timestamp.desc())
            )
            requests = result.scalars().all()

        history = []
        token_count = 0

        # идём с конца (новые сообщения первыми)
        for req in requests:
            messages = [
                {"role": "user", "content": req.request_text},
                {"role": "assistant", "content": req.response_text},
            ]
            for msg in reversed(messages):  # добавляем в обратном порядке
                msg_tokens = len(enc.encode(msg["content"]))
                if token_count + msg_tokens > Config.LLM_MAX_TOKENS:
                    break
                history.append(msg)
                token_count += msg_tokens

            if token_count >= Config.LLM_MAX_TOKENS:
                break

        # вернуть в хронологическом порядке
        return list(reversed(history))
