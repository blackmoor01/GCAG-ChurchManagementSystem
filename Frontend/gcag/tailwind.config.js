/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
  colors: {
    purple: {
      DEFAULT: "#5D0676",
      light: "#F3E8FB",
      dark: "#45045A",
    },
    green: {
      DEFAULT: "#22C55E", // Tailwind's emerald-500
    },
    black: "#000000",
  },
};
