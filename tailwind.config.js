/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './node_modules/flowbite/**/*.js'
  ],
  theme: {
    fontFamily: {
      'sans': ['Inter var','ui-sans-serif','system-ui','BlinkMacSystemFont','Segoe UI','Roboto','Helvetica Neue','Arial','Noto Sans','sans-serif','Apple Color Emoji','Segoe UI Emoji','Segoe UI Symbol','Noto Color Emoji'],
    },
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')
  ]
}
