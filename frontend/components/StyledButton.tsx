'use client';

import Link from 'next/link';
import { ReactNode } from 'react';

interface StyledButtonProps {
  href: string;
  children: ReactNode;
  style?: React.CSSProperties;
  className?: string;
}

export default function StyledButton({ href, children, style, className }: StyledButtonProps) {
  return (
    <Link
      href={href}
      style={style}
      className={className}
    >
      {children}
    </Link>
  );
}