import Link from 'next/link';

export default function HomePage() {
  return (
    <div style={{
      display: 'flex',
      minHeight: '100vh',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: '#0a0f2c', // dark navy blue background
      padding: '1rem'
    }}>
      <div style={{
        backgroundColor: 'white',
        borderRadius: '1rem',
        padding: '3rem',
        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)', // subtle shadow
        width: '100%',
        maxWidth: '32rem',
        textAlign: 'center'
      }}>
        <h1 style={{
          fontSize: '2.25rem',
          fontWeight: 'bold',
          color: '#0a0f2c', // dark navy blue color
          marginBottom: '1rem',
          textAlign: 'center'
        }}>
          Welcome to Task Manager
        </h1>

        <p style={{
          fontSize: '1.125rem',
          color: '#6b7280', // medium-dark gray color for contrast on dark background
          marginBottom: '2.5rem',
          textAlign: 'center'
        }}>
          A simple task management application with authentication
        </p>

        <div style={{
          display: 'flex',
          justifyContent: 'center',
          gap: '1rem',
          flexWrap: 'wrap'
        }}>
          <Link
            href="/auth/register"
            style={{
              backgroundColor: '#8b5cf6', // purple for Register button
              color: 'white',
              padding: '0.75rem 1.5rem',
              borderRadius: '0.5rem',
              fontWeight: '500',
              textDecoration: 'none',
              transition: 'all 0.2s ease-in-out',
              boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1)',
              display: 'inline-block'
            }}
            className="hover:bg-[#7c3aed] hover:scale-105 hover:shadow-lg transition-all duration-200"
          >
            Register
          </Link>

          <Link
            href="/auth/login"
            style={{
              backgroundColor: '#ec4899', // complementary pink color for Sign In button
              color: 'white',
              padding: '0.75rem 1.5rem',
              borderRadius: '0.5rem',
              fontWeight: '500',
              textDecoration: 'none',
              transition: 'all 0.2s ease-in-out',
              boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1)',
              display: 'inline-block'
            }}
            className="hover:bg-[#db2777] hover:scale-105 hover:shadow-lg transition-all duration-200"
          >
            Sign In
          </Link>
        </div>
      </div>
    </div>
  );
}
