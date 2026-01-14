'use client';

import { useState } from 'react';
import { apiClient } from '../../lib/api-client';

interface TaskFormProps {
  onTaskCreated?: () => void;
}

export default function TaskForm({ onTaskCreated }: TaskFormProps = {}) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Check if user is authenticated
    const token = localStorage.getItem('access_token');
    if (!token) {
      setError('You are not authenticated. Please log in to create tasks.');
      setLoading(false);
      return;
    }

    // Basic validation
    if (!title.trim()) {
      setError('Title is required');
      setLoading(false);
      return;
    }

    if (title.length > 200) {
      setError('Title must be 200 characters or less');
      setLoading(false);
      return;
    }

    if (description.length > 1000) {
      setError('Description must be 1000 characters or less');
      setLoading(false);
      return;
    }

    try {
      // Attempt to create the task
      const trimmedDescription = description.trim();
      await apiClient.createTask(title.trim(), trimmedDescription === '' ? undefined : trimmedDescription);

      // Reset form on success
      setTitle('');
      setDescription('');
      setError('');

      // Call the callback if provided
      if (onTaskCreated) {
        onTaskCreated();
      }
    } catch (err: any) {
      // Handle specific error messages
      if (err.message.includes('Authentication failed') || err.message.includes('log in')) {
        setError(err.message + ' Redirecting to login...');
        // Redirect to login page after a short delay
        setTimeout(() => {
          window.location.href = '/auth/login';
        }, 2000);
      } else {
        setError(err.message || 'An error occurred while creating the task');
      }
      console.error('Task creation error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-card p-6 rounded-lg shadow-sm border border-gray-200">
      <h2 className="text-xl font-semibold text-text-primary mb-4">Create New Task</h2>

      {error && (
        <div className="mb-4 bg-destructive/10 text-destructive p-3 rounded-md">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-text-primary mb-1">
            Title *
          </label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
            placeholder="Task title (1-200 characters)"
            maxLength={200}
          />
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-text-primary mb-1">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
            placeholder="Task description (optional, up to 1000 characters)"
            maxLength={1000}
            rows={3}
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-50"
        >
          {loading ? 'Creating Task...' : 'Create Task'}
        </button>
      </form>
    </div>
  );
}