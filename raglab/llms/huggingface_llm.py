from .base import LLMBase
import transformers
import torch
import gc

class HuggingFaceLLM(LLMBase):
    def __init__(self, model_id: str = "microsoft/Phi-3-small-128k-instruct", huggingface_access_token: str = "", max_tokens=256, temperature=0.3, top_p=0.9):
        self.model_id = model_id
        self.pipeline = transformers.pipeline(
            "text-generation",
            model=model_id,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device_map="auto",
            token=huggingface_access_token
        )
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p

    def invoke(self, prompt: str) -> str:
        with torch.no_grad():
            messages = [
                {"role": "user", "content": prompt},
            ]

            template_prompt = self.pipeline.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )

            terminators = [
                self.pipeline.tokenizer.eos_token_id,
                self.pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
            ]

            outputs = self.pipeline(
                template_prompt,
                max_new_tokens=self.max_tokens,
                eos_token_id=terminators,
                do_sample=True,
                temperature=self.temperature,
                top_p=self.top_p,
            )
            gc.collect()
            torch.cuda.empty_cache()
            return outputs[0]["generated_text"][len(template_prompt):]