// Utilidades compartidas por las calculadoras nuevas. Todo ocurre en el navegador.
export const idioma = document.documentElement.lang === "ca" ? "ca" : "es";
export const locale = idioma === "ca" ? "ca-ES" : "es-ES";
export const euros = new Intl.NumberFormat(locale, { style: "currency", currency: "EUR", useGrouping: "always" });
export const numero = new Intl.NumberFormat(locale, { maximumFractionDigits: 2 });

// Lee un importe. Si está vacío devuelve `vacio`; si no es válido, null.
export function importe(id, vacio = 0) {
  const texto = document.getElementById(id).value.trim();
  if (texto === "") return vacio;
  const valor = Number(texto);
  return Number.isFinite(valor) && valor >= 0 && valor <= 10_000_000 ? valor : null;
}

// Crea elementos con textContent, nunca con HTML, para no interpretar lo escrito.
export function elemento(etiqueta, texto, clase) {
  const nodo = document.createElement(etiqueta);
  if (texto !== undefined) nodo.textContent = texto;
  if (clase) nodo.className = clase;
  return nodo;
}

export function fila(celdas, fuerte = false, celda = "td") {
  const tr = elemento("tr", undefined, fuerte ? "fuerte" : undefined);
  for (const texto of celdas) tr.append(elemento(celda, texto));
  return tr;
}

export function tabla(filas, cabecera) {
  const t = document.createElement("table");
  if (cabecera) {
    const thead = document.createElement("thead");
    thead.append(fila(cabecera, false, "th"));
    t.append(thead);
  }
  const cuerpo = document.createElement("tbody");
  cuerpo.append(...filas);
  t.append(cuerpo);
  return t;
}

export function total(etiqueta, cifra, nota) {
  const caja = elemento("div", undefined, "total");
  caja.append(elemento("div", etiqueta), elemento("div", cifra, "cifra"));
  if (nota) caja.append(elemento("div", nota));
  return caja;
}

// Barra de reparto con su leyenda. partes: [{ texto, valor, color }].
export function barra(partes) {
  const fragmento = document.createDocumentFragment();
  const suma = partes.reduce((s, p) => s + Math.max(p.valor, 0), 0);
  if (suma <= 0) return fragmento;
  const caja = elemento("div", undefined, "barra");
  caja.setAttribute("aria-hidden", "true");
  const leyenda = elemento("div", undefined, "leyenda");
  for (const p of partes) {
    if (p.valor <= 0) continue;
    const trozo = document.createElement("span");
    trozo.style.width = `${(p.valor / suma) * 100}%`;
    trozo.style.background = p.color;
    caja.append(trozo);
    const item = document.createElement("span");
    const muestra = document.createElement("i");
    muestra.style.background = p.color;
    item.append(muestra, `${p.texto} ${numero.format(Math.round((p.valor / suma) * 100))} %`);
    leyenda.append(item);
  }
  fragmento.append(caja, leyenda);
  return fragmento;
}

export function mostrar(nodo, ...hijos) {
  nodo.replaceChildren(...hijos);
}

export function error(mensaje) {
  return elemento("p", mensaje, "error");
}

// Conecta el formulario: recalcula con cada cambio y nunca se envía.
export function conectar(calcular) {
  const formulario = document.getElementById("formulario");
  formulario.addEventListener("input", calcular);
  formulario.addEventListener("change", calcular);
  formulario.addEventListener("submit", (evento) => evento.preventDefault());
  calcular();
}
