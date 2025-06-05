from pydantic import BaseModel
from typing import List

class SendMessageRequest(BaseModel):
    message: str

class SendMessageResponse(BaseModel):
    messages: List[str]

class ErrorResponse(BaseModel):
    error: str 