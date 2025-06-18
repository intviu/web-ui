import os
import logging
from pathlib import Path
from playwright.async_api import async_playwright, Browser, BrowserContext

logger = logging.getLogger(__name__)

class BrowserRecorder:
    def __init__(self):
        self.video_dir = None
        self.context = None
        self.is_recording = False
        
    async def setup_recording(self, browser: Browser) -> BrowserContext:
        """Set up video recording right before browser launch"""
        try:
            # Create videos directory in outputdata
            self.video_dir = os.path.join(os.getcwd(), "outputdata", "videos")
            os.makedirs(self.video_dir, exist_ok=True)
            
            logger.info(f"\n🎥 Setting up video recording in: {self.video_dir}")
            
            # Create context with video recording
            self.context = await browser.new_context(
                record_video_dir=self.video_dir,
                record_video_size={"width": 1280, "height": 720}
            )
            
            # Verify recording is enabled
            self.is_recording = True
            logger.info("✅ Video recording successfully enabled")
            
            # Add listener for new pages
            async def on_page(page):
                logger.info(f"🎥 Starting recording for page: {page.url}")
                # Force start recording for this page
                await page.video.start()
                
            self.context.on("page", on_page)
            
            return self.context
            
        except Exception as e:
            logger.error(f"❌ Failed to setup video recording: {str(e)}")
            self.is_recording = False
            # Return regular context if recording fails
            return await browser.new_context()
            
    def is_video_recording(self) -> bool:
        """Check if video recording is active"""
        return self.is_recording
        
    async def save_recording(self):
        """Save the recording when browser closes"""
        if self.context and self.is_recording:
            try:
                # Get all pages
                pages = self.context.pages
                for page in pages:
                    if page.video:
                        # Save video for this page
                        video_path = await page.video.path()
                        logger.info(f"💾 Saved video recording to: {video_path}")
                        
            except Exception as e:
                logger.error(f"❌ Failed to save video recording: {str(e)}") 