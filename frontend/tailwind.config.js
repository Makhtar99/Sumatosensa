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
      'black':{
          100: '#000',
          200: '#0f172a',
        },
      'custom-blue': {
        300: '#D8E4F2',
        400: '#62AAF9',
        500: '#0064E3',
        600: '#062193',
        700: '#0B104F',
        900: '#0B104E'
      },
      'custom-yellow': {
        300: '#FFEAB4',
        400: '#FEEB89',
        500: '#FFDC48',
        600: '#FFBF52',
        700: '#FC9C10'
      },
      'custom-green': {
        300: '#D7FFEE',
        400: '#B1FFE1',
        500: '#7fffd4',
        600: '#47B38F',
        700: '#40806A',
        900: '#2f5e4e',
      },
      'custom-orange': {
        100: '#f5d8a3',
        200: '#f7c76e',
        300: '#ffb733',
        400: '#ffa500',
        600: '#cc8400',
        700: '#996300',
        800: '#664200',
        900: '#332100'
      },
      'custom-red': {
        300: '#DC3318',
        400: '#f87171',
        500: '#DC3318',
        600: '#B62C16',
        700: '#982B1B',
        900: '#7a1e12'
      },
      'custom-pink': {
        300: '#FFE1EE',
        400: '#E274A1',
        500: '#ED3B8C',
        600: '#B51556',
        700: '#8C1F4C'
      },
      'custom-purple': {
        100: '#e831e8',
        200: '#da0cda',
        300: '#b300b3',
        400: '#800080',
        600: '#4d004d',
        700: '#1a001a',
        800: '#000000',
        900: '#000000'
      },
      'custom-gray': {
        200: '#f8f9fc',
        300: '#edf1f8',
        400: '#bfc9d6',
        500: '#8487A6',
        600: '#4b5158',
        700: '#0a131f'
      },
    },
    extend: {
      colors: {
        'custom-sumatosensa-background': '#F5F0E0',
        'custom-sumatosensa-red': '#EB4636',
        'custom-sumatosensa-black': '#162426',

      },
    },
  },
};
