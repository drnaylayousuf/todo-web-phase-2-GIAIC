'use client';

import { useState } from 'react';
import { Task } from '@/lib/types';

interface TaskActionsProps {
  task: Task;
  onToggle: () => void;
  onDelete: () => void;
  onEdit: () => void;
}

export default function TaskActions({ task, onToggle, onDelete, onEdit }: TaskActionsProps) {
  const [isConfirmingDelete, setIsConfirmingDelete] = useState(false);

  const handleDeleteClick = () => {
    setIsConfirmingDelete(true);
  };

  const handleConfirmDelete = () => {
    onDelete();
    setIsConfirmingDelete(false);
  };

  const handleCancelDelete = () => {
    setIsConfirmingDelete(false);
  };

  return (
    <div className="flex space-x-2">
      {!isConfirmingDelete ? (
        <>
          <button
            onClick={onEdit}
            className="text-sm bg-secondary text-white px-2 py-1 rounded hover:bg-teal-700"
          >
            Edit
          </button>
          <button
            onClick={handleDeleteClick}
            className="text-sm bg-destructive text-white px-2 py-1 rounded hover:bg-red-700"
          >
            Delete
          </button>
        </>
      ) : (
        <div className="flex space-x-2">
          <button
            onClick={handleConfirmDelete}
            className="text-sm bg-destructive text-white px-2 py-1 rounded hover:bg-red-700"
          >
            Confirm
          </button>
          <button
            onClick={handleCancelDelete}
            className="text-sm bg-secondary text-white px-2 py-1 rounded hover:bg-teal-700"
          >
            Cancel
          </button>
        </div>
      )}
    </div>
  );
}