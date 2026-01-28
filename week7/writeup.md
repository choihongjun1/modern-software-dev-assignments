# Week 7 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **CHOI HONGJUN** \
SUNet ID: **202411913** \
Citations: **TODO**

This assignment took me about **TODO** hours to do. 


## Task 1: Add more endpoints and validations
a. Links to relevant commits/issues
> PR: https://github.com/choihongjun1/modern-software-dev-assignments/pull/1


b. PR Description
> This PR completes Task 1 by extending the API with additional endpoints and strengthening input validation and error handling.
\
Changes include adding DELETE endpoints for notes and action items, introducing shared helpers for pagination, sorting, and blank input validation, and enforcing explicit 400 and 404 error responses for invalid inputs and missing resources. Test coverage was also updated to verify correct delete behavior and error handling.


c. Graphite Diamond generated code review
> Graphite Diamond did not flag any issues for this PR ("Graphite Agent found no issues"), indicating that the changes aligned well with common FastAPI and REST best practices.


## Task 2: Extend extraction logic
a. Links to relevant commits/issues
> PR: https://github.com/choihongjun1/modern-software-dev-assignments/pull/2

b. PR Description
> This PR completes Task 2 by extending the action item extraction logic to support more sophisticated pattern recognition and analysis.
\
 The extraction function was enhanced to recognize a broader range of action-oriented expressions, including explicit prefixes (e.g., TODO:, ACTION:), sentence starters (such as "We should", "Please", and "Let's"), and imperative verbs. Additional heuristics were introduced to reduce false positives by filtering out questions, informational statements, and overly vague fragments. Comprehensive unit tests were added to validate the new patterns, ensure correct deduplication, and confirm that non-actionable text is excluded.


c. Graphite Diamond generated code review
> Graphite Diamond initially identified a critical correctness issue in the extraction logic: items matched by explicit prefixes (e.g., TODO:, ACTION:) were not being marked as actionable after normalization and could be incorrectly filtered out. This bug was fixed by explicitly treating prefix matches as actionable signals. After applying the fix, Graphite Diamond reported no remaining issues.


## Task 3: Try adding a new model and relationships
a. Links to relevant commits/issues
> TODO

b. PR Description
> TODO

c. Graphite Diamond generated code review
> TODO

## Task 4: Improve tests for pagination and sorting
a. Links to relevant commits/issues
> TODO

b. PR Description
> TODO

c. Graphite Diamond generated code review
> TODO

## Brief Reflection 
a. The types of comments you typically made in your manual reviews (e.g., correctness, performance, security, naming, test gaps, API shape, UX, docs).
> TODO 

b. A comparison of **your** comments vs. **Graphite’s** AI-generated comments for each PR.
> TODO

c. When the AI reviews were better/worse than yours (cite specific examples)
> TODO

d. Your comfort level trusting AI reviews going forward and any heuristics for when to rely on them.
>TODO 



