
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
      ivory: '#FAF8F4', // ivoire
      coral: '#FF6B5E', // corail
      anthracite: '#2E2E2E', // writing
      comfort: '#62C370', // green
      alert: '#F25C54', // red
      neutral: '#58A4B0', // blue
      light_orange: "#F9E0BD", // avatar
      background: '#FFF2D6', // background
      orange: "E25B2A", // orange
    },
  },
};



