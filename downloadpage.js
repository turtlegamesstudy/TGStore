// Función para mostrar el juego según el parámetro de la URL
function mostrarJuegoPorParametro() {
  const params = new URLSearchParams(window.location.search);
  const juego = params.get('juego');
  if (juego === 'metaedu' || juego === 'plasma') {
    document.getElementById('metaedu').classList.add('hidden');
    document.getElementById('plasma').classList.add('hidden');
    document.getElementById(juego).classList.remove('hidden');
  }
}

// Función para mostrar el juego al hacer clic en los botones
function mostrarJuego(juego) {
  document.getElementById('metaedu').classList.add('hidden');
  document.getElementById('plasma').classList.add('hidden');
  document.getElementById(juego).classList.remove('hidden');
}

// Ejecutar al cargar la página
window.addEventListener('DOMContentLoaded', mostrarJuegoPorParametro);
