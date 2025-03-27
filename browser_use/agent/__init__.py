"""
Agent module for browser automation.
"""
from .agent import Agent
from .email_agent import EmailAgent
from .views import AgentHistoryList

__all__ = ['Agent', 'EmailAgent', 'AgentHistoryList'] 