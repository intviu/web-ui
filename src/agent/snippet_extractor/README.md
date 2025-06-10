The Snippet Extractor Agent is responsible for **finding and returning the most relevant HTML snippet** from a webpage based on a user’s prompt. It is part of the larger `nextSQA` system for automating QA tasks on websites.

---

## Files Overview

### `agent.py`

This is the main engine. It:
- Loads the webpage.
- Splits the HTML into manageable parts (chunks).
- Uses AI to figure out which chunk contains the element the user wants.
- Returns the matching snippet.

### `prompt.py`

This contains the instructions given to the AI (LLM). It:
- Tells the AI what to look for in the webpage HTML.
- Includes example prompts like “test this form” or “click the subscribe button”.
- Provides expected output format.

### `output.py`

Defines the output structure using Pydantic. The AI must return:
```json
{
  "agent_msg": "The snippet ... has been extracted",
  "extracted_snippet": "<html>...</html>",
  "snippet_check": true
}
````

---

## How It Works (Step by Step)

1. The agent opens the webpage
2. It extracts the webpages code and saves into webpage_code.html under webpage directory.
3. It breaks the HTML into chunks, making sure each part is small enough for the AI to handle.
4. It sends each chunk + user prompt to the AI.
5. If the AI finds a match, the agent stops and returns the matching HTML snippet.
6. If nothing is found after checking all parts, it returns a failure response.

---

## Functions Explained

### `__init__(user_prompt, url)`

Sets up the agent with the user prompt and the webpage URL.

---

### `extract_webpage()`

**What it does:**

* Opens the webpage using Playwright (no GUI).
* Grabs all the HTML code.
* calls the store_webpage_code() functionxs

**Why it matters:**
We need the actual webpage content to search for the element the user asked about.

---

### `store_webpage_code()`

**What it does:**

* Saves the downloaded webpage HTML into `webpage/webpage_code.html`.

**Why it matters:**
It gives us a backup copy that can be used for testing, debugging, or sharing.

---

### `chunk_webpage_code()`

**What it does:**

* Breaks the HTML code into smaller "chunks" that fit under a token limit.
* Uses BeautifulSoup to identify sections inside `<body>`.
* Keeps tags and structure intact.
* Handles very large elements by recursively breaking them into smaller ones.

**Why it matters:**
The AI can’t process huge chunks due to token limit. We have to send small, meaningful pieces instead.

**Smart Features:**

* Uses the model’s tokenizer to estimate token size.
* Avoids cutting in the middle of tags.
* Tries to group related elements together when possible.

---

### `run_agent()`

**What it does:**

* Runs the full process:

  1. Extract webpage.
  2. Chunk the HTML.
  3. Send each chunk to the AI.
  4. Return the first valid snippet found.

**Fallback:**
If nothing is found, returns a message saying no snippet was found.

---

## Prompt Examples

**Prompt 1:**

> Test this form
> 🔎 Will extract only the HTML related to a `<form>`.

**Prompt 2:**

> Click the subscribe button
> 🔎 Will extract the section containing the `<button>` for subscribing.

---

## ✅ Output Format (Returned by Agent)

If snippet is found:

```json
{
  "agent_msg": "The snippet ... has been extracted",
  "extracted_snippet": "<section>...</section>",
  "snippet_check": true
}
```

If not found:

```json
{
  "agent_msg": "Unable to find the relevant snippet",
  "extracted_snippet": "No snippet found",
  "snippet_check": false
}
```

---

## Technologies Used

* GPT (via LangChain)
* Playwright (for browsing web pages)
* BeautifulSoup (for parsing HTML)
* tiktoken (for counting tokens)
* Pydantic (for structured output)

---

You can think of this agent like this.:

* Visits a webpage,
* Looks for the thing you asked about (like a form or button),
* Cuts it out from the extracted entire webpage code,
* And gives it to you in a neat little package.
