from pydantic import BaseModel

class SnippetExtractorOutput(BaseModel):
    agent_msg: str
    extracted_snippet: str
    snippet_check: bool