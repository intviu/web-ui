from pydantic import BaseModel

class PromptEnhancerOutput(BaseModel):
    agent_msg: str
    enhanced_prompt: str
