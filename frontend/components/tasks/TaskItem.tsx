'use client';

import { useState } from 'react';
import { apiClient } from '@/lib/api-client';

interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

interface TaskItemProps {
  task: Task;
  onToggle: () => void;
  onDelete: () => void;
  onUpdate?: (updatedTask: Task) => void;
}

export default function TaskItem({ task, onToggle, onDelete, onUpdate }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const updatedTask = await apiClient.updateTask(task.id, title, description || '');
      setIsEditing(false);

      // Call the onUpdate callback if provided
      if (onUpdate) {
        onUpdate({
          ...task,
          title,
          description: description || null,
          updated_at: updatedTask.updated_at || task.updated_at
        });
      }
    } catch (err: any) {
      if (err.message && (err.message.includes('Task not found') || err.message.includes('do not have permission'))) {
        alert('Task not found or you do not have permission to update this task. The task may have been deleted or does not belong to you.');
        // Optionally refresh the task list to reflect current state
        window.location.reload(); // Simple solution to refresh the page
      } else {
        console.error('Error updating task:', err);
        alert('Failed to update task: ' + (err.message || 'Unknown error'));
      }
    }
  };

  return (
    <li className="bg-card p-4 rounded-lg shadow-sm border border-gray-200">
      {isEditing ? (
        <form onSubmit={handleUpdate} className="space-y-3">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
            required
            maxLength={200}
          />
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
            maxLength={1000}
            placeholder="Description (optional)"
            rows={2}
          />
          <div className="flex space-x-2">
            <button
              type="submit"
              className="px-3 py-1 bg-primary text-white rounded hover:bg-blue-700"
            >
              Save
            </button>
            <button
              type="button"
              onClick={() => {
                setIsEditing(false);
                setTitle(task.title);
                setDescription(task.description || '');
              }}
              className="px-3 py-1 bg-secondary text-white rounded hover:bg-teal-700"
            >
              Cancel
            </button>
          </div>
        </form>
      ) : (
        <div className="flex items-start justify-between">
          <div className="flex items-start space-x-3">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={onToggle}
              className="mt-1 h-4 w-4 text-primary rounded focus:ring-primary border-gray-300"
            />
            <div>
              <h3 className={`text-lg ${task.completed ? 'text-text-disabled line-through' : 'text-text-primary'}`}>
                {task.title}
              </h3>
              {task.description && (
                <p className={`mt-1 ${task.completed ? 'text-text-disabled' : 'text-text-secondary'}`}>
                  {task.description}
                </p>
              )}
              <p className="text-xs text-text-secondary mt-1">
                Created: {new Date(task.created_at).toLocaleDateString()}
              </p>
            </div>
          </div>
          <div className="flex space-x-2">
            <button
              onClick={() => setIsEditing(true)}
              className="text-sm bg-secondary text-white px-2 py-1 rounded hover:bg-teal-700"
            >
              Edit
            </button>
            <button
              onClick={onDelete}
              className="text-sm bg-destructive text-white px-2 py-1 rounded hover:bg-red-700"
            >
              Delete
            </button>
          </div>
        </div>
      )}
    </li>
  );
}