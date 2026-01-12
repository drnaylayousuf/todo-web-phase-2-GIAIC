'use client';

import RegisterForm from '@/components/auth/RegisterForm';

export default function RegisterPage() {
  // Add styles for animations
  const styles = `
    @keyframes fadeInDown {
      from {
        opacity: 0;
        transform: translateY(-20px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    @keyframes fadeInUp {
      from {
        opacity: 0;
        transform: translateY(20px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    @keyframes fadeIn {
      from {
        opacity: 0;
      }
      to {
        opacity: 1;
      }
    }
  `;

  return (
    <>
      <style>{styles}</style>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        * {
          font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        }
      `}</style>
    <div
      className="min-h-screen flex items-center justify-center bg-slate-900 p-4"
      style={{
        minHeight: '100vh',
        background: '#0a0f2c', /* Dark navy blue */
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '1rem',
        margin: 0,
        width: '100%',
        overflow: 'auto'
      }}
    >
      <div
        className="bg-white/15 backdrop-blur-xl rounded-3xl shadow-2xl p-10 w-full max-w-md"
        style={{
          background: 'rgba(255, 255, 255, 0.12)', /* More opaque translucent white */
          backdropFilter: 'blur(16px)',
          borderRadius: '2rem',
          boxShadow: '0 30px 60px -15px rgba(0, 0, 0, 0.4), inset 0 4px 8px rgba(255, 255, 255, 0.15)',
          padding: '2.5rem',
          width: '100%',
          maxWidth: '28rem', /* Wider for better spacing */
          margin: '0 auto',
          textAlign: 'center',
          border: '1px solid rgba(255, 255, 255, 0.2)',
          position: 'relative',
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center'
        }}
      >
        <div className="text-center mb-8" style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h1
            className="text-3xl font-bold text-white mb-2"
            style={{
              fontWeight: '700',
              fontSize: '1.875rem',
              color: '#ffffff',
              textAlign: 'center',
              marginBottom: '0.5rem',
              animation: 'fadeInDown 0.6s ease-out',
              letterSpacing: '0.025em',
              fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif"
            }}
          >
            Create Account
          </h1>
          <p
            className="text-gray-300"
            style={{
              color: '#d1d5db', /* Soft gray color */
              textAlign: 'center',
              fontSize: '0.875rem',
              animation: 'fadeInUp 0.6s ease-out 0.2s both',
              opacity: 0.9,
              fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif"
            }}
          >
            Sign up to manage your tasks
          </p>
        </div>

        <RegisterForm />
      </div>
    </div>
    </>
  );
}