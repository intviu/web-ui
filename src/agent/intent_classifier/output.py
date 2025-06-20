from typing import Optional
from pydantic import BaseModel

class IntentClassifierOutput(BaseModel):
    agent_msg: str
    intent: bool
    modified_prompt: Optional[str] = ""