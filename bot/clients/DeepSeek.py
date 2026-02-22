import json

import httpx
from typing import AsyncGenerator

from config import Config


class AIAgent:
    """
    Асинхронный клиент для DeepSeek API.
    Использует стандартный OpenAI‑совместимый интерфейс:
    POST /v1/chat/completions
    """

    def __init__(self):
        self.api_key = Config.LLM_API_KEY
        self.base_url = Config.LLM_BASE_URL
        self.model = Config.LLM_MODEL
        self.max_tokens = Config.LLM_MAX_TOKENS
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def chat(
        self,
        messages: list[dict],
        temperature: float = 0.7
    ) -> str:
        """
        Нормальный запрос (полный ответ после генерации).
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": temperature,
            "stream": False
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=60.0
            )
            response.raise_for_status()
            data = response.json()

        # Стандартный OpenAI‑формат ответа
        return data["choices"][0]["message"]["content"]

    async def stream_chat(
        self,
        messages: list[dict],
        temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        """
        Асинхронный стриминг токенов.
        Сервер будет возвращать частичный поток ответов.
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": temperature,
            "stream": True
        }

        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload
            ) as resp:
                resp.raise_for_status()

                async for line in resp.aiter_lines():
                    # Формат SSE: строки вида `data: {...}`
                    if not line or not line.startswith("data:"):
                        continue
                    payload = line.removeprefix("data:").strip()
                    if payload == "[DONE]":
                        break

                    # Переводим JSON события
                    try:
                        event = json.loads(payload)
                        # OpenAI‑совм класс токенов
                        delta = event["choices"][0]["delta"].get("content")
                        if delta:
                            yield delta
                    except ValueError:
                        # Игнорируем неподходящие строки
                        continue