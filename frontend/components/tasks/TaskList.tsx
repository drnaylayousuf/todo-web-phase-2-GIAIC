'use client';

import { useState, useEffect } from 'react';
import TaskItem from './TaskItem';
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

import { useCallback } from 'react';

import { forwardRef, useImperativeHandle } from 'react';

export interface TaskListRef {
  refetch: () => void;
}

const TaskList = forwardRef<TaskListRef>((props, ref) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchTasks = useCallback(async () => {
    try {
      const data = await apiClient.getTasks();
      setTasks(data);
      setError('');
    } catch (err: any) {
      setError(err.message || 'An error occurred while fetching tasks');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  useImperativeHandle(ref, () => ({
    refetch: fetchTasks
  }));

  const handleTaskToggle = async (id: number) => {
    try {
      // Optimistic update: update UI immediately, then revert if API fails
      setTasks(tasks.map(task =>
        task.id === id ? { ...task, completed: !task.completed } : task
      ));

      await apiClient.toggleTaskCompletion(id);
    } catch (err: any) {
      // If API fails, revert the optimistic update
      setTasks(tasks.map(task =>
        task.id === id ? { ...task, completed: !task.completed } : task
      ));
      console.error('Error toggling task:', err);
    }
  };

  const handleTaskDelete = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this task? This action cannot be undone.')) {
      return;
    }

    try {
      // Optimistic update: remove task from UI immediately, then revert if API fails
      const taskToDelete = tasks.find(task => task.id === id);
      if (!taskToDelete) return;

      setTasks(tasks.filter(task => task.id !== id));

      await apiClient.deleteTask(id);
    } catch (err: any) {
      // If API fails, revert the optimistic update
      // Find the task that was being deleted to restore it
      const taskToRestore = tasks.find(task => task.id === id);
      if (taskToRestore) {
        setTasks([...tasks, taskToRestore]);
      }
      console.error('Error deleting task:', err);
    }
  };

  if (loading) {
    return <div className="text-center py-4">Loading tasks...</div>;
  }

  if (error) {
    return <div className="text-center py-4 text-destructive">{error}</div>;
  }

  if (tasks.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-[300px]">
        <div className="bg-card p-8 rounded-lg shadow-sm border border-gray-200 max-w-md w-full text-center">
          <p className="text-text-secondary">You don't have any tasks yet. Create your first task to get started!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-text-primary">Your Tasks</h2>
      <ul className="space-y-2">
        {tasks.map((task) => (
          <TaskItem
            key={task.id}
            task={task}
            onToggle={() => handleTaskToggle(task.id)}
            onDelete={() => handleTaskDelete(task.id)}
            onUpdate={(updatedTask) => {
              setTasks(tasks.map(t => t.id === updatedTask.id ? updatedTask : t));
            }}
          />
        ))}
      </ul>
    </div>
  );
});

export default TaskList;