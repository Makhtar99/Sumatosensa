
/** @type {import('tailwindcss').Config} */
import tailwindPlugin from 'tailwindcss-primeui';

export default {
 content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  plugins: [tailwindPlugin],
  darkMode: 'class',
};

