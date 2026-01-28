# Week 6 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **CHOI HONGJUN** \
SUNet ID: **202411913** \
Citations: Semgrep documentation (subprocess-shell-true rule), OWASP Top 10 (Injection), Cursor (AI coding assistant)


This assignment took me about **TODO** hours to do. 


## Brief findings overview 
> Semgrep reported one confirmed, real finding that I fixed in this codebase: an OS Command Injection risk in the FastAPI debug endpoint `GET /notes/debug/run`. The endpoint executed user-controlled input via `subprocess.run(..., shell=True, ...)`, which Semgrep flagged under the rule **`subprocess-shell-true`**. I mitigated the issue by removing `shell=True` and restricting execution to a strict allowlist of safe commands invoked with `shell=False` and an argument list.

## Fix #1
a. File and line(s)
> `week6/backend/app/routers/notes.py` — `debug_run` endpoint (`@router.get("/debug/run")`), around lines **108–142** (exact line numbers may shift slightly after edits).

b. Rule/category Semgrep flagged
> Semgrep rule: **`subprocess-shell-true`** (category: OS Command Injection via shell execution).

c. Brief risk description
> The endpoint accepted a query parameter `cmd` and passed it directly to `subprocess.run(cmd, shell=True, ...)`. Because `cmd` is user-controlled and `shell=True` invokes a system shell, an attacker could inject arbitrary shell metacharacters and execute unintended commands on the server (OS Command Injection / remote code execution risk).

d. Your change (short code diff or explanation, AI coding tool usage)
> I changed only the `/debug/run` endpoint implementation:\
> - Removed `shell=True`.\
> - Replaced dynamic execution of `cmd` with a strict allowlist mapping of supported commands (e.g., `whoami`, `pwd`, `ls`) to fixed argument lists.\
> - Executed the allowlisted commands via `subprocess.run(args, shell=False, ...)`.\
> - If `cmd` is not in the allowlist, the endpoint returns the same response shape (`returncode`, `stdout`, `stderr`) but refuses execution with a clear error message.\
>\
> **AI tool usage:** I used **Cursor** as an AI coding assistant to help identify the minimal safe change that satisfies Semgrep (remove `shell=True`) while preserving the route name and response format. I reviewed and applied the final patch myself.

e. Why this mitigates the issue
> This mitigates OS Command Injection by eliminating shell interpretation (`shell=False`) and preventing arbitrary command execution through a strict allowlist. With `shell=False` and a fixed argument list, user input is no longer parsed by a shell, and only explicitly permitted commands can run. Any non-allowlisted input is rejected without execution, removing the attacker’s ability to run arbitrary OS commands via the endpoint.

## Fix #2
a. File and line(s)
> TODO

b. Rule/category Semgrep flagged
> TODO

c. Brief risk description
> TODO

d. Your change (short code diff or explanation, AI coding tool usage)
> TODO

e. Why this mitigates the issue
> TODO

## Fix #3
a. File and line(s)
> TODO

b. Rule/category Semgrep flagged
> TODO

c. Brief risk description
> TODO

d. Your change (short code diff or explanation, AI coding tool usage)
> TODO

e. Why this mitigates the issue
> TODO