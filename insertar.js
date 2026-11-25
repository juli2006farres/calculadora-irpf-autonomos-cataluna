// Página «Pon nuestras calculadoras en tu web»: cambia la vista previa y el código según la calculadora
// elegida, y copia el código. El código solo lleva un iframe y un enlace: nada se ejecuta en la otra web.
const idioma = document.documentElement.lang === "ca" ? "ca" : "es";
const TEXTOS = {
  es: { pie: (enlace, titulo) => `Calculadora: <a href="${enlace}">${titulo}</a>, de Calculadoras para autónomos.`, copiado: "Código copiado. Pégalo en tu web.", manual: "Selecciona el código y cópialo con Ctrl+C (o mantén pulsado en el móvil)." },
  ca: { pie: (enlace, titulo) => `Calculadora: <a href="${enlace}">${titulo}</a>, de Calculadores per a autònoms.`, copiado: "Codi copiat. Enganxa'l al teu web.", manual: "Selecciona el codi i copia'l amb Ctrl+C (o mantén premut al mòbil)." },
};
const t = TEXTOS[idioma];
const radios = [...document.querySelectorAll('input[name="widget"]')];
const codigo = document.getElementById("codigo");
const vista = document.getElementById("vista");
const aviso = document.getElementById("copiado");
// Ajusta la altura del iframe a lo que pide la calculadora (lo envía widget.js). Va en el código para copiar
// y también aquí, para la vista previa.
const ORIGEN = "https://juli2006farres.github.io";
const AJUSTE = `<script>addEventListener("message",function(e){var d=e.data;if(e.origin!=="${ORIGEN}"||!d||d.tipo!=="calculadora-autonomos-altura")return;document.querySelectorAll("iframe").forEach(function(f){if(f.contentWindow===e.source)f.style.height=Math.min(Math.max(+d.altura||0,300),6000)+"px"})})<\/script>`;
window.addEventListener("message", (e) => {
  const d = e.data;
  if (e.source !== vista.contentWindow || !d || d.tipo !== "calculadora-autonomos-altura") return;
  vista.style.height = `${Math.min(Math.max(Number(d.altura) || 0, 300), 6000)}px`;
});
const escapar = (texto) => texto.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

function actualizar() {
  const elegido = radios.find((r) => r.checked) ?? radios[0];
  const { src, vista: rutaVista, enlace, titulo, altura } = elegido.dataset;
  codigo.value = `<iframe src="${escapar(src)}" title="${escapar(titulo)}" width="100%" height="${Number(altura)}" style="border:0;width:100%;max-width:100%" loading="lazy"></iframe>\n<p style="font-size:14px">${t.pie(escapar(enlace), escapar(titulo))}</p>
${AJUSTE}`;
  if (vista.getAttribute("src") !== rutaVista) vista.setAttribute("src", rutaVista);
  vista.height = String(Number(altura));
  vista.title = titulo;
  aviso.textContent = "";
}

for (const r of radios) r.addEventListener("change", actualizar);
document.getElementById("copiar").addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(codigo.value);
    aviso.textContent = t.copiado;
  } catch {
    codigo.focus();
    codigo.select();
    aviso.textContent = t.manual;
  }
});
actualizar();
