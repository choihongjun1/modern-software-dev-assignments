# Week 7 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **CHOI HONGJUN** \
SUNet ID: **202411913** \
Citations: 
- Graphite Diamond AI Code Review (https://graphite.dev)
- FastAPI Documentation (https://fastapi.tiangolo.com/)
- SQLAlchemy ORM Documentation (https://docs.sqlalchemy.org/)


This assignment took me about **4** hours to do. 


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
> PR: https://github.com/choihongjun1/modern-software-dev-assignments/pull/3

b. PR Description
> This PR completes Task 3 by introducing a new Project model and establishing a one-to-many relationship between projects and notes.
\
 A new Project entity was added, and the Note model was updated to optionally reference a project via a foreign key. The API was extended to support creating projects, fetching individual projects, and retrieving notes associated with a specific project. Additional validation was added to prevent notes from being associated with non-existent projects.


c. Graphite Diamond generated code review
> Graphite Diamond completed an automated review and did not surface any issues ("Graphite Agent found no issues"). The absence of findings suggested that the new model, relationships, and API changes followed common SQLAlchemy and FastAPI best practices.


## Task 4: Improve tests for pagination and sorting
a. Links to relevant commits/issues
> PR: https://github.com/choihongjun1/modern-software-dev-assignments/pull/4

b. PR Description
> This PR completes Task 4 by improving test coverage for pagination and sorting functionality across the application.
\
Additional tests were added to explicitly verify pagination behavior using skip and limit parameters, as well as sorting behavior using the sort query parameter. Both successful and error cases were covered to ensure that valid sort fields produce correctly ordered results and invalid sort fields return appropriate errors.


c. Graphite Diamond generated code review
> Graphite Diamond completed an automated review and did not surface any issues ("Graphite Agent found no issues"). The lack of findings indicated that the added tests aligned well with existing pagination and sorting logic and followed common testing best practices.


## Brief Reflection 
a. The types of comments you typically made in your manual reviews (e.g., correctness, performance, security, naming, test gaps, API shape, UX, docs).
> In my manual reviews, I primarily focused on correctness, data integrity, and API behavior. This included checking edge cases, validating database relationships and foreign keys, ensuring consistent error handling, and verifying that test coverage reflected real usage scenarios. I also paid attention to API shape and schema boundaries to avoid unnecessary coupling or overexposure of internal data.


b. A comparison of **your** comments vs. **Graphite’s** AI-generated comments for each PR.
> Overall, my manual reviews tended to focus on intent and edge cases, while Graphite’s AI-generated reviews focused on validating structural correctness and common best practices. In Task 2, the AI review was especially valuable in identifying a subtle logic bug that I initially missed. In Tasks 1, 3, and 4, the AI reviews did not raise issues and instead served as confirmation that the implementations aligned with standard patterns.


c. When the AI reviews were better/worse than yours (cite specific examples)
> The AI review outperformed my manual review in Task 2 by catching a correctness bug where prefix-based action items (e.g., TODO:, ACTION:) were not being marked as actionable after normalization. This issue could have caused expected behavior to silently break. In contrast, my manual reviews were more effective in Tasks 1 and 3, where I added explicit validation logic (such as preventing notes from referencing non-existent projects) and made design decisions around schema boundaries that the AI did not comment on.


d. Your comfort level trusting AI reviews going forward and any heuristics for when to rely on them.
> I am comfortable using AI reviews as a first-pass validation tool to check for common mistakes, style issues, and structural correctness. However, I do not fully rely on AI reviews for complex logic, data relationships, or domain-specific decisions. Going forward, my heuristic is to use AI reviews for breadth and consistency checks, while relying on manual review for depth, correctness, and design intent.




