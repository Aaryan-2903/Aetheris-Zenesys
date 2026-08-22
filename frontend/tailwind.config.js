/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#f9f9fb',
        card: '#ffffff',
        navy: '#00174b',
        primary: '#0066cc',
        text: '#1a1c1d',
        muted: '#727784',
        border: '#e5e5ea',
        red: '#ff3b30',
        redbg: '#fff0f0',
        green: '#17803d',
        greenbg: '#effaf2',
        warning: '#9a6700',
        warningbg: '#fff4df'
      },
      fontFamily: {
        sans: ['"Hanken Grotesk"', 'sans-serif'],
      },
      boxShadow: {
        card: '0 4px 24px rgba(0,0,0,0.04)',
        modal: '0 25px 80px rgba(0,0,0,0.2)',
        toast: '0 10px 35px rgba(0,0,0,0.2)'
      }
    },
  },
  plugins: [],
}
