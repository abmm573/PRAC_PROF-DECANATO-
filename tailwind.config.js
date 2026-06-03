/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Paleta profesional de la carrera
        'azul-marino': '#0F172A',   // Para headers, botones principales y footers
        'azul-primario': '#1D4ED8', // Para botones de acción, enlaces y estados activos
        'azul-claro': '#DBEAFE',    // Para fondos de tarjetas (cards) o alertas suaves
        'gris-fondo': '#F8FAFC',    // Fondo general limpio y minimalista
        'gris-texto': '#475569',    // Texto secundario, descripciones legibles
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'], // Tipografía moderna y limpia
      }
    },
  },
  plugins: [],
}