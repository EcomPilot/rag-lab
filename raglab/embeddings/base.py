from abc import ABCMeta, abstractmethod
from typing import Any, List

class EmbeddingBase(metaclass=ABCMeta):
    @abstractmethod
    def embed_query(self, text:str, **kwargs: Any) -> List[float]:
      pass