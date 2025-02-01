// tailwind.config.js
module.exports = {
  content: [
    "./public/*.html", // Include all HTML files in the public directory
    "./src/**/*.{js,jsx,ts,tsx}", // Include all JS/TS files in the src directory
  ],
  theme: {
    extend: {
      // Extend the default Tailwind theme here
      colors: {
        'noir-black': '#0A0A0A',
        'neon-blue': '#00FFFF',
        'neon-pink': '#FF00FF',
        'vintage-brown': '#8B4513',
      },
      fontFamily: {
        'sans': ['"Times New Roman"', 'serif'], // 1930s-style serif font
        'mono': ['"Courier New"', 'monospace'], // Typewriter-style font
      },
      backgroundImage: {
        'noir-street': "url('/path/to/your/noir-street-image.jpg')", // Add custom background images
      },
    },
  },
  plugins: [],
}