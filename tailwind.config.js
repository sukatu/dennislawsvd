/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  darkMode: 'class', // Enable dark mode with class strategy
  theme: {
    extend: {
          colors: {
            brand: {
              // Royal Blue - Primary brand color (#0808EF)
              50: '#f0f0ff',
              100: '#e0e1ff',
              200: '#c7c8ff',
              300: '#a5a7ff',
              400: '#8184ff',
              500: '#0808EF', // Primary Royal Blue
              600: '#0707d6',
              700: '#0606bd',
              800: '#0505a4',
              900: '#04048b',
              950: '#030372',
              DEFAULT: '#0808EF',
              dark: '#0606bd',
              light: '#8184ff'
            },
            accent: {
              // Teal - Secondary brand color (#5CDAB9)
              50: '#f0fdfa',
              100: '#ccfbf1',
              200: '#99f6e4',
              300: '#5CDAB9', // Primary Teal
              400: '#2dd4bf',
              500: '#14b8a6',
              600: '#0d9488',
              700: '#0f766e',
              800: '#115e59',
              900: '#134e4a',
              950: '#042f2e'
            },
            light: {
              // Light Blue - Tertiary brand color (#D5DFE7)
              50: '#f8fafc',
              100: '#f1f5f9',
              200: '#e2e8f0',
              300: '#D5DFE7', // Primary Light Blue
              400: '#94a3b8',
              500: '#64748b',
              600: '#475569',
              700: '#334155',
              800: '#1e293b',
              900: '#0f172a',
              950: '#020617'
            }
          },
      fontFamily: {
        'inter': ['Inter', 'ui-sans-serif', 'system-ui', '-apple-system', 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', 'Apple Color Emoji', 'Segoe UI Emoji']
      }
    },
  },
  plugins: [],
}
