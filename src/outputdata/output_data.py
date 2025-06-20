import json
import os
import time
from pathlib import Path

def write_data_to_file(
    agents_name: str,
    number_of_tries: int = 1,
    time_taken: float = 0.0,
    user_input=None,
    output=None,
    evaluation=None,
    memory=None,
    next_goal=None,
    actions=None,
    final_result=None
) -> None:
    try:
        script_dir = Path(__file__).parent
        output_file = script_dir / 'agent_execution.json'
        os.makedirs(script_dir, exist_ok=True)

        # Read existing data safely
        if output_file.exists():
            with open(output_file, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = []
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        #construct new entry
        if agents_name == "Browser Use Agent":
            new_entry = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "agents_name": agents_name,
                "evaluation": evaluation,
                "memory": memory,
                "next_goal": next_goal,
                "actions": actions,
                "final_result": final_result
            }
        else:
            new_entry = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "agents_name": agents_name,
                "number_of_tries": number_of_tries,
                "time_taken": time_taken,
                "user_input": user_input,
                "output": output
            }

        data.append(new_entry)

        #Write entire list back safely
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print(f"❌ Error writing data to file: {e}")