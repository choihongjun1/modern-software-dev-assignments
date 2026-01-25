# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **CHOI HONGJUN** \
SUNet ID: **202411913** \
Citations: **Ollama documentation, Cursor IDE**

This assignment took me about **TODO** hours to do. 


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt: 
```
Analyze extract_action_items in this file.
Add a new function extract_action_items_llm(text: str) -> list[str].

The function should:
- Use Ollama with a small local model (phi-3)
- Send the notes to the model
- Ask for ONLY a JSON array of strings as output
- Return an empty list for empty input
- Be robust to malformed model output

Do not modify the existing extract_action_items function.
Add comments explaining the logic.
``` 

Generated Code Snippets:
```
- File: week2/app/services/extract.py
  - Added new function `extract_action_items_llm`
  - Lines: 92–173
```

### Exercise 2: Add Unit Tests
Prompt: 
```
Write unit tests for extract_action_items_llm.

The tests should:
- Import extract_action_items_llm from services.extract
- Test empty input returns an empty list
- Test bullet-point input returns a non-empty list
- Test keyword-based input (e.g. TODO, Action:) returns a list
- Avoid asserting exact string matches, since LLM output is non-deterministic
- Assert only on types, length, and general properties

Add comments explaining why the assertions are written this way.
``` 

Generated Code Snippets:
```
- File: week2/tests/test_extract.py
  - Added tests for extract_action_items_llm
  - Lines: approximately 21–69
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt: 
```
Refactor this router to improve clarity and API contracts.

Replace raw Dict-based request parsing with explicit Pydantic models.
Define clear request and response schemas.
Do not change application behavior.
Add comments explaining the refactoring decisions.
``` 

Generated/Modified Code Snippets:
```
- File: week2/app/routers/action_items.py
  - Replaced Dict-based request/response handling with Pydantic schemas
  - Added explicit request/response models and improved documentation

- File: week2/app/schemas.py
  - Added Pydantic models defining API contracts for action items

- File: week2/app/routers/notes.py
  - Updated endpoints to use typed request/response schemas
```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt: 
```
Add a new endpoint for LLM-based action item extraction.

Requirements:
- Endpoint path: /action-items/extract-llm
- Use extract_action_items_llm instead of extract_action_items
- Reuse the existing ExtractActionItemsRequest and ExtractActionItemsResponse schemas
- Do not change existing endpoints
- Keep behavior consistent with /extract (including save_note support)
``` 
```
Add a new endpoint to list all notes.

Requirements:
- Endpoint path: GET /notes
- Return a list of NoteResponse objects
- Use the existing database helper list_notes()
- Do not modify existing endpoints
``` 
```
Update the frontend to support the new backend features.

Requirements:
1. Add a new button labeled "Extract LLM".
   - When clicked, send the input text to POST /action-items/extract-llm
   - Display the returned action items in the same UI as the existing Extract button

2. Add a new button labeled "List Notes".
   - When clicked, fetch data from GET /notes
   - Display the list of notes (id and content) on the page

3. Do not break existing functionality.
   - The original Extract button using /action-items/extract must continue to work.

4. Keep the UI simple.
   - Plain HTML + JavaScript is sufficient.
   - No styling changes are required.

Add clear comments explaining the new logic.
``` 

Generated Code Snippets:
```
- File: week2/app/routers/action_items.py
  - Added /action-items/extract-llm endpoint using LLM-based extraction

- File: week2/app/routers/notes.py
  - Added GET /notes endpoint to list all notes

- File: frontend/index.html
  - Added "Extract LLM" and "List Notes" buttons
  - Added shared JavaScript logic to call new endpoints and render results
```


### Exercise 5: Generate a README from the Codebase
Prompt: 
```
TODO
``` 

Generated Code Snippets:
```
TODO: List all modified code files with the relevant line numbers.
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 