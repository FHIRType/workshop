/** @type {import('tailwindcss').Config} */
const {nextui} = require("@nextui-org/react");

export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
        "./node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            fontFamily: {
                roboto: ['Roboto', 'sans-serif'],
            },
            colors: {
                "pacific-blue": "#21578A",
                "pacific-light-blue": "#6892BB",
                "pacific-blue-9": "#134673",
                "pacific-gray": "#D9D9D9",
                "pacific-light-gray": "#F6F6F6"
            }
        },
    },
    darkMode: "class",
    plugins: [
        nextui()
    ],
}