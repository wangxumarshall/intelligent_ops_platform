// frontend/tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./public/index.html", // Scan the main HTML shell in public
    "./src/**/*.{vue,js,ts,jsx,tsx}" // Scan all Vue components and JS/TS files in src
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'], // Set Inter as default sans-serif
      },
    },
  },
  plugins: [],
}
