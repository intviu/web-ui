from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from pydantic import BaseModel

@dataclass
class AgentStep:
    """Agent step class that tracks a single step in the agent's execution"""
    thought: str
    action: str
    result: str
    error: Optional[str] = None

class AgentHistoryList:
    """Class to track agent execution history"""
    
    def __init__(self):
        self.steps: List[AgentStep] = []
        self.errors: List[str] = []
        
    def add_step(self, thought: str, action: str, result: str) -> None:
        """Add a step to the history"""
        self.steps.append(AgentStep(thought=thought, action=action, result=result))
        
    def add_error(self, error: str) -> None:
        """Add an error to the history"""
        self.errors.append(error)
        
    def final_result(self) -> Dict[str, Any]:
        """Get the final result"""
        if not self.steps:
            return {"status": "error", "message": "No steps executed"}
        return {
            "status": "success",
            "last_step": self.steps[-1].result
        }
        
    @property
    def error_list(self) -> List[str]:
        """Get all errors"""
        return self.errors
        
    def model_actions(self) -> List[str]:
        """Get all actions taken"""
        return [step.action for step in self.steps]
        
    def model_thoughts(self) -> List[str]:
        """Get all thoughts"""
        return [step.thought for step in self.steps]

class ActionResult(BaseModel):
    """Result of an action"""
    success: bool = True
    error: Optional[str] = None
    extracted_content: Optional[str] = None
    title: Optional[str] = None
    
class ActionModel(BaseModel):
    """Base model for actions"""
    action: str
    parameters: Dict[str, Any] = {}
    
class AgentOutput(BaseModel):
    """Output from the agent"""
    action: List[ActionModel]
    
class AgentHistory(BaseModel):
    """History of agent execution"""
    steps: List[Dict[str, Any]] = [] 