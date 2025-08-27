from pydantic import BaseModel, Field
from typing import List, Literal, Optional


Role = Literal["system", "user", "assistant"]


class Message(BaseModel):
    role: Role
    content: str


class ChatRequest(BaseModel):
    messages: List[Message] = Field(default_factory=list)
    model: Optional[str] = None
    max_new_tokens: int = 256
    temperature: float = 0.7
    top_p: float = 0.95


class ChatResponse(BaseModel):
    reply: str