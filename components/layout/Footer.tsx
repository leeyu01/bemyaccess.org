export default function Footer() {
  return (
    <footer className="site-footer" role="contentinfo">
      <div className="container mx-auto px-4 py-8 max-w-4xl text-center">
        <p className="text-gray-600 dark:text-gray-400">
          {new Date().getFullYear()} Be My Access. Serving Suffolk County, NY.
        </p>
        <p className="text-sm mt-2">
          Accessible news for the visually impaired community.
        </p>
      </div>
    </footer>
  );
}
