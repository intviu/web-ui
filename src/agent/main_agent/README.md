Here is a revised, focused `README.md` for your `mainAgent/agent.py` file. It:
# `mainAgent/agent.py` – Universal AI Agent Executor

This module provides a reusable utility to execute **any AI agent** using LangChain + OpenAI with structured output, retry logic, prompt templating, and logging.

---

## Overview

This file contains:

* `run_main_agent(...)` — Main entry point to run an agent
* `get_chatprompt_templates(...)` — Builds a LangChain `ChatPromptTemplate` using system and human messages
* Logging and retry logic
* Execution data logging via `write_data_to_file(...)`

---

## 🔧 Function: `get_chatprompt_templates(...)`

```python
def get_chatprompt_templates(agents_prompt: str, input_keys: list[str]) -> ChatPromptTemplate
```

### Purpose:

Constructs a `ChatPromptTemplate` that defines how the system and user interact with the AI model.

### How It Works:

1. Escapes `{` and `}` in the `agents_prompt` to prevent unintended format errors.
2. Wraps the `agents_prompt` inside a `SystemMessagePromptTemplate` – this sets the model's role/instructions.
3. Builds a `HumanMessagePromptTemplate` from input keys like:

4. Combines both into a single `ChatPromptTemplate`, used as the model’s full prompt.

---

## Function: `run_main_agent(...)`

```python
def run_main_agent(
    output_pydantic_class,
    agents_name: str,
    agents_prompt: str,
    input_to_prompt: dict,
    model_name: Optional[AIModel] = AIModel.GPT_4O,
) -> Any
```

### Purpose:

Runs a full agent pipeline: builds a prompt, invokes an OpenAI model with structured output, retries if needed, and logs the results.

### Parameters:

* `output_pydantic_class`: A Pydantic model that defines the structure of the expected AI output.
* `agents_name`: String name of the agent (used for logs and file output).
* `agents_prompt`: Instruction string that guides the AI’s behavior.
* `input_to_prompt`: Dictionary of inputs (e.g., `{"user_query": ..., "url": ...}`) to be inserted into the prompt.
* `model_name`: (Optional) Enum value representing the LLM to use (default: GPT-4o).

---

### Core Logic Steps:

#### 1. **Model Initialization**

```python
ChatOpenAI(...).with_structured_output(output_pydantic_class)
```

* Initializes an OpenAI chat model wrapped with `with_structured_output`, ensuring output adheres to the given Pydantic schema.

#### 2. **Prompt Construction**

```python
chat_prompt = get_chatprompt_templates(agents_prompt, input_to_prompt.keys())
```

* Combines system instructions and user input fields into a structured prompt.

#### 3. **LangChain `Runnable`**

```python
chain = chat_prompt | llm_model
```

* Constructs a LangChain chain: a pipeline where the formatted prompt is passed to the model.

#### 4. **Retry Logic (Up to 5 Attempts)**

```python
while MAX_TRIES <= 5:
```

* If the model throws an exception (e.g., parsing, rate limits), it retries with modified prompt.
* The original prompt is updated to include the error message as context, which helps the model avoid repeating the same failure.

```python
error_context = f"{agents_prompt}\n\n[ERROR MESSAGE FOR AGENT CONTEXT]: {str(e)}"
```

#### 5. **Logging**

* Logs the attempt number, error if any, and success/failure using the `logging` module.
* Measures total time taken using `time.time()`.

#### 6. **Data Output**

```python
write_data_to_file(...)
```

* Saves the execution metadata and results into a structured JSON file.
* Includes:

  * Agent name
  * Number of tries
  * Time taken
  * Input values
  * Final output

---

This enables later analysis, debugging, or benchmarking.

---

## Summary

This module abstracts away the complexity of:

* Prompt formatting
* Structured model responses
* Error handling and retry logic
* Timing and logging

It lets developers easily run any prompt-based AI agent with clean, consistent behavior and outputs.