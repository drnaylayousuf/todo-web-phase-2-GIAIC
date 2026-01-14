'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { AuthCredentials, TokenResponse } from '../../lib/types';
import { apiClient } from '../../lib/api-client';

interface LoginFormProps {
  onLogin?: (token: string) => void;
}

export default function LoginForm({ onLogin }: LoginFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const data = await apiClient.login(email, password);

      // Login successful, store token and call callback or redirect
      const tokenData: TokenResponse = data;
      localStorage.setItem('access_token', tokenData.access_token);

      if (onLogin) {
        onLogin(tokenData.access_token);
      } else {
        // Default behavior: redirect to dashboard
        router.push('/dashboard');
      }
    } catch (err: any) {
      setError(err.message || 'Invalid email or password');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-16">
      {error && (
        <div className="bg-red-100 text-red-700 p-4 rounded-xl border border-red-200">
          {error}
        </div>
      )}

      <div className="flex flex-col space-y-10">
        <label htmlFor="email" className="block text-base font-semibold text-white self-start" style={{ color: 'white !important' }}>
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="w-full px-8 py-6 border-2 border-gray-500 rounded-2xl focus:outline-none focus:ring-4 focus:ring-blue-500/40 focus:border-blue-400 transition-all duration-300 text-lg bg-white/95 text-gray-900 shadow-lg"
          placeholder="you@example.com"
          style={{ fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif" }}
        />
      </div>

      <div className="flex flex-col space-y-10">
        <label htmlFor="password" className="block text-base font-semibold text-white self-start" style={{ color: 'white !important' }}>
          Password
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="w-full px-8 py-6 border-2 border-gray-500 rounded-2xl focus:outline-none focus:ring-4 focus:ring-blue-500/40 focus:border-blue-400 transition-all duration-300 text-lg bg-white/95 text-gray-900 shadow-lg"
          placeholder="Your password"
          style={{ fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif" }}
        />
      </div>

      <div className="mt-4">
        <button
          type="submit"
          disabled={loading}
          className="w-full py-5 px-4 text-xl font-bold text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 rounded-full transition-all duration-300 shadow-lg hover:shadow-2xl transform hover:scale-105 active:scale-95"
          style={{ fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif" }}
        >
          {loading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Signing In...
            </span>
          ) : (
            'Sign In'
          )}
        </button>
      </div>
    </form>
  );
}