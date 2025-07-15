module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx}',
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        background: '#F8F9FA',
        primary: '#7C83FD',
        secondary: '#A3B18A',
        surface: '#FFFFFF',
        text: '#22223B',
        border: '#E0E1DD',
        error: '#FF6F61',
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui'],
      },
    },
  },
  plugins: [],
}