from ...models.models import AIModel
from typing import Optional, Any
import json
import time
import os
import logging
from langchain_openai import ChatOpenAI
from langchain_ollama.chat_models import ChatOllama
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from ...outputdata.output_data import write_data_to_file
load_dotenv()

import logging
logger = logging.getLogger(__name__)

def get_chatprompt_templates(agents_prompt: str, input_keys: list[str]) -> ChatPromptTemplate:
    agents_prompt = agents_prompt.replace("{", "{{").replace("}", "}}")
    agents_prompt_template = SystemMessagePromptTemplate.from_template(agents_prompt)
    
    #combining all inputs into a single human message with named placeholders
    input_text = "\n".join([f"{key}: {{{key}}}" for key in input_keys])
    user_input_template = HumanMessagePromptTemplate.from_template(input_text)

    return ChatPromptTemplate.from_messages([
        agents_prompt_template,
        user_input_template
    ])

def get_llm_model(
        model_name: Any,
        output_pydantic_class
) -> ChatOllama | ChatOpenAI:
    
    if isinstance(model_name, dict):
        if AIModel.Ollama_DeepSeek_14b.value in model_name.model:
            return ChatOllama(model=AIModel.Ollama_DeepSeek_14b.value).with_structured_output(output_pydantic_class)
        elif AIModel.Ollama_Gemma_7b.value in model_name.model:
            return ChatOllama(model=AIModel.Ollama_Gemma_7b.value).with_structured_output(output_pydantic_class)
        else:
            #we could specify which model to use here always, for now if not deepseek then just use gpt4-o
            return ChatOpenAI(model_name=AIModel.GPT_4O.value).with_structured_output(output_pydantic_class)
        

    #if the model is not an instance of dict, then we can assume that it is a string and return just gpt40
    return ChatOpenAI(model_name=AIModel.GPT_4O.value).with_structured_output(output_pydantic_class)


def run_main_agent(
    output_pydantic_class,
    agents_name: str,
    agents_prompt: str,
    input_to_prompt: dict,
    model_name: Optional[str],
    ) -> Any:

    llm_model = get_llm_model(model_name, output_pydantic_class)

    logger.info(f"Running agent '{agents_name}' with model: {model_name}")
    
    chat_prompt = get_chatprompt_templates(agents_prompt, list(input_to_prompt.keys()))
  
    chain = chat_prompt | llm_model 

    MAX_TRIES = 1
    output = None
    start_time = time.time()
        
    while MAX_TRIES <= 5:
        try:
            logger.info(f"Attempt {MAX_TRIES} for agent '{agents_name}'")
           
            output = chain.invoke(input_to_prompt)
            
            logger.info(f"Agent '{agents_name}' succeeded on attempt {MAX_TRIES}")
            break
        except Exception as e:
            logger.error(f"Error in agent '{agents_name}' on attempt {MAX_TRIES}: {e}")
            
            #Appending error message to the prompt for the next try
            error_context = f"{agents_prompt}\n\n[ERROR MESSAGE FOR AGENT CONTEXT]: {str(e)}"
            chat_prompt = get_chatprompt_templates(error_context, list(input_to_prompt.keys()))
            chain = chat_prompt | llm_model 

            MAX_TRIES += 1

    end_time = time.time()
    time_taken = end_time - start_time
    logger.info(f"Agent '{agents_name}' finished execution in {time_taken:.2f} seconds with {MAX_TRIES} tries.")
    
    # print("\n\n\n\n OUTPUT: ", output, "\n\n\n\n")
    
    #lets dump the data into json
    write_data_to_file(
        agents_name=agents_name,
        number_of_tries=MAX_TRIES,
        time_taken=time_taken,
        user_input=input_to_prompt,
        output=output
    )
    
    # print("\n\n\n\n OUTPOUT: ", output , "\n\n\n\n")
    logger.info(f"Agent '{agents_name}' execution data written to agent_execution.json")
    return output