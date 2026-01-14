'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import TaskList, { TaskListRef } from '@/components/tasks/TaskList';
import TaskForm from '@/components/tasks/TaskForm';

export default function DashboardPage() {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const taskListRef = useRef<TaskListRef>(null);
  const router = useRouter();

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('access_token');
    if (!token) {
      router.push('/auth/login');
      return;
    }

    // In a real app, you might fetch user details here
    // For now, we'll just check if the token exists
    // We could also verify the token by making an API call
    setUser({ email: 'user@example.com' }); // Placeholder
    setLoading(false);
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    router.push('/auth/login');
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#e6f3ff', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', width: '100%', minHeight: '100vh', overflowX: 'hidden' }}>
      <div style={{ width: '100%', display: 'flex', justifyContent: 'center' }}>
        <header className="shadow-md transition-all duration-300 hover:shadow-lg" style={{ backgroundColor: '#e6f3ff', textAlign: 'center', width: 'fit-content', minWidth: '600px' }}>
          <div className="px-4 py-6 flex flex-col items-center space-y-4">
            <h1
              className="text-3xl font-bold text-white text-center px-6 py-3 rounded-lg transition-all duration-500 hover:scale-105 hover:shadow-xl hover:text-white animate-fade-in"
              style={{ backgroundColor: '#1e90ff', border: '2px solid #1e90ff', margin: '0 auto', display: 'inline-block', color: 'black !important' }}
            >
              Task Dashboard
            </h1>
            <div className="flex items-center space-x-4">
              <span style={{ color: 'pink !important', display: 'inline-block', fontWeight: 'bold', border: '2px solid #1e90ff', borderRadius: '4px', padding: '4px 8px' }}>{user?.email}</span>
              <button
                onClick={handleLogout}
                className="text-sm bg-destructive text-white px-3 py-1 rounded hover:bg-red-700 transition-colors"
                style={{ color: 'white !important' }}
              >
                Logout
              </button>
            </div>
          </div>
        </header>
      </div>

      <main className="w-full flex flex-col items-center justify-center px-4 py-8" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', width: '100%', maxWidth: '600px', margin: '0 auto' }}>
        <div className="w-full" style={{ backgroundColor: '#e6f3ff', borderRadius: '12px', boxShadow: '0 10px 25px rgba(0,0,0,0.2)', width: '100%', padding: '24px', marginBottom: '32px' }}>
          <div style={{ color: '#0a192f' }}>
            <TaskForm onTaskCreated={() => {
              // Refetch tasks to show the newly created task
              taskListRef.current?.refetch();
            }} />
          </div>
        </div>

        <div className="w-full" style={{ backgroundColor: '#e6f3ff', borderRadius: '12px', boxShadow: '0 10px 25px rgba(0,0,0,0.2)', width: '100%', padding: '24px' }}>
          <div style={{ color: '#0a192f' }}>
            <TaskList ref={taskListRef} />
          </div>
        </div>
      </main>
    </div>
  );
}