"""
Utilities for browser automation.
"""
import sys
import time
import functools
import asyncio
from typing import Callable, Any
from pathlib import Path

# Add src to Python path
src_dir = str(Path(__file__).parent.parent / "src")
if src_dir not in sys.path:
    sys.path.append(src_dir)

# Import from the existing utils modules
from utils.utils import get_llm_model
from utils.llm import DeepSeekR1ChatOpenAI, DeepSeekR1ChatOllama

def time_execution_async(name: str):
    """Decorator to measure the execution time of an async function"""
    def decorator(fn):
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            result = await fn(*args, **kwargs)
            end_time = time.time()
            print(f"{name} took {end_time - start_time:.3f} seconds")
            return result
        return wrapper
    return decorator

__all__ = ["get_llm_model", "DeepSeekR1ChatOpenAI", "DeepSeekR1ChatOllama", "time_execution_async"] 