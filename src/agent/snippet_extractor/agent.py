import logging
from .output import SnippetExtractorOutput
from .prompt import agents_prompt
from ..main_agent.agent import run_main_agent
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import os
import tiktoken

logger = logging.getLogger(__name__)

class SnippetExtractorAgent:
    def __init__(self, user_prompt: str, url: str) -> None:
        logger.info("Initializing SnippetExtractorAgent")
        self.output_pydantic_class = SnippetExtractorOutput
        self.user_prompt = user_prompt
        self.agent_prompt = agents_prompt
        self.url = url

    def store_webpage_code(self) -> bool:
        logger.info("Storing webpage code into webpage_code.html under webpage directory....")
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            webpage_dir = os.path.abspath(os.path.join(base_dir, '..', '..', 'webpage'))
            file_path = os.path.join(webpage_dir, "webpage_code.html")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.webpage_code)
            logger.info(f"Webpage code stored at {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error storing webpage code: {e}")
            return False

    async def extract_webpage(self) -> bool:
        logger.info(f"Extracting webpage for URL: {self.url}")
        self.webpage_code = ""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(self.url)
                content = await page.content()
                logger.info("Webpage content fetched successfully.")
                await browser.close()
                logger.info("Browser closed.")
                self.webpage_code = content

            if self.webpage_code == "":
                return False

            return self.store_webpage_code()

        except Exception as e:
            logger.error(f"Error extracting webpage: {e}")
            return False

    def chunk_webpage_code(self, max_total_tokens=6000, overlap_tokens=1500, model="gpt-4o"):
        enc = tiktoken.encoding_for_model(model)
        soup = BeautifulSoup(self.webpage_code, 'html.parser')
        body = soup.body
        if not body:
            logger.warning("No <body> tag found in HTML; returning full code as single chunk.")
            return [self.webpage_code]

        prompt_tokens = len(enc.encode(self.user_prompt or ""))
        max_chunk_tokens = max_total_tokens - prompt_tokens
        if max_chunk_tokens <= 0:
            raise ValueError("max_total_tokens must be greater than user prompt token length")

        chunks = []
        current_chunk_elements = []
        current_chunk_token_count = 0

        def flush_chunk():
            nonlocal current_chunk_elements, current_chunk_token_count
            if current_chunk_elements:
                chunk_html = "".join(str(el) for el in current_chunk_elements)
                chunks.append(chunk_html)
                current_chunk_elements = []
                current_chunk_token_count = 0

        def chunk_element(element):
            nonlocal current_chunk_elements, current_chunk_token_count

            element_html = str(element)
            element_tokens = len(enc.encode(element_html))

            if element_tokens > max_chunk_tokens:
                #element is too large, try recursively splitting children
                children = list(element.children)
                if not children:
                    #if no children: splitting string content into token-sized slices
                    if hasattr(element, 'string') and element.string:
                        raw_text = str(element.string)
                        tokenized = enc.encode(raw_text)
                        for i in range(0, len(tokenized), max_chunk_tokens):
                            chunk_text = enc.decode(tokenized[i:i + max_chunk_tokens])
                            chunks.append(f"<{element.name}>{chunk_text}</{element.name}>")
                    else:
                        logger.warning("Element too large and no children or string to split; skipping.")
                    return

                #flush current chunk before recursive split
                if current_chunk_elements:
                    flush_chunk()

                #recursively chunk each child element
                for child in children:
                    chunk_element(child)

            else:
                #element fits in chunk, add or flush then add
                if current_chunk_token_count + element_tokens <= max_chunk_tokens:
                    current_chunk_elements.append(element)
                    current_chunk_token_count += element_tokens
                else:
                    flush_chunk()
                    current_chunk_elements.append(element)
                    current_chunk_token_count = element_tokens

        #start chunking all top-level body elements
        for el in body.find_all(recursive=False):
            chunk_element(el)

        #flush last chunk if any
        flush_chunk()

        logger.info(f"Chunked webpage into {len(chunks)} parts, max tokens per chunk (excluding prompt): {max_chunk_tokens}")
        return chunks


    async def run_agent(self) -> SnippetExtractorOutput:
        logger.info(f"Running Snippet Extractor Agent....")

        if not await self.extract_webpage():
            return {
                'actuall_snippet': "",
                "snippet_check": False,
            }

        chunks = self.chunk_webpage_code()

        enc = tiktoken.encoding_for_model("gpt-4o")

        for i, chunk in enumerate(chunks):
            logger.info(f"Processing chunk {i+1}/{len(chunks)}")

            prompt_tokens = len(enc.encode(self.user_prompt))
            chunk_tokens = len(enc.encode(chunk))
            total_tokens = prompt_tokens + chunk_tokens
            logger.info(f"Token usage: prompt={prompt_tokens}, chunk={chunk_tokens}, total={total_tokens}")

            output = run_main_agent(
                output_pydantic_class=self.output_pydantic_class,
                agents_name="Snippet Extractor Agent",
                agents_prompt=self.agent_prompt,
                input_to_prompt={
                    'input': self.user_prompt,
                    'webpage_code': chunk
                }
            )
            if output.snippet_check:
                logger.info(f"Snippet found in chunk {i+1}")
                return output

        logger.info("No valid snippet found after processing all chunks.")
        return {
            'actuall_snippet': "",
            "snippet_check": False,
        }