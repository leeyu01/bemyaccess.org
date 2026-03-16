/**
 * SkipLink - Accessibility skip to main content link
 */
'use client';

export default function SkipLink() {
  return (
    <a
      href="#main-content"
      className="skip-link"
      onClick={(e) => {
        e.preventDefault();
        document.getElementById('main-content')?.focus();
      }}
    >
      Skip to main content
    </a>
  );
}
