import gradio as gr

def create_interface():
    with gr.Tab("Run Agent"):
        with gr.Row():
            pdf_upload = gr.File(
                label="Upload PDF (Optional)", 
                file_types=[".pdf"],
                type="binary"
            )
        
        with gr.Row():
            prompt = gr.Textbox(
                label="Prompt",
                placeholder="Enter your prompt here...",
                lines=3
            )
            
        with gr.Row():
            submit_btn = gr.Button("Run")
            
        output = gr.Markdown()
        
        def run_agent_with_pdf(prompt, pdf_file, agent=None):
            if agent is None:
                try:
                    from browser_agent.agent_interface import AgentInterface
                    agent = AgentInterface()
                except ImportError:
                    return "Error: Could not import Agent. Please ensure browser_agent package is installed correctly."
            if pdf_file is not None:
                return agent.run_agent(prompt, pdf_file.name)
            return agent.run_agent(prompt)
            
        submit_btn.click(
            fn=run_agent_with_pdf,
            inputs=[prompt, pdf_upload],
            outputs=output
        ) 