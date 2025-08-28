# app/services/chat_service.py
from app.schemas.chat import ChatRequest, ChatResponse
from app.llm.hf_client import HFClient
from app.services.prompt import build_prompt
from app.services.tools import get_tools
from app.utils.yaml_loader import load_yaml

llm_client = HFClient()
llm_config = load_yaml("llm.yaml")

"""The chat service orchestrates user input, builds prompts with context and workflow instructions, calls the LLM w
ith proper configuration and tools, post-processes the response, and returns a structured reply to the API."""
async def process_chat(req: ChatRequest,categories:list[str]) -> ChatResponse:
    
    model = llm_config.get("llm").get("default_model")
    params = llm_config.get("llm").get("params", {})
    params = {
        "max_new_tokens": params.get("max_new_tokens", 512),
        "temperature": params.get("temperature", 0.7),
        "top_p": params.get("top_p", 0.9),
        "return_full_text": False,
    }
    
    
    prompt = build_prompt([m.dict() for m in req.messages],categories=categories)
    tools = get_tools(categories)
    
    text = llm_client.generate(model=model, prompt=prompt, params=params, tools=tools)
    if text.startswith(prompt):
        text = text[len(prompt):].lstrip()
    return ChatResponse(reply=text)
