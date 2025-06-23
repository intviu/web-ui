import logging
from .output import QAPossibilityCheckerOutput
from .prompt import agents_prompt
from ..main_agent.agent import run_main_agent
import logging
import asyncio
from playwright.async_api import async_playwright
import os
import base64
from openai import OpenAI
import time


logger = logging.getLogger(__name__)

class QAPossibilityChecker:
    def __init__(self, llm: str, 
                 user_prompt: str, 
                 url: str
                 ) -> None:
        logger.info("Initializing QAPossibilityChecker")
        self.output_pydantic_class = QAPossibilityCheckerOutput
        self.user_prompt = user_prompt
        self.agent_prompt = agents_prompt
        self.url = url
        self.llm = llm
        self.client = OpenAI()

    async def take_screenshot(self, save_path: str) -> bool:
        try:
            logger.info(f"\nTaking screenshot...")
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(self.url, timeout=60000, wait_until="networkidle")
                
                # Simulate scroll to load dynamic content
                # await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(2)

                # Optional: scroll multiple times for infinite scrolling pages
                for _ in range(6):
                    await page.mouse.wheel(0, 1000)
                    await asyncio.sleep(1)

                # # Final wait for animations or delayed JS
                # await asyncio.sleep(3)

                await page.screenshot(path=save_path, full_page=True)
                await browser.close()
                logger.info(f"Screenshot saved at: {save_path}")
                return True
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return False
    
    
    def get_image_fileId(self) -> str:
        logger.info("Extracting image file ID...")
        try:
            with open("screenshot.png", "rb") as image_file:
                image_file_id = self.client.files.create(file=image_file, purpose="vision").id
                logger.info(f"Image file ID extracted: {image_file_id}")
                return image_file_id

        except Exception as e:
            logger.error(f"Error extracting base64 image: {e}")
            return ""

    def run_agent(self) -> QAPossibilityCheckerOutput:

        if asyncio.run(self.take_screenshot("screenshot.png")):
            image_file_id = self.get_image_fileId()
            if image_file_id:

                output = run_main_agent(
                    output_pydantic_class=self.output_pydantic_class,
                    agents_name="QA POSSIBILTY CHECKER",
                    agents_prompt=self.agent_prompt,
                    input_to_prompt={
                        "input": self.user_prompt,
                        "image_file_id": image_file_id
                    },
                    model_name=self.llm
                )
                logger.info(f"QA Possibilty Checker finished Output...: {output}")
                return output
        
        return QAPossibilityCheckerOutput(
            agent_msg="Failed to take screenshot or extract base64 image.",
            qa_possibility=False
        )