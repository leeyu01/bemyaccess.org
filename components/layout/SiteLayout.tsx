'use client';

import Header from './Header';
import Footer from './Footer';
import WeatherWidget from '@/components/features/WeatherWidget';
import { useTheme } from '@/components/ui/ThemeProvider';

interface SiteLayoutProps {
  children: React.ReactNode;
  showWeather?: boolean;
}

export default function SiteLayout({ children, showWeather = true }: SiteLayoutProps) {
  const { theme } = useTheme();

  return (
    <div className={`site-layout theme-${theme}`}>
      <Header />
      <main id="main-content" role="main" tabIndex={-1}>
        {showWeather && (
          <div className="container mx-auto px-4 py-4 max-w-4xl">
            <WeatherWidget />
          </div>
        )}
        <div className="container mx-auto px-4 py-4 max-w-4xl">
          {children}
        </div>
      </main>
      <Footer />
    </div>
  );
}
