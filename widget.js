// Calculadoras insertadas en otras webs: avisa a la página que las contiene de la altura que necesitan,
// para que el iframe crezca o encoja sin barra de desplazamiento. Solo envía un número.
const contenido = document.querySelector("main");
function enviar() {
  if (window.parent === window) return;
  window.parent.postMessage({ tipo: "calculadora-autonomos-altura", altura: Math.ceil(contenido.getBoundingClientRect().height) + 4 }, "*");
}
new ResizeObserver(enviar).observe(contenido);
window.addEventListener("load", enviar);
enviar();
