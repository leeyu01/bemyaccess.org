import { Suspense } from "react";

export default function Home() {
  return (
    <div className="min-h-screen">
      <header>
        <h1>Be My Access</h1>
        <p>Accessible News for Suffolk County</p>
      </header>

      <nav aria-label="Category navigation">
        <ul>
          <li><a href="/articles?category=1">Local News</a></li>
          <li><a href="/articles?category=2">News for the Disabled</a></li>
          <li><a href="/articles?category=3">Weather</a></li>
        </ul>
      </nav>

      <main>
        <h2>Latest Articles</h2>
        {/* Article list will go here */}
      </main>
    </div>
  );
}
