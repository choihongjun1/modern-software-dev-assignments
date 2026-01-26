# Intent
Run the backend test suite in a consistent way and summarize failures.
This command standardizes test execution across platforms (macOS, Linux, Windows).

# Inputs
- $ARGUMENTS (optional): test path or pytest markers
  Examples:
  - backend/tests
  - backend/tests/test_notes.py
  - -k notes

# Steps
1. Run pytest with fast-fail enabled.
2. If tests pass, report success and total runtime.
3. If tests fail:
   - Identify failing test files and test names.
   - Summarize the assertion errors.
   - Suggest likely next steps (e.g., inspect failing module, run single test).

# Output
- A concise test summary:
  - PASS / FAIL
  - Number of tests run
  - Failing tests (if any)
- Suggested follow-up actions when failures occur.

# Safety Notes
- This command is read-only with respect to application data.
- It only executes the test suite and does not modify source files.

# Rollback
- No rollback required. No files are modified by this command.
