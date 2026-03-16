import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Link from "next/link";
import "./globals.css";
import { ThemeProvider } from "@/components/ui/ThemeProvider";
import SkipLink from "@/components/ui/SkipLink";
import SiteLayout from "@/components/layout/SiteLayout";
import { BookmarkProvider } from "@/components/BookmarkProvider";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: "Be My Access - Accessible News for Suffolk County",
  description: "Accessible news portal for visually impaired community in Suffolk County, NY",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.variable} font-sans`}>
        <SkipLink />
        <ThemeProvider>
          <BookmarkProvider>
            {/* Simple navigation - replace with proper component */}
            <nav
              className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700"
              role="navigation"
              aria-label="Main navigation"
            >
              <div className="container mx-auto px-4 py-4 max-w-4xl flex justify-between items-center">
                <a
                  href="/"
                  className="text-xl font-bold text-blue-600 dark:text-blue-400 hover:underline"
                >
                  Be My Access
                </a>
                <div className="flex gap-4">
                  <Link
                    href="/"
                    className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded min-h-[44px] hover:bg-gray-50 dark:hover:bg-gray-800"
                  >
                    Home
                  </Link>
                  <Link
                    href="/bookmarks"
                    className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded min-h-[44px] hover:bg-gray-50 dark:hover:bg-gray-800"
                  >
                    Bookmarks
                  </Link>
                </div>
              </div>
            </nav>

            <SiteLayout>{children}</SiteLayout>
          </BookmarkProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
