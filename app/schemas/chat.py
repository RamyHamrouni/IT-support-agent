from pydantic import BaseModel, Field
from typing import List, Literal, Optional

Role = Literal["user", "system", "assistant", "tool-call", "tool-call-output"]

class Message(BaseModel):
    role: Role
    content: str

class ChatRequest(BaseModel):
    user_id: str
    messages: List[Message] = Field(default_factory=list)

class ChatResponse(BaseModel):
    user_id: str 
    messages: Optional[List[Message]] = None 
