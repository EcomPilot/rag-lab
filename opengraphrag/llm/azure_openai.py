from opengraphrag.llm.base import LLMBase
from openai import AzureOpenAI

class AzureOpenAILLM(LLMBase):
    def __init__(self, model_id: str = "gpt-35-turbo", access_token: str = "", endpoint: str = "", api_version="2024-02-01"):
        self.model_id = model_id
        self.client = AzureOpenAI(
            api_key=access_token,  
            api_version=api_version,
            azure_endpoint = endpoint
            )

    def invoke(self, prompt: str, max_tokens=1024, temperature=0.3, top_p=0.9) -> str:
        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p
        )
        return response.choices[0].message.content