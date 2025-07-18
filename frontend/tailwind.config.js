
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
    extend: {
      colors: {
        'sumato-ivory': '#FAF8F4', // ivoire
        'sumato-coral': '#FF6B5E', // corail
        'sumato-anthracite': '#2E2E2E', // writing
        'sumato-comfort': '#62C370', // green
        'sumato-alert': '#F25C54', // red
        'sumato-neutral': '#58A4B0', // blue
        'sumato-light-orange': '#F9E0BD', // avatar
        'sumato-background': '#FFF2D6', // background
        'sumato-orange': '#E25B2A', // orange
        'sumato-orange-hover': '#F07A4D', // orange hover
      },
    },
  },
};

