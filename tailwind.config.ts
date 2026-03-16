module.exports = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // From the UI spec in 2-second-meeting.md
        primary: {
          DEFAULT: '#0057B8',
          dark: '#4FA3FF',
        },
        accent: {
          DEFAULT: '#FF6B00',
        },
      },
      fontSize: {
        'base': '18px', // Minimum 18px per spec
      },
      lineHeight: {
        'relaxed': '1.6', // Minimum 1.6 per spec
      },
    },
  },
  plugins: [],
}
