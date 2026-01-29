# Developer Control Center

A full-stack task management web application for developers to track tasks and notes.

## Tech Stack

- **Frontend**: Next.js 13 with React, TypeScript, and Tailwind CSS
- **Backend**: Next.js API Routes
- **Database**: Supabase (PostgreSQL)
- **UI Components**: shadcn/ui

## Features

- Create, read, update, and delete tasks
- Organize tasks by status (To Do, In Progress, Done)
- Edit task titles and descriptions inline
- Real-time task status updates
- Clean, responsive UI with loading and error states
- Form validation and error handling

## Database Schema

The application uses a single `tasks` table with the following structure:

```sql
tasks {
  id          uuid (primary key)
  title       text (required)
  description text (optional)
  status      text (enum: 'todo', 'in_progress', 'done')
  created_at  timestamptz
  updated_at  timestamptz (auto-updated)
}
```

## API Endpoints

- `GET /api/tasks` - Fetch all tasks
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/:id` - Update an existing task
- `DELETE /api/tasks/:id` - Delete a task

## Getting Started

### Prerequisites

- Node.js 18+ installed
- A Supabase account and project

### Installation

1. Clone the repository and install dependencies:

```bash
npm install
```

2. Set up environment variables:

The Supabase connection details should already be configured in your `.env` file:

```
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

3. The database schema has already been applied via Supabase migrations.

### Running the Application

Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:3000`.

### Building for Production

Build the application:

```bash
npm run build
```

Start the production server:

```bash
npm start
```

## Project Structure

```
project/
├── app/
│   ├── api/
│   │   └── tasks/          # API route handlers
│   │       ├── route.ts    # GET, POST endpoints
│   │       └── [id]/
│   │           └── route.ts # PUT, DELETE endpoints
│   ├── globals.css         # Global styles
│   ├── layout.tsx          # Root layout
│   └── page.tsx            # Main page component
├── components/
│   ├── ui/                 # shadcn/ui components
│   ├── TaskForm.tsx        # Task creation form
│   ├── TaskList.tsx        # Task list with status groups
│   └── TaskItem.tsx        # Individual task card
├── lib/
│   ├── supabase.ts         # Supabase client setup
│   └── utils.ts            # Utility functions
└── package.json
```

## Usage

### Creating a Task

1. Enter a task title (required)
2. Optionally add a description
3. Click "Create Task"

### Updating a Task

- Click the pencil icon to edit the title and description
- Use the status dropdown to change between To Do, In Progress, and Done

### Deleting a Task

- Click the trash icon
- Confirm the deletion in the dialog

## Error Handling

The application includes comprehensive error handling:

- Client-side validation (e.g., empty titles)
- Server-side validation with proper HTTP status codes
- User-friendly error messages
- Loading states for async operations

## Development Notes

- All components use TypeScript for type safety
- The UI uses Tailwind CSS for styling
- Forms include proper validation and error display
- API routes follow REST conventions
- Database operations use Supabase client library
