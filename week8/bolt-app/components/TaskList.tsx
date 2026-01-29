'use client';

import { Task } from '@/lib/supabase';
import { TaskItem } from '@/components/TaskItem';

interface TaskListProps {
  tasks: Task[];
  onTaskUpdated: (task: Task) => void;
  onTaskDeleted: (taskId: string) => void;
}

export function TaskList({ tasks, onTaskUpdated, onTaskDeleted }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="text-center py-12 bg-white rounded-lg shadow-sm border border-slate-200">
        <p className="text-slate-500 text-lg">No tasks yet</p>
        <p className="text-slate-400 text-sm mt-2">Create your first task to get started</p>
      </div>
    );
  }

  const tasksByStatus = {
    todo: tasks.filter(task => task.status === 'todo'),
    in_progress: tasks.filter(task => task.status === 'in_progress'),
    done: tasks.filter(task => task.status === 'done'),
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold text-slate-700 mb-3 flex items-center gap-2">
          <span className="w-3 h-3 bg-slate-400 rounded-full"></span>
          To Do ({tasksByStatus.todo.length})
        </h2>
        <div className="space-y-3">
          {tasksByStatus.todo.map(task => (
            <TaskItem
              key={task.id}
              task={task}
              onTaskUpdated={onTaskUpdated}
              onTaskDeleted={onTaskDeleted}
            />
          ))}
        </div>
      </div>

      <div>
        <h2 className="text-xl font-semibold text-slate-700 mb-3 flex items-center gap-2">
          <span className="w-3 h-3 bg-blue-500 rounded-full"></span>
          In Progress ({tasksByStatus.in_progress.length})
        </h2>
        <div className="space-y-3">
          {tasksByStatus.in_progress.map(task => (
            <TaskItem
              key={task.id}
              task={task}
              onTaskUpdated={onTaskUpdated}
              onTaskDeleted={onTaskDeleted}
            />
          ))}
        </div>
      </div>

      <div>
        <h2 className="text-xl font-semibold text-slate-700 mb-3 flex items-center gap-2">
          <span className="w-3 h-3 bg-green-500 rounded-full"></span>
          Done ({tasksByStatus.done.length})
        </h2>
        <div className="space-y-3">
          {tasksByStatus.done.map(task => (
            <TaskItem
              key={task.id}
              task={task}
              onTaskUpdated={onTaskUpdated}
              onTaskDeleted={onTaskDeleted}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
