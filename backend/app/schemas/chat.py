from pydantic import BaseModel, Field
from typing import List, Literal, Optional


Role = Literal["system", "user", "assistant"]


class Message(BaseModel):
    role: Role
    content: str


class ChatRequest(BaseModel):
    messages: List[Message] = Field(default_factory=list)


class ChatResponse(BaseModel):
    reply: str