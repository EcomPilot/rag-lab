from typing import List
from .base import EmbeddingBase
from openai import AzureOpenAI

class AzureOpenAIEmbedding(EmbeddingBase):
    def __init__(self, model_id: str = "'text-embedding-3-small", access_token: str = "", endpoint: str = "", api_version="2024-02-01"):
        self.model_id = model_id
        self.client = AzureOpenAI(
            api_key=access_token,  
            api_version=api_version,
            azure_endpoint = endpoint
            )

    def embed_query(self, text:str) -> List[float]:
        response = self.client.embeddings.create(
            input=text,
            model=self.model_id
        )
        return response.data[0].embedding