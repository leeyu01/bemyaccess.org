'use client';

import { useBookmarks } from '@/components/BookmarkProvider';

interface BookmarkButtonProps {
  articleId: number;
  title: string;
}

export default function BookmarkButton({ articleId, title }: BookmarkButtonProps) {
  const { isBookmarked, toggleBookmark } = useBookmarks();
  const bookmarked = isBookmarked(articleId);

  return (
    <button
      onClick={() => toggleBookmark(articleId, title)}
      className={`bookmark-btn px-4 py-2 border rounded min-h-[44px] ${
        bookmarked
          ? 'bg-yellow-400 text-black border-yellow-400'
          : 'bg-transparent text-current border-current'
      }`}
      aria-pressed={bookmarked}
      aria-label={bookmarked ? `Remove "${title}" from bookmarks` : `Save "${title}" to bookmarks`}
    >
      {bookmarked ? '★ Saved' : '☆ Save'}
    </button>
  );
}
