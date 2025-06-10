import json
import os
import logging
logger = logging.getLogger(__name__)

def write_data_to_file(
    agents_name: str,
    number_of_tries: str,
    time_taken: int,
    user_input: float,
    output: str
    ) -> None:

    result_data = {
        "Agent Name": agents_name,
        "Number of tries": number_of_tries,
        "TimeTaken": time_taken,
        "User_input": f"HumanMessage: {user_input}",
        "Output": f"SystemMessage: {output}",
    }

    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "agent_execution.json")

    #reading existing data if file exists, else start a new list
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    all_data = json.load(f)
                    if not isinstance(all_data, list):
                        all_data = []
                except json.JSONDecodeError:
                    all_data = []
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            all_data = []
    else:
        all_data = []

    all_data.append(result_data)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(all_data, f, indent=4)
        logger.info(f"Data written to file....")
    except Exception as e:
        logger.error(f"Error writing to file {file_path}: {e}")