from langchain_openai import ChatOpenAI
from support_copilot.infrastructure.config.settings import settings


class OpenAILLMProvider:
    def __init__(self) -> None:
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=0,
        )

    def answer(self, prompt: str) -> str:
        return self.llm.invoke(prompt).content
