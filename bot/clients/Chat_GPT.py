from openai import OpenAI

from config import Config


class AIAgent:
    def __init__(self):
        self.client = OpenAI(api_key=Config.LLM_API_KEY)

    async def make_request(self, user_request: str):
        # resp = await self.client.chat.completions.create(
        #     model="gpt-4",
        #     messages=[
        #         {"role": "system", "content": "You are a helpful assistant."},
        #         {"role": "user", "content": user_request}
        #     ]
        # )
        # print(resp.choices[0].message.content)
        return "Ответ ИИ"
