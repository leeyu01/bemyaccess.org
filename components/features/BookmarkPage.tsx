'use client';

import { useBookmarks } from '@/components/BookmarkProvider';
import Link from 'next/link';

export default function BookmarkPage() {
  const { bookmarks, toggleBookmark } = useBookmarks();

  if (bookmarks.length === 0) {
    return (
      <div className="bookmark-page">
        <h1>Saved Articles</h1>
        <p>You haven&apos;t saved any articles yet.</p>
      </div>
    );
  }

  return (
    <div className="bookmark-page">
      <h1>Saved Articles</h1>
      <p className="text-gray-600 dark:text-gray-400 mb-6">
        {bookmarks.length} article{bookmarks.length !== 1 ? 's' : ''} saved
      </p>

      <ul className="bookmark-list">
        {bookmarks.map((bookmark) => (
          <li key={bookmark.articleId} className="bookmark-item border rounded-lg p-4 mb-4">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="font-bold text-lg">{bookmark.title}</h3>
                <p className="text-sm text-gray-500">
                  Saved on {new Date(bookmark.savedAt).toLocaleDateString()}
                </p>
              </div>
              <button
                onClick={() => toggleBookmark(bookmark.articleId, bookmark.title)}
                className="px-4 py-2 border border-red-500 text-red-500 rounded min-h-[44px] hover:bg-red-50 dark:hover:bg-red-900"
                aria-label={`Remove "${bookmark.title}" from bookmarks`}
              >
                Remove
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
