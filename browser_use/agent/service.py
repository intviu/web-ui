"""
Base implementation of the agent service.
"""
from typing import Optional, List, Dict, Any, Type, Callable
from .views import AgentHistoryList, AgentOutput

class Agent:
    """Base agent implementation for browser automation"""
    
    def __init__(
        self,
        task: str,
        llm: Any,
        browser=None,
        browser_context=None,
        controller=None,
        use_vision: bool = True,
        use_vision_for_planner: bool = False,
        save_conversation_path: Optional[str] = None,
        save_conversation_path_encoding: Optional[str] = 'utf-8',
        max_failures: int = 3,
        retry_delay: int = 10,
        system_prompt_class: Any = None,
        max_input_tokens: int = 128000,
        validate_output: bool = False,
        message_context: Optional[str] = None,
        generate_gif: bool = True,
        sensitive_data: Optional[Dict[str, str]] = None,
        available_file_paths: Optional[List[str]] = None,
        include_attributes: List[str] = None,
        max_error_length: int = 400,
        max_actions_per_step: int = 10,
        tool_call_in_content: bool = True,
        initial_actions: Optional[List[Dict[str, Dict[str, Any]]]] = None,
        register_new_step_callback: Optional[Callable] = None,
        register_done_callback: Optional[Callable] = None,
        tool_calling_method: Optional[str] = 'auto',
        planner_llm: Optional[Any] = None,
        planner_interval: int = 1
    ):
        """Initialize the agent"""
        self.task = task
        self.llm = llm
        self.browser = browser
        self.browser_context = browser_context
        self.controller = controller
        self.use_vision = use_vision
        self.use_vision_for_planner = use_vision_for_planner
        self.save_conversation_path = save_conversation_path
        self.save_conversation_path_encoding = save_conversation_path_encoding
        self.max_failures = max_failures
        self.retry_delay = retry_delay
        self.system_prompt_class = system_prompt_class
        self.max_input_tokens = max_input_tokens
        self.validate_output = validate_output
        self.message_context = message_context
        self.generate_gif = generate_gif
        self.sensitive_data = sensitive_data
        self.available_file_paths = available_file_paths
        self.include_attributes = include_attributes if include_attributes else []
        self.max_error_length = max_error_length
        self.max_actions_per_step = max_actions_per_step
        self.tool_call_in_content = tool_call_in_content
        self.initial_actions = initial_actions
        self.register_new_step_callback = register_new_step_callback
        self.register_done_callback = register_done_callback
        self.tool_calling_method = tool_calling_method
        self.planner_llm = planner_llm
        self.planner_interval = planner_interval
        
        # Get model name from LLM when available
        self.model_name = getattr(self.llm, "model_name", "unknown")
        
    async def run(self, max_steps: int = 10) -> AgentHistoryList:
        """Run the agent with the given task"""
        # For stub implementation, just return a success history
        history = AgentHistoryList()
        history.add_step(
            thought="Starting task execution",
            action="initialize",
            result="Agent initialized successfully"
        )
        return history 