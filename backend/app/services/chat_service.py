from app.schemas.chat import ChatRequest, ChatResponse
from app.llm.hf_client import HFClient
from app.services.prompt import build_prompt
from app.services.tools import get_tools
from app.services.tool_dispatcher import handle_tool_call
from app.utils.yaml_loader import load_yaml

llm_client = HFClient()
llm_config = load_yaml("llm.yaml")
model = llm_config.get("llm").get("default_model")
params = llm_config.get("llm").get("params", {})
params = {
    "max_new_tokens": params.get("max_new_tokens", 512),
    "temperature": params.get("temperature", 0.7),
    "top_p": params.get("top_p", 0.9),
    "return_full_text": False,
}

async def process_chat(req: ChatRequest, categories: list[str], attempts: int = 0) -> ChatResponse:
    """
    Orchestrates the chat flow: builds prompt, calls LLM, dispatches tool calls,
    and returns a structured ChatResponse.
    """
    prompt = build_prompt([m.dict() for m in req.messages], categories=categories)
    tools = get_tools(categories)

    completion = llm_client.generate(model=model, prompt=prompt, params=params, tools=tools)
    message = completion.choices[0].message

    if message.tool_calls:
        return await handle_tool_call(req, categories, message.tool_calls, attempts)

    return ChatResponse(reply=message.content)
