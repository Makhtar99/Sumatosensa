
/** @type {import('tailwindcss').Config} */
import tailwindPlugin from 'tailwindcss-primeui';

export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  plugins: [tailwindPlugin],
  darkMode: 'class',
  theme: {
    colors: {
      ivory: '#FAF8F4',
      coral: '#FF6B5E',
      anthracite: '#2E2E2E',
      comfort: '#62C370',
      alert: '#F25C54',
      neutral: '#58A4B0',
      avatar: '#FBE3C0',
    },
  },
};


