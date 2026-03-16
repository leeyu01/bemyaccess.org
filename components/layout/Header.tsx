'use client';

import Link from 'next/link';
import ThemeToggle from '@/components/ui/ThemeToggle';

export default function Header() {
  return (
    <header className="site-header">
      <nav className="nav-container" aria-label="Main navigation">
        <Link href="/" className="nav-brand">
          <span className="logo" aria-hidden="true">B</span>
          <span>Be My Access</span>
        </Link>

        <div className="nav-actions">
          <ThemeToggle />
        </div>
      </nav>
    </header>
  );
}
