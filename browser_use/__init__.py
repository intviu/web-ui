"""
Browser use module for virtual business manager.
"""
from .agent.agent import Agent
from .agent.views import AgentHistoryList
from .browser.browser import Browser, BrowserConfig
from .browser.context import BrowserContext, BrowserContextConfig, BrowserContextWindowSize

__all__ = [
    'Agent', 
    'AgentHistoryList', 
    'Browser', 
    'BrowserConfig', 
    'BrowserContext', 
    'BrowserContextConfig', 
    'BrowserContextWindowSize'
] 