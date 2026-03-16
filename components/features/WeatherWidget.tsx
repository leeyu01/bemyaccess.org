'use client';

import { useState, useEffect } from 'react';

interface WeatherData {
  temperature: number;
  description: string;
  humidity: number;
  windSpeed: number;
}

export default function WeatherWidget() {
  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchWeather();
  }, []);

  const fetchWeather = async () => {
    setLoading(true);
    setError(null);

    try {
      // Using Open-Meteo API (free, no key required)
      const lat = 40.7891; // Suffolk County, NY
      const lon = -73.1350;

      const res = await fetch(
        `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m&temperature_unit=fahrenheit`
      );

      if (!res.ok) {
        throw new Error('Weather API request failed');
      }

      const data = await res.json();

      setWeather({
        temperature: Math.round(data.current.temperature_2m),
        description: getWeatherDescription(data.current.temperature_2m),
        humidity: data.current.relative_humidity_2m,
        windSpeed: data.current.wind_speed_10m,
      });
    } catch (err) {
      setError('Unable to load weather');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getWeatherDescription = (temp: number): string => {
    if (temp > 80) return 'Sunny';
    if (temp > 70) return 'Clear';
    if (temp > 60) return 'Partly Cloudy';
    if (temp > 50) return 'Cloudy';
    if (temp > 40) return 'Overcast';
    return 'Cold';
  };

  if (loading) {
    return (
      <div className="weather-widget bg-surface border border-border rounded-lg p-4">
        <p>Loading weather...</p>
      </div>
    );
  }

  if (error || !weather) {
    return (
      <div className="weather-widget bg-surface border border-border rounded-lg p-4">
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  return (
    <div className="weather-widget bg-surface border border-border rounded-lg p-4 flex items-center gap-4 flex-wrap">
      <div className="weather-icon" aria-hidden="true">
        {getWeatherEmoji(weather.description)}
      </div>
      <div className="weather-main flex-1 min-w-[160px]">
        <div className="weather-loc text-sm font-semibold uppercase tracking-wide">
          Suffolk County, NY
        </div>
        <div className="weather-temp text-2xl font-bold">
          {weather.temperature}°F
        </div>
        <div className="weather-desc text-sm">{weather.description}</div>
      </div>
      <div className="weather-details flex gap-4 flex-wrap">
        <div className="weather-detail">
          <strong>Humidity</strong>
          <span>{weather.humidity}%</span>
        </div>
        <div className="weather-detail">
          <strong>Wind</strong>
          <span>{weather.windSpeed} mph</span>
        </div>
      </div>
    </div>
  );
};

function getWeatherEmoji(description: string): string {
  const emojiMap: Record<string, string> = {
    'Sunny': '☀️',
    'Clear': '🌞',
    'Partly Cloudy': '⛅',
    'Cloudy': '☁️',
    'Overcast': '☁️',
    'Rain': '🌧️',
    'Snow': '❄️',
    'Storm': '⛈️',
    'Cold': '🥶',
  };
  return emojiMap[description] || '🌤️';
}
