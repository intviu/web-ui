#make enums of models like gpt4 gpt4o
from enum import Enum
from typing import List, Dict, Any

class AIModel(Enum):
    GPT_4 = "gpt-4"
    GPT_4O = "gpt-4o"
    Ollama_DeepSeek_14b = "deepseek-r1:14b"