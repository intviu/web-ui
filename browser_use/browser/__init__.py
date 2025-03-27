"""
Browser module for browser automation.
"""
from .browser import Browser, BrowserConfig
from .context import BrowserContextConfig, BrowserContextWindowSize

__all__ = ['Browser', 'BrowserConfig', 'BrowserContextConfig', 'BrowserContextWindowSize'] 