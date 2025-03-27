from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING, Any

# Only import when type checking to avoid circular imports
if TYPE_CHECKING:
    from .browser import Browser
else:
    # Use forward references in runtime
    Browser = Any

@dataclass
class BrowserContextWindowSize:
    """Window size configuration for browser context"""
    width: int = 1920
    height: int = 1080

@dataclass
class BrowserContextConfig:
    """Configuration for browser context"""
    trace_path: Optional[str] = None
    save_recording_path: Optional[str] = None
    no_viewport: bool = False
    browser_window_size: Optional[BrowserContextWindowSize] = None

class BrowserContext:
    """Browser context for automation"""
    
    def __init__(self, browser: "Browser", config: BrowserContextConfig):
        self.browser = browser
        self.config = config
        
    async def __aenter__(self):
        """Context manager entry"""
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        await self.close()
        
    async def close(self):
        """Close the browser context"""
        if self in self.browser.contexts:
            self.browser.contexts.remove(self) 