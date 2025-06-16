import logging
from .output import PromptEnhancerOutput
from .prompt import agents_prompt
from ..main_agent.agent import run_main_agent
import logging
logger = logging.getLogger(__name__)

class PromptEnhancerAgent:
    def __init__(self,llm: str, user_prompt: str, extracted_snippet: str) -> None:
        logger.info("Initializing PromptEnhancerAgent...")
        self.output_pydantic_class = PromptEnhancerOutput
        self.user_prompt = user_prompt
        self.agent_prompt = agents_prompt
        self.extracted_snippet = extracted_snippet
        self.llm = llm

    def run_agent(self) -> PromptEnhancerOutput:        
        output = run_main_agent(
            output_pydantic_class=self.output_pydantic_class,
            agents_name="Prompt Enhancer Agent",
            agents_prompt=self.agent_prompt,
            input_to_prompt={
                "input": self.user_prompt,
                "extracted_snippet": self.extracted_snippet
            },
             model_name=self.llm
        )
        
        logger.info(f"Prompt Enhancers Agent finished...")
        return output