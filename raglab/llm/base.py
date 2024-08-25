from abc import ABCMeta, abstractmethod
from typing import Any, Dict, List, Optional

class LLMBase(metaclass=ABCMeta):
    @abstractmethod
    def invoke(self, prompt: str, **kwargs: Any) -> str:
      pass