The **=Prompt Enhancer Agent** is a key component in our AI-based QA automation system. Its job is to take a user's basic QA prompt (like "test the signup form") and turn it into a clear, step-by-step testing plan. This helps the system better understand what exactly needs to be tested on the webpage.


## What This Agent Does
* When a user says:
  **"Check if the signup form works"**

  The Prompt Enhancer Agent transforms that into something like:
  **"1. Enter a test email. 2. Fill out the password. 3. Click submit. 4. Check for a success message."**

* It uses the **HTML snippet** from the webpage to make the steps more relevant.

* This makes the instructions much more helpful for the next agents in the chain that will actually run the tests.

* The final result looks like this:

```json
{
  "agent_msg": "The prompt has been enhanced",
  "enhanced_prompt": "1. Do this. 2. Do that. 3. Check result..."
}
```

---

## How It Works – File by File

### 1. `agent.py` – The Agent Logic

This file contains the class `PromptEnhancerAgent`, which controls everything this agent does. It has two main parts:

#### a. `__init__(self, user_prompt: str, extracted_snippet: str)`

This function runs when we first create the agent. It:

* Stores the **user’s original prompt**
* Stores the **extracted HTML snippet** from the webpage
* Loads the agent prompts (`agents_prompt`)
* Sets the expected output format using the Pydantic model `PromptEnhancerOutput`

#### b. `run_agent(self) -> PromptEnhancerOutput`

This is where the agent actually runs. It:

* Logs that it started
* Sends the instructions, inputs, and output schema to the shared helper function `run_main_agent` inside of main agent
* Receives the enhanced prompt from the AI and returns it

---

### 2. `prompt.py` – The Instructions for the AI

This file contains a variable named `agents_prompt` — a detailed instruction written in natural language, telling the AI model how to do its job.

It ends with this output format:

```json
{
  "agent_msg": "The prompt has been enhanced",
  "enhanced_prompt": "1. ... 2. ... 3. ..."
}
```

This ensures the output is clean and easy for the next steps in the system to use.

---

### 3. `output.py` – The Output Schema

This file defines the format of the result using a Pydantic class:

```python
class PromptEnhancerOutput(BaseModel):
    agent_msg: str
    enhanced_prompt: str
```

This means the final result will always contain:

* A message confirming that the prompt was enhanced
* A step-by-step version of the original QA request

Example:

```json
{
  "agent_msg": "The prompt has been enhanced",
  "enhanced_prompt": "1. Enter your email. 2. Enter a password. 3. Click login."
}
```

---

## How It Fits in the Big Picture

This agent runs **after** we’ve confirmed that the user request is a valid QA task (using the Intent Classifier Agent), and we’ve extracted the right part of the webpage (via the Snippet Extractor Agent).

Its job is to **translate vague user prompts into clear QA instructions** that the final test executor can follow without confusion.

By enhancing prompts, this agent makes the entire testing process more effective and accurate.

---

## 📌 Summary

* **Goal**: Turn a vague QA prompt into detailed, step-by-step test instructions
* **Input**:

  * A user’s original QA prompt
  * A snippet of webpage HTML
* **Output**:

```json
{
  "agent_msg": "The prompt has been enhanced",
  "enhanced_prompt": "1. Step one. 2. Step two. ..."
}
```

* **Key Files**: `agent.py`, `prompt.py`, `output.py`
* **Next Step**: Send the enhanced prompt to the QA execution engine or possibility checker