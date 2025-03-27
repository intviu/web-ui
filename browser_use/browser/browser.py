from dataclasses import dataclass
from typing import List, Optional, TYPE_CHECKING, Any

# Only import when type checking to avoid circular imports
if TYPE_CHECKING:
    from .context import BrowserContext, BrowserContextConfig
else:
    # Use forward references in runtime
    BrowserContext = Any
    BrowserContextConfig = Any

@dataclass
class BrowserConfig:
    """Configuration for browser instance"""
    headless: bool = False
    disable_security: bool = True
    chrome_instance_path: Optional[str] = None
    extra_chromium_args: List[str] = None
    new_context_config: Optional["BrowserContextConfig"] = None

class Browser:
    """Browser class for automation"""
    
    def __init__(self, config: BrowserConfig):
        self.config = config
        self.contexts: List["BrowserContext"] = []
        
    async def new_context(self, config: Optional["BrowserContextConfig"] = None) -> "BrowserContext":
        """Create a new browser context"""
        # Import here to avoid circular imports
        from .context import BrowserContext
        
        context_config = config or self.config.new_context_config
        if not context_config:
            raise ValueError("No context configuration provided")
            
        context = BrowserContext(self, context_config)
        self.contexts.append(context)
        return context
        
    async def close(self):
        """Close all browser contexts"""
        for context in self.contexts:
            await context.close()
        self.contexts.clear() 