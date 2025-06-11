
The Intent Classifier Agent is the first component in our AI-based QA automation system. Its main role is to decide whether a user's request is about testing a webpage or completely unrelated. This helps the system ignore non-testing prompts early, saving time and resources.

What This Agent Does
- When a user sends a message like: "Check if the login button works"
- The Intent Classifier Agent will recognize this as a valid QA task and pass it on to the next agent in the  chain.

- But if the user says: "How do I use ChatGPT to write an essay?"
- Then the agent will mark it as not related to QA, and the system will stop there.

The agent gives a simple true or false answer in this format:

{ "intent": true }
or
{ "intent": false }

How It Works – File by File

1. agent.py – The Agent Logic
This file contains the class IntentClassifierAgent, which manages the entire logic. It does three main things:

    a. __init__(self, user_prompt: str):
        This function is called when we first create the agent. It:
        - Stores the user’s input (their message)
        - Loads the classification prompt
        - Tells the system which output structure to expect (a Pydantic class)
    
    b. run_agent(self) -> IntentClassifierOutput:
        This function starts the classification process. It:
        - Logs that the agent is running
        - Sends everything (prompt, input, expected output format) to a helper function called run_main_agent which handles actual interaction with the AI model
        - Returns the result (either true or false)


2. prompt.py – The Instruction for the AI
This file contains a variable called agents_prompt, which is the natural-language instruction given to the AI model. It includes:

    - Clear criteria for what counts as a QA-related task
    - A few examples of QA prompts vs. non-QA prompts (few shot learning technique)
    - A placeholder {input} where the user’s query is inserted
    - This prompt ensures the AI is focused on classifying only QA-relevant commands.

3. output.py – The Output Schema
This file defines a simple Pydantic model called IntentClassifierOutput:

    - class IntentClassifierOutput(BaseModel):
        intent: bool

    - This means the final answer must look like this:
        { "intent": true } 
               or
        { "intent": false }

This structured format makes it easy for the next parts of the system to read and act on.

How It Fits in the Big Picture
This agent is the first step in the AI pipeline.

If the user request is QA-related (intent: true), we move on to the Snippet Extractor Agent.
If it’s not QA-related (intent: false), the workflow stops early, saving time and computation.
This makes our system more intelligent, cost-efficient, and focused.

Summary
Goal: Filter out non-QA requests
Input: A single user message
Output: { "intent": true } or { "intent": false }
Key Files: agent.py, prompt.py, output.py
Next Step: Trigger next agent only if intent is true