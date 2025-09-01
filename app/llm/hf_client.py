import os
from typing import Dict, Any
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

class HFClient:
    def __init__(self, token: str | None = None):
        load_dotenv()
        self.token = token or os.getenv("HF_TOKEN")
        if not self.token:
            raise RuntimeError("HF_TOKEN is missing. Set it in your environment variables.")
        self.client = InferenceClient(token=self.token)
   
    def generate(self, model: str, prompt: str, params: Dict[str, Any],tools) :
        
        
        completion =self.client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3-0324",
            messages=[{"role": "user", "content": prompt}],
            tools=tools,
            tool_choice="auto",
        
            
        )
        if not completion.choices:
            raise RuntimeError("No completion returned from HF Inference API.")
        if len(completion.choices) > 1:
            print("Warning: Multiple completions returned, using the first one.")
        if completion.choices[0].message.tool_calls:
            print(f"Tool calls: {completion.choices[0].message.tool_calls}")
            return completion
        

        return completion