from PyPDF2 import PdfReader
import os

class AgentInterface:
    def __init__(self):
        self.uploaded_pdf_content = None

    def read_pdf(self, pdf_path):
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return None

    async def run_agent(self, prompt, uploaded_file=None):
        if uploaded_file:
            pdf_content = self.read_pdf(uploaded_file)
            if pdf_content:
                # Combine PDF content with user prompt
                enhanced_prompt = f"PDF Content:\n{pdf_content}\n\nUser Question/Prompt:\n{prompt}"
                prompt = enhanced_prompt
            
        # ... rest of existing run_agent code ... 