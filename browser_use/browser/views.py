"""
View models for browser automation.
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class BrowserStateHistory(BaseModel):
    """History of browser state"""
    screenshots: List[str] = []
    texts: List[str] = []
    titles: List[str] = []
    urls: List[str] = [] 