The **QA Possibility Checker Agent** is like a smart gatekeeper in our AI-based QA automation system. Its job is to check whether the test the user wants to perform can actually be done on the current webpage snippet.


## What This Agent Does

* When a user says something like:
  **"Check if the 'Submit' button works"**

  And the webpage snippet actually includes a `<button>Submit</button>` –
  ✅ The agent will say the test is **possible**.

* But if the user says:
  **"Test the payment gateway"**
  and the snippet has no signs of payment features –
  ❌ The agent will say the test is **not possible**.

The result looks like one of these:

```json
{
  "agent_msg": "QA is possible on the extracted Snippet",
  "qa_possibilty": true
}
```

or

```json
{
  "agent_msg": "QA is not possible on the extracted Snippet",
  "qa_possibilty": false
}
```

---

## How It Works – File by File

### 1. `agent.py` – The Agent Logic

This file contains the class `QAPossibilityChecker`, which runs the entire logic for checking QA feasibility. It has two main parts:

#### a. `__init__(self, user_prompt: str, extracted_snippet: str)`

This function runs when the agent is first created. It:

* Stores the **user's QA prompt** (like "test the login form")
* Stores the **extracted HTML snippet** from the webpage
* Loads the instruction prompt from `prompt.py`
* Sets the expected response format using the Pydantic model `QAPossibiltyChecker`

#### b. `run_agent(self) -> QAPossibiltyChecker`

This is where the real work happens. It:

* Logs that the agent has started
* Sends all the inputs and instructions to `run_main_agent`, which interacts with the AI model
* Logs and returns the result (either `true` or `false`)

### 2. `prompt.py` – The Instructions for the AI

This file holds a long string named `agents_prompt` — it tells the AI model **exactly what to do**.

Example logic it follows:

If the prompt says "Click the signup button", but there's no `<button>` or form in the HTML snippet → return false.

The format is always like this:

```json
{
  "agent_msg": "QA is possible on the extracted Snippet",
  "qa_possibilty": true
}
```

or

```json
{
  "agent_msg": "QA is not possible on the extracted Snippet",
  "qa_possibilty": false
}
```

---

### 3. `output.py` – The Output Schema

This file defines a simple Pydantic class that sets the structure for the agent's response:

```python
class QAPossibiltyChecker(BaseModel):
    agent_msg: str
    qa_possibilty: bool
```

* `agent_msg` gives a short explanation
* `qa_possibilty` is the actual yes/no answer (true or false)

Example valid output:

```json
{
  "agent_msg": "QA is not possible on the extracted Snippet",
  "qa_possibilty": false
}
```

---

## How It Fits in the Big Picture

This agent comes **after** we’ve enhanced the user’s prompt and identified what part of the page to test.

Its job is to **double-check**:

“Is this test actually doable on the provided HTML snippet?”

This helps us avoid wasting time trying to run tests on things that aren’t even present in the UI.


## Summary

* **Goal**: Check if a given QA test can be run on the extracted webpage snippet

* **Input**:

  * A user prompt (like "test the search bar")
  * A portion of the webpage HTML

* **Output**:

```json
{
  "agent_msg": "...",
  "qa_possibilty": true/false
}
```

* **Key Files**: `agent.py`, `prompt.py`, `output.py`
* **Next Step**: If QA is possible → proceed to test execution. If not → skip or alert the user.

