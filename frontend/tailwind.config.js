/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#2563EB',      // Calm, professional blue
        secondary: '#14B8A6',    // Soft teal
        destructive: '#EF4444',  // Vivid red for errors
        success: '#22C55E',      // Vibrant green for success
        background: '#F9FAFB',   // Soft off-white
        card: '#FFFFFF',         // Pure white
        navy: {
          900: '#0a192f',        // Dark navy blue
          800: '#112240',        // Slightly lighter navy
          700: '#172a45',        // Lighter navy
        },
        // Define text colors at the root level to match expected classes
        "text-primary": '#111827',    // Dark text
        "text-secondary": '#6B7280',  // Secondary text
        "text-disabled": '#9CA3AF',   // Disabled text
        // Keep nested text object for consistency
        text: {
          primary: '#111827',    // Dark text
          secondary: '#6B7280',  // Secondary text
          disabled: '#9CA3AF'    // Disabled text
        }
      },
      container: {
        center: true,
        padding: {
          DEFAULT: "1rem",
          sm: "2rem",
          lg: "4rem",
          xl: "5rem",
          "2xl": "6rem",
        },
      },
      keyframes: {
        'pulse-slow': {
          '0%, 100%': { opacity: 1 },
          '50%': { opacity: 0.7 },
        },
      },
      animation: {
        'pulse-slow': 'pulse-slow 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
    },
  },
  plugins: [],
}

