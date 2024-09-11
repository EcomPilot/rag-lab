from typing import List
from openai import OpenAI
from .base import EmbeddingBase

class OpenAIEmbedding(EmbeddingBase):
    def __init__(self, model_id: str = "text-embedding-ada-002", api_key: str = ""):
        self.model_id = model_id
        self.client = OpenAI(api_key=api_key)

    def embed_query(self, text: str) -> List[float]:
        response = self.client.Embedding.create(
            input=text,
            model=self.model_id
        )
        return response.data.embedding
