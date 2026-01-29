# Week 8 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **CHOI HONGJUN** \
SUNet ID: **202411913** \
Citations: Bolt documentation, Django REST Framework documentation, Flask documentation, Cursor AI coding assistant


This assignment took me about **2** hours to do. 


## App Concept
```
Developer Control Center is a simple task management web application designed to help developers track and organize their tasks. The app supports creating, viewing, updating, and deleting tasks, along with basic status management (To Do, In Progress, Done). Across all versions, the core functionality remains the same, while different technology stacks are used to explore trade-offs in development speed, control, and complexity.
```


## Version #1 Description
```
APP DETAILS:
===============
Folder name: week8/bolt-app  
AI app generation platform: Bolt  
Tech Stack: Next.js, React, TypeScript  
Persistence: Supabase (PostgreSQL)  
Frameworks/Libraries Used: Next.js App Router, Supabase client, Tailwind CSS, shadcn/ui  
(Optional but recommended) Screenshots of core flows: Not included

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them:  
Delete and update operations initially failed due to Supabase Row Level Security (RLS) restrictions. This was resolved by adjusting the database security configuration to allow unauthenticated CRUD access for demo purposes.

b. Prompting (e.g. what required additional guidance; what worked poorly/well):  
Providing a clear description of the data model, CRUD endpoints, and UI flows in the initial prompt worked well. Additional prompting was required to clarify validation behavior and API route structure.

c. Approximate time-to-first-run and time-to-feature metrics:  
The initial working prototype was generated within minutes. Minor manual fixes and configuration adjustments took additional time, but overall development was significantly faster than manual implementation.
```

## Version #2 Description
```
APP DETAILS:
===============
Folder name: week8/django-app  
AI app generation platform: None  
Tech Stack: Django, Django REST Framework  
Persistence: SQLite  
Frameworks/Libraries Used: Django, Django REST Framework  
(Optional but recommended) Screenshots of core flows: Not included

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them:  
No major issues were encountered. Django REST Framework’s ModelViewSet and router abstractions provided straightforward CRUD functionality with minimal configuration.

b. Prompting (e.g. what required additional guidance; what worked poorly/well):  
This version was primarily implemented manually, with targeted assistance from Cursor for boilerplate REST API code. Clearly specifying file-level responsibilities resulted in clean and predictable output.

c. Approximate time-to-first-run and time-to-feature metrics:  
Time to first run was moderate due to initial project setup and migrations. Core CRUD functionality was implemented quickly once the project structure was in place.
```

## Version #3 Description
```
APP DETAILS:
===============
Folder name: week8/flask-app  
AI app generation platform: None  
Tech Stack: Flask, SQLite, Vanilla JavaScript  
Persistence: SQLite (sqlite3, no ORM)  
Frameworks/Libraries Used: Flask  
(Optional but recommended) Screenshots of core flows: Not included

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them:  
This version required more manual work, particularly around database initialization and request handling. However, the simplicity of the stack made debugging straightforward.

b. Prompting (e.g. what required additional guidance; what worked poorly/well):  
Cursor was used to generate a minimal end-to-end implementation based on a detailed prompt. Explicitly constraining scope (no ORM, no frameworks) was important to avoid unnecessary complexity.

c. Approximate time-to-first-run and time-to-feature metrics:  
Time to first run was very fast due to minimal setup. Implementing basic CRUD features took slightly longer than Version 1 but provided full control over the application logic.
```
