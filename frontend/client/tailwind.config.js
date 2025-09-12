/**** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        casino: {
          red: "#E30613",
          green: "#009739",
          gray: "#4D4D4D",
          white: "#FFFFFF",
        },
      },
    },
  },
  plugins: [],
};
