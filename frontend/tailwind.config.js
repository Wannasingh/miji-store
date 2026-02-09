/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#111318",
        "background-dark": "#0a0a0a",
      },
    },
  },
  plugins: [],
}
