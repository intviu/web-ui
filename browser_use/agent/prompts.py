"""
Prompt templates for the agent.
"""
from typing import Optional, List, Dict, Any

class SystemPrompt:
    """System prompt for the agent"""
    
    def get_prompt(self) -> str:
        """Get the system prompt"""
        return """
You are an autonomous browsing agent that can help users with web-based tasks.
Your goal is to complete the user's request by interacting with a web browser.
You can perform actions like navigating to websites, clicking elements, typing text, and more.
Always think step by step about what you need to do to complete the task.
"""

class AgentMessagePrompt:
    """Message prompt for the agent"""
    
    def get_prompt(
        self, 
        task: str, 
        previous_actions: Optional[List[Dict[str, Any]]] = None, 
        observation: Optional[str] = None,
        memory: Optional[Dict[str, Any]] = None
    ) -> str:
        """Get the agent message prompt"""
        prompt = f"Task: {task}\n\n"
        
        if previous_actions:
            prompt += "Previous actions:\n"
            for i, action in enumerate(previous_actions):
                prompt += f"{i+1}. {action.get('action', 'Unknown')} - {action.get('result', 'No result')}\n"
            prompt += "\n"
            
        if observation:
            prompt += f"Observation: {observation}\n\n"
            
        prompt += "What's your next step to complete this task?"
        return prompt 

class PlannerPrompt:
    """Prompt for the planner"""
    
    def get_prompt(
        self,
        task: str,
        current_state: Optional[Dict[str, Any]] = None,
        steps_so_far: Optional[List[Dict[str, Any]]] = None,
        observation: Optional[str] = None
    ) -> str:
        """Get the planner prompt"""
        prompt = f"Task: {task}\n\n"
        
        if steps_so_far:
            prompt += "Steps taken so far:\n"
            for i, step in enumerate(steps_so_far):
                prompt += f"{i+1}. {step.get('action', 'Unknown')}\n"
            prompt += "\n"
            
        if current_state:
            prompt += "Current state:\n"
            for key, value in current_state.items():
                prompt += f"- {key}: {value}\n"
            prompt += "\n"
            
        if observation:
            prompt += f"Observation: {observation}\n\n"
            
        prompt += "Please create a plan to complete this task. What are the next steps?"
        return prompt 