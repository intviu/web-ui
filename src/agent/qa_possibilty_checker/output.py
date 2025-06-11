from pydantic import BaseModel

class QAPossibiltyChecker(BaseModel):
    agent_msg: str
    qa_possibilty: bool