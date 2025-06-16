import json
import os
import time
from pathlib import Path

def write_data_to_file(
    agents_name: str,
    number_of_tries: int,
    time_taken: float,
    user_input: str,
    output: str
    ) -> None:
    """
    Appends agent execution data to agent_execution.json in the outputdata directory.
    Handles different formats for 'Browser Use Agent' and other agents.
    """
    try:
        script_dir = Path(__file__).parent
        output_file = script_dir / 'agent_execution.json'
        os.makedirs(script_dir, exist_ok=True)

        # Load existing data if file exists
        if output_file.exists():
            with open(output_file, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        # Create new data entry
        if agents_name == "Browser Use Agent":
            new_data = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "evaluation_previous_goal": user_input,
                "memory": output,
                "next_goal": agents_name,
                "actions": number_of_tries
            }
        else:
            new_data = {
                "agents_name": agents_name,
                "number_of_tries": number_of_tries,
                "time_taken": time_taken,
                "user_input": user_input,
                "output": output
            }

        data.append(new_data)

        # Write updated data back to file
        with open(output_file, 'a') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error writing data to file: {e}") 