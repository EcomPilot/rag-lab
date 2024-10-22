from .base import LLMBase
from openai import AzureOpenAI

class AzureOpenAILLM(LLMBase):
    def __init__(self, model_id: str = "gpt-35-turbo", access_token: str = "", endpoint: str = "", api_version="2024-02-01", max_tokens=2000, temperature=0.1, top_p=0.8):
        self.model_id = model_id
        self.client = AzureOpenAI(
            api_key=access_token,  
            api_version=api_version,
            azure_endpoint = endpoint
            )
        
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p

    def invoke(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=self.top_p
        )
        return response.choices[0].message.content