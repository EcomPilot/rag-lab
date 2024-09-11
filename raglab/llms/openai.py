from openai import OpenAI
from .base import LLMBase

class OpenAILLM(LLMBase):
    def __init__(self, model_id: str = "gpt-3.5-turbo", api_key: str = "", max_tokens: int = 2000, temperature: float = 0.1, top_p: float = 0.8):
        self.model_id = model_id
        self.client = OpenAI(api_key=api_key)
        
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p

    def invoke(self, prompt: str) -> str:
        response = self.client.Completion.create(
            model=self.model_id,
            prompt=prompt,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=self.top_p
        )
        return response.choices.text
