import type { ReactNode } from 'react';
import './globals.css';

export const metadata = {
  title: 'Task Manager',
  description: 'A simple task management application with authentication',
};

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-background min-h-screen">
        <div className="container mx-auto">
          {children}
        </div>
      </body>
    </html>
  );
}