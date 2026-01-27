# Week 5 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **CHOI HONGJUN** \
SUNet ID: **202411913** \
Citations:
\
**FastAPI exception handlers and error responses:** `https://fastapi.tiangolo.com/tutorial/handling-errors/`, `https://fastapi.tiangolo.com/tutorial/handling-errors/#use-the-requestvalidationerror-body` (referenced for global error handling patterns)
\
**Starlette routing/APIRoute context:** `https://www.starlette.io/routing/` (referenced for route wrapping ideas). No other external code was copied.

This assignment took me about **4** hours to do. 


## YOUR RESPONSES
### Automation A: Warp Drive saved prompts, rules, MCP servers

a. Design of each automation, including goals, inputs/outputs, steps
> **Automation A1 — “Design + impact analysis” saved prompt (Warp Drive prompt):**\
> **Goal:** Quickly understand a change (Task 6 extraction/endpoint additions; Task 7 response envelopes) and predict blast radius in tests.
\
> **Inputs:** Short description of intended backend change + current failing test names (when available) + relevant file paths.\
> **Outputs:** A concrete plan: which modules/routes to touch, what invariants must hold (idempotency, API response shapes), and a checklist of likely test updates.\
> **Steps:**
> - Provide the task statement and constraints (backend only, avoid frontend changes).
> - Ask Warp to enumerate impacted endpoints and tests (by pattern: request/response shape, status codes, idempotency semantics).
> - Ask Warp to propose minimal implementation strategy (global vs per-route) and risks.

> **Automation A2 — “Test runner + failure summarizer” saved prompt (Warp Drive prompt):**\
> **Goal:** Tight feedback loop while iterating on backend changes.\
> **Inputs:** pytest command + failure output.\
> **Outputs:** Grouped failure causes (schema mismatch vs behavior mismatch), and suggested next debugging steps.\
> **Steps:** run tests in Warp → paste failure output into the prompt → follow suggested triage ordering.\
>\
> **Automation A3 — Lightweight rule for response contracts (Warp Drive rule):**\
> **Goal:** Keep responses consistent after Task 7.\
> **Inputs:** Any endpoint change.\
> **Outputs:** Reminder checklist: “success responses must be `{ok:true,data:...}`; errors must be `{ok:false,error:{code,message}}`; tests should assert envelope.”\
> **Steps:** Use the rule as a pre-commit mental checklist before running tests.

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before:** I would open files, reason about routes and tests manually, then run pytest and iteratively chase failures one-by-one. Predicting which tests would break (especially after changing response shapes globally) was time-consuming.\
> **After:** With Warp Drive prompts, I front-loaded the “blast radius” analysis: I asked Warp to predict which tests would break and why (envelope shape, status codes, validation errors). This made my edit→test cycles shorter because I usually fixed the right tests/modules first instead of discovering failures gradually.

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> Warp was used in an **advisory** capacity. I did **not** allow Warp to directly edit code files.\
> - **Task 6:** Warp read/analysis + command execution (pytest) only. I manually implemented extraction logic changes and new endpoint behavior.
> - **Task 7:** Warp helped reason about architectural options (global wrapper vs per-route) and ran tests. I manually implemented the global response envelope and then manually updated tests.\
> **Supervision:** I reviewed every suggested change, translated it into explicit code edits myself, and used tests as the final verification gate.

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> Not applicable for Automation A (Warp Drive artifacts). I used single-agent prompts/rules rather than concurrent agents here.

e. How you used the automation (what pain point it resolves or accelerates)
> - **Task 6 (extraction + new endpoint modes):** Warp Drive prompts accelerated upfront design (how preview/apply should behave, and how to enforce apply=true idempotency). It also helped identify which API tests should be added/updated.
> - **Task 7 (global envelopes):** The biggest acceleration was “test impact analysis.” Warp highlighted that many tests would fail due to response shape changes (previously raw JSON vs enveloped). This let me update tests systematically instead of reacting to failures ad hoc.\
> Overall, Warp reduced the time spent on “figuring out what to do next” and increased time spent on actual implementation and verification.



### Automation B: Multi‑agent workflows in Warp 

a. Design of each automation, including goals, inputs/outputs, steps
> **Automation B — Parallel analysis agents (Warp multi-agent workflow):**\
> **Goal:** Split design and verification thinking into parallel roles to reduce context switching.\
> **Agents/roles:**
> - **Design Analyst:** proposes implementation approach and edge cases (e.g., apply=true idempotency, envelope semantics for errors).
> - **Test Impact Analyst:** predicts which tests will fail and what assertions need to change.
> - **Runner/Triage Agent:** interprets pytest failures and suggests the minimal fixes.\
> **Inputs:** Task description + key code locations (routers, services, tests).\
> **Outputs:** Consolidated action plan (files to change + test update checklist) and a prioritized triage list after test runs.\
> **Steps:**
> - Launch parallel agents with the same task goal but different responsibilities.
> - Merge their results into a single plan.
> - Implement manually, then rerun tests; if failing, feed failure output to the Runner/Triage agent.

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before:** I would alternate between designing the change and scanning tests, which caused repeated re-reading of the same files and slower iteration.\
> **After:** Running multi-agent analysis let me get (1) design recommendations and (2) test impact predictions in parallel. This cut down the “back-and-forth” between implementation and test updates—especially for Task 7 where many tests required envelope-aware assertions.

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> Multi-agent runs were still **read/analyze + advise** only. I used Warp agents for:
> - Architectural comparison (global wrapper vs per-route envelopes)
> - Enumerating affected endpoints and tests
> - Interpreting pytest failures
> I kept actual code edits manual to stay in control of correctness and to ensure the changes matched the assignment requirements (backend only, realistic scope).

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> **Coordination strategy:** I gave each agent a narrow objective (design vs test impact vs failure triage) and asked for concrete deliverables (checklists, invariants, likely failing assertions). Then I reconciled differences manually.\
> **Concurrency wins:** Faster “first plan” and faster identification of test breakpoints (particularly the response envelope migration).\
> **Risks/failures:** Occasionally an agent would assume patterns not present in the codebase (e.g., suggesting refactors that would touch frontend). I mitigated this by constraining prompts to backend-only and by validating every suggestion against the actual code/tests.

e. How you used the automation (what pain point it resolves or accelerates)
> - **Task 6:** Multi-agent analysis helped surface edge cases I needed to encode in tests (preview should not persist; apply should persist; apply=true should be idempotent when called repeatedly).
> - **Task 7:** The Test Impact Analyst was most useful: it predicted that nearly every API test would need to assert `{ok, data/error}` instead of raw JSON, and that validation errors should map to the error envelope consistently.\
> This automation mainly reduced time spent auditing the test suite and made the migration less error-prone.
