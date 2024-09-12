/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        abel: ['Abel', 'sans-serif'],  // Add Abel to your font family options
      },
    },
  },
  plugins: [],
}
