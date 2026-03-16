'use client';

import { createContext, useContext, useState, ReactNode, useEffect } from 'react';

interface Bookmark {
  articleId: number;
  title: string;
  savedAt: string;
}

interface BookmarkContextType {
  bookmarks: Bookmark[];
  toggleBookmark: (articleId: number, title: string) => void;
  isBookmarked: (articleId: number) => boolean;
}

const BookmarkContext = createContext<BookmarkContextType | undefined>(undefined);

const BOOKMARKS_COOKIE_NAME = 'bemyaccess_bookmarks';

export function BookmarkProvider({ children }: { children: ReactNode }) {
  const [bookmarks, setBookmarks] = useState<Bookmark[]>([]);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    // Load bookmarks from cookies on mount
    const cookieBookmarks = getBookmarksFromCookie();
    setBookmarks(cookieBookmarks);
    setMounted(true);
  }, []);

  useEffect(() => {
    // Save bookmarks to cookie whenever they change
    if (mounted) {
      setBookmarksCookie(bookmarks);
    }
  }, [bookmarks, mounted]);

  const getBookmarksFromCookie = (): Bookmark[] => {
    if (typeof document === 'undefined') return [];

    const cookie = document.cookie
      .split('; ')
      .find(row => row.startsWith(BOOKMARKS_COOKIE_NAME + '='));

    if (!cookie) return [];

    try {
      const value = decodeURIComponent(cookie.split('=')[1]);
      return JSON.parse(value);
    } catch {
      return [];
    }
  };

  const setBookmarksCookie = (bookmarks: Bookmark[]) => {
    if (typeof document === 'undefined') return;

    const value = encodeURIComponent(JSON.stringify(bookmarks));
    const expires = new Date();
    expires.setFullYear(expires.getFullYear() + 1); // 1 year expiry

    document.cookie = `${BOOKMARKS_COOKIE_NAME}=${value}; expires=${expires.toUTCString()}; path=/`;
  };

  const toggleBookmark = (articleId: number, title: string) => {
    setBookmarks(prev => {
      const exists = prev.find(b => b.articleId === articleId);
      if (exists) {
        return prev.filter(b => b.articleId !== articleId);
      } else {
        return [...prev, {
          articleId,
          title,
          savedAt: new Date().toISOString(),
        }];
      }
    });
  };

  const isBookmarked = (articleId: number): boolean => {
    return bookmarks.some(b => b.articleId === articleId);
  };

  return (
    <BookmarkContext.Provider value={{ bookmarks, toggleBookmark, isBookmarked }}>
      {children}
    </BookmarkContext.Provider>
  );
}

export function useBookmarks() {
  const context = useContext(BookmarkContext);
  if (!context) {
    throw new Error('useBookmarks must be used within a BookmarkProvider');
  }
  return context;
}
