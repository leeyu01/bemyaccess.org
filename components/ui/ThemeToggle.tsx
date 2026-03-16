/**
 * ThemeToggle - Switch between light, dark, and high-contrast modes
 */
'use client';

import { useTheme } from './ThemeProvider';

export default function ThemeToggle() {
  const { theme, setTheme } = useTheme();
  const themes = ['light', 'dark', 'high-contrast'] as const;

  return (
    <div className="theme-toggle" role="group" aria-label="Theme selection">
      {themes.map((t) => (
        <button
          key={t}
          onClick={() => setTheme(t)}
          aria-pressed={theme === t}
          className={`px-4 py-2 border ${
            theme === t ? 'bg-primary text-white' : 'bg-transparent'
          }`}
        >
          {t.charAt(0).toUpperCase() + t.slice(1).replace('-', ' ')}
        </button>
      ))}
    </div>
  );
}
