from pydantic import BaseModel, Field
from typing import List, Literal, Optional


Role = Literal["system", "user", "assistant", "tool-call", "tool-call-output"]


class Message(BaseModel):
    role: Role
    content: str


class ChatRequest(BaseModel):
    messages: List[Message] = Field(default_factory=list)


class ChatResponse(BaseModel):
    messages: List[Message] | None = None # full history