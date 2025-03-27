"""
Controller service for browser automation.
"""
from typing import List, Dict, Any, Optional, Type
from pydantic import BaseModel
from .registry import ActionRegistry
from .views import DoneAction

class Controller:
    """Controller class for browser automation"""
    
    def __init__(
        self, 
        exclude_actions: List[str] = [],
        output_model: Optional[Type[BaseModel]] = None
    ):
        """Initialize the controller"""
        self.registry = ActionRegistry()
        self.exclude_actions = exclude_actions
        self.output_model = output_model
        self._register_default_actions()
        
    def _register_default_actions(self):
        """Register default browser actions"""
        
        @self.registry.action("Done")
        def done(message: str = "Task completed successfully"):
            return DoneAction(message=message)
    
    async def execute_action(self, action_name: str, **kwargs) -> Any:
        """Execute an action with the given name and parameters"""
        action_fn = self.registry.get_action(action_name)
        if action_fn:
            return await action_fn(**kwargs)
        raise ValueError(f"Unknown action: {action_name}") 