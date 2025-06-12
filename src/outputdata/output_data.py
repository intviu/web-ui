import json
import os
import logging
from pathlib import Path
import time

logger = logging.getLogger(__name__)

def write_data_to_file(
    agents_name: str,
    number_of_tries: str,
    time_taken: int,
    user_input: float,
    output: str
    ) -> None:
    try:
        script_dir = Path(__file__).parent
        output_file = script_dir / 'agent_execution.json'
        
        # initial_agents = [
        #     "Intent Classifier Agent",
        #     "Webpage Checker",
        #     "Prompt Enhancer Agent",
        #     "Snippet Extractor Agent",
        #     "QA POSSIBILTY CHECKER",
        # ]

        # Create new data entry           
        if agents_name == "Browser Use Agent":
            new_data = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "evaluation": user_input,
                "memory": output,
                "next_goal": agents_name,
                "actions": json.loads(number_of_tries) if isinstance(number_of_tries, str) else number_of_tries
            }
        else:
             new_data = {
                "agents_name": agents_name,
                "number_of_tries": number_of_tries,
                "time_taken": time_taken,
                "user_input": user_input,
                "output": output
            }

        # Read existing data if file exists
        # existing_data = []
        # if output_file.exists():
        #     try:
        #         with open(output_file, 'r') as f:
        #             content = f.read()
        #             if content.strip():  # Check if file is not empty
        #                 existing_data = json.loads(content)
        #                 if not isinstance(existing_data, list):
        #                     existing_data = [existing_data]
        #     except json.JSONDecodeError:
        #         existing_data = []
        
        # # Append new data
        # existing_data.append(new_data)
        
        # Write back to file
        with open(output_file, 'a') as f:
            json.dump(new_data, f, indent=2)
            f.write("}")
            
    except Exception as e:
        print(f"Error writing data to file: {e}") 