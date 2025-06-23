from pydantic import BaseModel

class QAPossibilityCheckerOutput(BaseModel):
    agent_msg: str
    qa_possibility: bool