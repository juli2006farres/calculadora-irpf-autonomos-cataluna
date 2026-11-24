// Botones para compartir, copiar el enlace o imprimir el resultado de una calculadora.
// Los datos viajan en la parte del enlace que va después de «#»: el navegador no la envía a
// ningún servidor y esta web no la guarda. Al abrir un enlace así, el formulario se rellena solo.
const idioma = document.documentElement.lang === "ca" ? "ca" : "es";
const TEXTOS = {
  es: {
    titulo: "Guarda o comparte este cálculo",
    compartir: "Compartir",
    copiar: "Copiar enlace",
    copiado: "Enlace copiado. Pégalo donde quieras.",
    manual: "Copia este enlace:",
    imprimir: "Imprimir o guardar en PDF",
    nota: "El enlace lleva los datos que has escrito, para que quien lo abra vea el mismo cálculo. Esta web no los guarda.",
    impreso: (fecha, url) => `Calculado el ${fecha} en ${url}`,
    locale: "es-ES",
  },
  ca: {
    titulo: "Desa o comparteix aquest càlcul",
    compartir: "Comparteix",
    copiar: "Copia l'enllaç",
    copiado: "Enllaç copiat. Enganxa'l on vulguis.",
    manual: "Copia aquest enllaç:",
    imprimir: "Imprimeix o desa en PDF",
    nota: "L'enllaç porta les dades que has escrit, perquè qui l'obri vegi el mateix càlcul. Aquest web no les desa.",
    impreso: (fecha, url) => `Calculat el ${fecha} a ${url}`,
    locale: "ca-ES",
  },
};
const t = TEXTOS[idioma];
// Marca de versión del enlace: así un ancla normal (#algo) nunca cambia el formulario.
const VERSION = "1";
const NUMERO = /^\d{1,10}(\.\d{1,4})?$/;
const ICONOS = {
  compartir: '<path d="M12 3v12M7 8l5-5 5 5"/><path d="M5 13v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6"/>',
  copiar: '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
  imprimir: '<path d="M7 9V3h10v6"/><rect x="3" y="9" width="18" height="8" rx="2"/><path d="M7 14h10v7H7z"/>',
};

const formulario = document.getElementById("formulario");
const caja = document.querySelector("section.resultado");

function campos() {
  return [...formulario.elements].filter((e) => e.name && !e.disabled && (e.tagName === "INPUT" || e.tagName === "SELECT"));
}

// Todos los campos, también los vacíos, para que el enlace reproduzca exactamente lo escrito.
function enlace() {
  const datos = new URLSearchParams({ v: VERSION });
  for (const e of campos()) {
    if (e.type === "radio") {
      if (e.checked) datos.set(e.name, e.value);
    } else if (e.type === "checkbox") {
      datos.set(e.name, e.checked ? "1" : "0");
    } else {
      datos.set(e.name, e.value.trim());
    }
  }
  return `${location.origin}${location.pathname}#${datos.toString()}`;
}

function restaurar() {
  if (location.hash.length < 2) return;
  const datos = new URLSearchParams(location.hash.slice(1));
  if (datos.get("v") !== VERSION) return;
  let cambios = false;
  for (const e of campos()) {
    if (!datos.has(e.name)) continue;
    const valor = datos.get(e.name);
    if (e.type === "radio") {
      if (e.value === valor) {
        e.checked = true;
        cambios = true;
      }
    } else if (e.type === "checkbox") {
      if (valor === "1" || valor === "0") {
        e.checked = valor === "1";
        cambios = true;
      }
    } else if (e.tagName === "SELECT") {
      if ([...e.options].some((o) => o.value === valor)) {
        e.value = valor;
        cambios = true;
      }
    } else if (e.type === "number" && (valor === "" || NUMERO.test(valor))) {
      e.value = valor;
      cambios = true;
    }
  }
  if (!cambios) return;
  // Abre los apartados plegados que tengan algún dato distinto del inicial, para que se vea.
  for (const d of formulario.querySelectorAll("details")) {
    const distinto = [...d.querySelectorAll("input, select")].some((e) =>
      e.type === "checkbox" || e.type === "radio" ? e.checked !== e.defaultChecked
        : e.tagName === "SELECT" ? !e.options[e.selectedIndex]?.defaultSelected : e.value !== e.defaultValue);
    if (distinto) d.open = true;
  }
  formulario.dispatchEvent(new Event("input", { bubbles: true }));
  formulario.dispatchEvent(new Event("change", { bubbles: true }));
}

function boton(clave, texto) {
  const b = document.createElement("button");
  b.type = "button";
  b.className = "accion";
  b.innerHTML = `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONOS[clave]}</svg>`;
  b.append(texto);
  return b;
}

function crearBotones() {
  const zona = document.createElement("div");
  zona.className = "acciones";
  const titulo = document.createElement("p");
  titulo.className = "acciones-titulo";
  titulo.textContent = t.titulo;
  const fila = document.createElement("div");
  fila.className = "acciones-fila";
  const aviso = document.createElement("p");
  aviso.className = "acciones-aviso";
  aviso.setAttribute("role", "status");
  const nota = document.createElement("p");
  nota.className = "acciones-nota";
  nota.textContent = t.nota;

  if (typeof navigator.share === "function") {
    const compartir = boton("compartir", t.compartir);
    compartir.addEventListener("click", () => {
      navigator.share({ title: document.title, url: enlace() }).catch(() => {});
    });
    fila.append(compartir);
  }
  const copiar = boton("copiar", t.copiar);
  copiar.addEventListener("click", async () => {
    const url = enlace();
    aviso.replaceChildren();
    try {
      await navigator.clipboard.writeText(url);
      aviso.textContent = t.copiado;
    } catch {
      // Sin acceso al portapapeles: se muestra el enlace seleccionado para copiarlo a mano.
      const campo = document.createElement("input");
      campo.type = "text";
      campo.readOnly = true;
      campo.value = url;
      campo.setAttribute("aria-label", t.manual);
      aviso.append(t.manual, campo);
      campo.focus();
      campo.select();
    }
  });
  const imprimir = boton("imprimir", t.imprimir);
  imprimir.addEventListener("click", () => window.print());
  fila.append(copiar, imprimir);
  zona.append(titulo, fila, aviso, nota);

  const pie = document.createElement("p");
  pie.className = "solo-impresion";
  caja.append(zona, pie);

  // Al imprimir: fecha y enlace con los datos, y los apartados plegados abiertos.
  let plegados = [];
  window.addEventListener("beforeprint", () => {
    const fecha = new Date().toLocaleDateString(t.locale, { day: "numeric", month: "long", year: "numeric" });
    pie.textContent = t.impreso(fecha, enlace());
    plegados = [...formulario.querySelectorAll("details:not([open])")];
    for (const d of plegados) d.open = true;
  });
  window.addEventListener("afterprint", () => {
    for (const d of plegados) d.open = false;
    plegados = [];
  });
}

if (formulario && caja) {
  crearBotones();
  restaurar();
}
