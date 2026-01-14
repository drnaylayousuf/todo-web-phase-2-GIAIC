'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { AuthCredentials } from '../../lib/types';
import { apiClient } from '../../lib/api-client';

interface RegisterFormProps {
  onRegister?: (credentials: AuthCredentials) => void;
}

export default function RegisterForm({ onRegister }: RegisterFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    if (!email || !password) {
      setError('Email and password are required');
      setLoading(false);
      return;
    }

    try {
      await apiClient.register(email, password);

      // Registration successful, call the callback or redirect
      if (onRegister) {
        onRegister({ email, password });
      } else {
        // Default behavior: redirect to login
        router.push('/auth/login');
      }
    } catch (err: any) {
      setError(err.message || 'An error occurred during registration');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-8">
      {error && (
        <div className="bg-red-100 text-red-700 p-3 rounded-lg border border-red-200">
          {error}
        </div>
      )}

      <div className="flex flex-col space-y-5">
        <label htmlFor="email" className="text-sm font-medium text-white self-start" style={{ fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif", color: 'white !important' }}>
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="w-full px-8 py-5 border border-gray-600 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200 text-lg bg-white/90 text-gray-900"
          placeholder="you@example.com"
          style={{ fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif" }}
        />
      </div>

      <div className="flex flex-col space-y-5">
        <label htmlFor="password" className="text-sm font-medium text-white self-start" style={{ fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif", color: 'white !important' }}>
          Password
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          minLength={8}
          className="w-full px-8 py-5 border border-gray-600 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200 text-lg bg-white/90 text-gray-900"
          placeholder="At least 8 characters"
          style={{ fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif" }}
        />
      </div>

      <div className="flex flex-col space-y-5">
        <label htmlFor="confirmPassword" className="text-sm font-medium text-white self-start" style={{ fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif", color: 'white !important' }}>
          Confirm Password
        </label>
        <input
          id="confirmPassword"
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
          className="w-full px-8 py-5 border border-gray-600 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200 text-lg bg-white/90 text-gray-900"
          placeholder="Confirm your password"
          style={{ fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif" }}
        />
      </div>

      <div className="mt-2">
        <button
          type="submit"
          disabled={loading}
          className="w-full py-6 px-4 text-xl font-bold text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 rounded-full transition-all duration-300 shadow-lg hover:shadow-2xl transform hover:scale-105 active:scale-95"
          style={{ fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif" }}
        >
          {loading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Creating Account...
            </span>
          ) : (
            'Register'
          )}
        </button>
      </div>

      <div className="text-center text-sm text-white mt-6" style={{ fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif", color: 'white !important' }}>
        Already have an account?{' '}
        <a href="/auth/login" className="font-medium text-blue-400 hover:text-blue-300 hover:underline transition-colors duration-200">
          Sign In
        </a>
      </div>
    </form>
  );
}