from pydantic import BaseModel, Field, field_validator
from typing import List
import re

class SendMessageRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=4096,
        description="The message to send to BotFather"
    )

    @field_validator('message')
    @classmethod
    def validate_message(cls, v: str) -> str:
        # Remove any potential command injection
        v = re.sub(r'[^\w\s\-/]', '', v)
        if not v.strip():
            raise ValueError("Message cannot be empty or contain only special characters")
        return v.strip()

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "/newbot"
            }
        }
    }

class SendMessageResponse(BaseModel):
    messages: List[str] = Field(
        ...,
        description="List of replies received from BotFather"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "messages": [
                    "Please choose a name for your bot.",
                    "Please choose a username for your bot.",
                    "Great! Your bot has been created."
                ]
            }
        }
    }

class ErrorResponse(BaseModel):
    error: str = Field(
        ...,
        description="Error message describing what went wrong"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "error": "Rate limit exceeded. Maximum 10 requests per 60 seconds."
            }
        }
    } 