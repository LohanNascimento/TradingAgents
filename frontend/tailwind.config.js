/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        'discord-dark': '#36393f',
        'discord-darker': '#2f3136',
        'discord-light': '#40444b',
        'discord-blue': '#5865f2',
        'discord-green': '#57f287',
        'discord-red': '#ed4245',
        'discord-yellow': '#fee75c',
        'discord-text': '#dcddde',
        'discord-text-muted': '#72767d',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce-slow': 'bounce 2s infinite',
        'typing': 'typing 2s infinite',
      },
      keyframes: {
        typing: {
          '0%, 100%': { opacity: 1 },
          '50%': { opacity: 0.5 },
        }
      }
    },
  },
  plugins: [],
}