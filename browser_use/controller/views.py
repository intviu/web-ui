"""
View models for browser controller.
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class ActionResult(BaseModel):
    """Result of an action"""
    success: bool = True
    error: Optional[str] = None
    extracted_content: Optional[str] = None
    
class DoneAction(BaseModel):
    """Action to indicate the task is complete"""
    message: str = "Task completed successfully"
    
class ClickElementAction(BaseModel):
    """Action to click an element"""
    selector: str
    
class InputTextAction(BaseModel):
    """Action to input text"""
    selector: str
    text: str
    
class GoToUrlAction(BaseModel):
    """Action to navigate to a URL"""
    url: str
    
class ScrollAction(BaseModel):
    """Action to scroll the page"""
    direction: str = "down"
    amount: int = 1
    
class ExtractPageContentAction(BaseModel):
    """Action to extract content from the page"""
    selector: Optional[str] = None
    
class SearchGoogleAction(BaseModel):
    """Action to search on Google"""
    query: str
    
class OpenTabAction(BaseModel):
    """Action to open a new tab"""
    url: Optional[str] = None
    
class SwitchTabAction(BaseModel):
    """Action to switch to a different tab"""
    tab_index: int
    
class SendKeysAction(BaseModel):
    """Action to send keyboard keys"""
    keys: str 