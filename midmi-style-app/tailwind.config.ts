import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './pages/**/*.mdx',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Rose Tone Colors based on knowledge base
        'rose-light': '#F4ACB7', // Lightest tone
        'rose-medium': '#E07A5F', // Main accent tone (from sessions/2026-05-01T17-15/designer.md)
        'rose-dark': '#C95B43',   // Darker shade for contrast
        'glass-bg': 'rgba(255, 255, 255, 0.1)', // Glassmorphism background base
      },
      fontFamily: {
        // Serif typography based on knowledge base
        'serif-custom': ['Georgia', 'serif'],
      },
    },
  },
};

export default config;