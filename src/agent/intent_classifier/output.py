from pydantic import BaseModel

class IntentClassifierOutput(BaseModel):
    agent_msg: str
    intent: bool