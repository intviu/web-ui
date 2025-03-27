"""
Action registry for browser automation.
"""
from typing import Dict, Any, Callable, List, Optional, Type
import inspect
from pydantic import BaseModel, create_model

class ActionRegistry:
    """Registry for browser actions"""
    
    def __init__(self):
        """Initialize the registry"""
        self.actions: Dict[str, Callable] = {}
        self.descriptions: Dict[str, str] = {}
        
    def action(self, name: str, description: str = ""):
        """Decorator to register an action"""
        def decorator(fn):
            self.actions[name] = fn
            self.descriptions[name] = description or fn.__doc__ or ""
            return fn
        return decorator
        
    def get_action(self, name: str) -> Optional[Callable]:
        """Get an action by name"""
        return self.actions.get(name)
        
    def get_actions(self) -> Dict[str, Callable]:
        """Get all registered actions"""
        return self.actions
        
    def get_action_names(self) -> List[str]:
        """Get all registered action names"""
        return list(self.actions.keys())
        
    def get_prompt_description(self) -> str:
        """Get a description of all actions for the prompt"""
        result = ""
        for name, description in self.descriptions.items():
            params = inspect.signature(self.actions[name]).parameters
            param_desc = ", ".join([f"{p}: {type(v.default).__name__}" for p, v in params.items() if p != "self"])
            result += f"{name}({param_desc}): {description}\n"
        return result
        
    def create_action_model(self) -> Type[BaseModel]:
        """Create a dynamic action model"""
        return create_model("ActionModel", action=(str, ...), parameters=(Dict[str, Any], {})) 