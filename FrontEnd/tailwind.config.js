/** @type {import('tailwindcss').Config} */
const { nextui } = require('@nextui-org/react');

export default {
    content: [
        './index.html',
        './src/**/*.{js,ts,jsx,tsx}',
        './node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}',
    ],
    theme: {
        extend: {
            fontFamily: {
                roboto: ['Roboto', 'sans-serif'],
            },
            colors: {
                'pacific-blue': '#21578A',
                'pacific-light-blue': '#6892BB',
                'pacific-blue-9': '#134673',
                'pacific-gray': '#D9D9D9',
                'pacific-light-gray': '#F6F6F6',
            },
            backgroundImage: {
                family: "url('/src/assets/family.jpg')",
            },
            boxShadow: {
                mobile: '0 20px 25px -5px rgb(255 255 255 / 0.1), 0 8px 10px -6px rgb(255 255 255 / 0.1)',
            },
            flex: {
                half: '0 0 35%',
            },
        },
    },
    darkMode: 'class',
    plugins: [nextui()],
};
