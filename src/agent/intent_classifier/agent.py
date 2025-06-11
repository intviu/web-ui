import logging
from .output import IntentClassifierOutput
from .prompt import agents_prompt
from ..main_agent.agent import run_main_agent
import logging
from typing import Any

logger = logging.getLogger(__name__)

class IntentClassifierAgent:
    def __init__(self, llm: Any, user_prompt: str) -> None:
        logger.info("Initializing IntentClassifierAgent")
        self.output_pydantic_class = IntentClassifierOutput
        self.llm = llm
        self.agent_prompt = agents_prompt
        self.user_prompt = user_prompt

    def run_agent(self) -> IntentClassifierOutput:
        logger.info(f"Running Intent Classifier Agent....")
        
        output = run_main_agent(
            output_pydantic_class=self.output_pydantic_class,
            agents_name="Intent Classifier Agent",
            agents_prompt=self.agent_prompt,
            input_to_prompt={
                "input": self.user_prompt
            }
        )
        
        logger.info(f"Intent Classifier Agent finished. Output: {output}")
        return output
