# Week 4 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **CHOI HONGJUN** \
SUNet ID: **202411913** \
Citations:
- Claude Code Best Practices (Anthropic Engineering Blog)  
- Claude Code Sub-Agents Overview (Anthropic Documentation)

This assignment took me about **3** hours to do. 


## YOUR RESPONSES
### Automation #1
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> This automation was inspired by the Claude Code best practices, which emphasize creating small, reusable, and idempotent workflows for common developer tasks. During development, I frequently ran the test suite to validate changes, especially after fixing platform-specific issues on Windows. This made test execution a natural candidate for automation.

b. Design of each automation, including goals, inputs/outputs, steps
> **Goal:**  
Standardize and simplify test execution across environments while providing concise feedback when failures occur.

> **Inputs:**  
Optional test path or pytest arguments (e.g. `backend/tests`, `-k notes`)

> **Outputs:**  
Pass/fail summary  
Identification of failing tests (if any)  
Suggested next debugging steps

> **Steps:**  
Run pytest with fast-fail enabled.  
If all tests pass, report success and runtime.  
If tests fail, summarize failing tests and common causes.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> **How to run:**  
`/run-tests`  
or  
`/run-tests backend/tests/test_notes.py`

> **Expected outputs:**  
Clear PASS or FAIL summary  
List of failing test files and test names (if any)  
Short suggestions for next debugging steps when failures occur

> **Safety notes:**  
This automation is read-only with respect to application data and source code.  
It only executes the test suite and does not modify files or database state.

> **Rollback:**  
No rollback is required, as this automation does not change application state.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before automation:**  
Manually running `pytest` in the terminal  
Manually scanning long traceback logs  

> **After automation:**  
Single slash command to run tests  
Immediate summary of failures and suggested next steps

e. How you used the automation to enhance the starter application
> This automation was used repeatedly while extending the starter application, particularly when adding a new endpoint and resolving Windows-specific SQLite teardown issues. It ensured rapid feedback and consistent validation after each change.


### Automation #2
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> This automation was inspired by the Claude Code Sub-Agents overview, which emphasizes decomposing complex development tasks into role-specialized agents. Separating testing and implementation responsibilities enables safer, more reliable changes and mirrors real-world collaborative engineering workflows.

b. Design of each automation, including goals, inputs/outputs, steps
> **Goal:**  
Safely extend the starter application using a test-driven, role-separated workflow that minimizes regressions.

> **Agents:**  
> **TestAgent:**  
Writes failing tests to define new behavior and validate API contracts.  
Confirms failures before implementation begins.  
> **CodeAgent:**  
Implements the required functionality to satisfy failing tests.  
Modifies models, schemas, and routers while preserving existing behavior.

> **Workflow steps:**  
TestAgent writes a failing test describing the desired behavior.  
The failing test is executed to confirm correctness.  
CodeAgent implements the necessary changes.  
Tests are re-run until all tests pass successfully.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> **How to run:**  
Write or update tests using pytest.  
Iteratively implement changes until all tests pass by running `pytest`.

> **Expected outputs:**  
Initially failing tests that define the new feature.  
A fully passing test suite after implementation is complete.

> **Safety notes:**  
All changes are validated through automated tests before being considered complete.  
This workflow reduces the risk of regressions.

> **Rollback:**  
If tests fail or behavior is incorrect, changes can be reverted using version control.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before automation:**  
Feature changes were reasoned about manually without enforced test-first validation.  
Higher risk of introducing subtle regressions.

> **After automation:**  
Behavior is defined explicitly through tests before implementation.  
Clear separation of responsibilities between testing and coding.  
Higher confidence in correctness through automated verification.

e. How you used the automation to enhance the starter application
> Using the TestAgent–CodeAgent workflow, I added support for marking notes as completed in the starter application. A failing test was first written to specify the expected behavior of the new endpoint. The CodeAgent then implemented the required database model updates, schema changes, and routing logic until all tests passed, demonstrating an effective autonomous coding workflow.