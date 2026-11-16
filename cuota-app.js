// Calculadora de la cuota de autónomos. Todo ocurre en el navegador: no se envía nada.
// cuota/calculo.js y cuota/tablas.js son copias exactas de la compilación del servidor MCP.
import { calcularCuota } from "./cuota/calculo.js";
import { FECHA_REVISION_CUOTA, FUENTES_CUOTA } from "./cuota/tablas.js";

const TEXTOS = {
  es: {
    locale: "es-ES",
    error: "Revisa los importes: deben ser números positivos.",
    cuota: "Cuota mínima al mes",
    resumen: (tabla, tramo) => `Tabla ${tabla}, tramo ${tramo}`,
    tablas: { reducida: "reducida", general: "general" },
    filas: [
      "Rendimiento que cuenta para la cuota (al año)",
      "Deducción por gastos genéricos (7 %)",
      "Rendimiento neto al mes",
      "Base de cotización mínima",
      "Base de cotización máxima",
      "Cuota con la base máxima (al mes)",
      "Cuota mínima al año",
    ],
  },
  ca: {
    locale: "ca-ES",
    error: "Revisa els imports: han de ser nombres positius.",
    cuota: "Quota mínima al mes",
    resumen: (tabla, tramo) => `Taula ${tabla}, tram ${tramo}`,
    tablas: { reducida: "reduïda", general: "general" },
    filas: [
      "Rendiment que compta per a la quota (a l'any)",
      "Deducció per despeses genèriques (7 %)",
      "Rendiment net al mes",
      "Base de cotització mínima",
      "Base de cotització màxima",
      "Quota amb la base màxima (al mes)",
      "Quota mínima a l'any",
    ],
  },
};

const t = TEXTOS[document.documentElement.lang] ?? TEXTOS.es;
const formulario = document.getElementById("formulario");
const resultado = document.getElementById("resultado");
const euros = new Intl.NumberFormat(t.locale, { style: "currency", currency: "EUR" });

function importe(id) {
  const texto = document.getElementById(id).value.trim();
  if (texto === "") return 0;
  const valor = Number(texto);
  return Number.isFinite(valor) && valor >= 0 && valor <= 10_000_000 ? valor : null;
}

function fila(concepto, valor, fuerte = false) {
  const tr = document.createElement("tr");
  if (fuerte) tr.className = "fuerte";
  for (const texto of [concepto, valor]) {
    const td = document.createElement("td");
    td.textContent = texto;
    tr.append(td);
  }
  return tr;
}

function calcular() {
  const ingresos = importe("ingresos");
  const gastos = importe("gastos");
  if (ingresos === null || gastos === null) {
    const p = document.createElement("p");
    p.className = "error";
    p.textContent = t.error;
    resultado.replaceChildren(p);
    return;
  }

  const r = calcularCuota({
    ingresos,
    gastos,
    modalidad: document.getElementById("modalidad").value,
    cumpleRequisitosArt32: document.getElementById("cliente").checked,
  });

  const total = document.createElement("div");
  total.className = "total";
  const etiqueta = document.createElement("div");
  etiqueta.textContent = t.cuota;
  const cifra = document.createElement("div");
  cifra.className = "cifra";
  cifra.textContent = euros.format(r.cuota_mensual_minima);
  const nota = document.createElement("div");
  nota.textContent = t.resumen(t.tablas[r.tabla], r.tramo);
  total.append(etiqueta, cifra, nota);

  const [computable, deduccion, mensual, minima, maxima, cuotaMaxima, anual] = t.filas;
  const tabla = document.createElement("table");
  const cuerpo = document.createElement("tbody");
  cuerpo.append(
    fila(computable, euros.format(r.rendimiento_computable_anual)),
    fila(deduccion, `− ${euros.format(r.deduccion_gastos_genericos)}`),
    fila(mensual, euros.format(r.rendimiento_mensual), true),
    fila(minima, euros.format(r.base_minima)),
    fila(maxima, euros.format(r.base_maxima)),
    fila(cuotaMaxima, euros.format(r.cuota_mensual_maxima)),
    fila(anual, euros.format(r.cuota_anual_minima), true),
  );
  tabla.append(cuerpo);
  resultado.replaceChildren(total, tabla);
}

formulario.addEventListener("input", calcular);
formulario.addEventListener("submit", (evento) => evento.preventDefault());

document.getElementById("fecha-revision").textContent = new Date(`${FECHA_REVISION_CUOTA}T00:00:00Z`).toLocaleDateString(t.locale, {
  day: "numeric",
  month: "long",
  year: "numeric",
  timeZone: "UTC",
});
const lista = document.getElementById("fuentes");
for (const fuente of FUENTES_CUOTA) {
  const [texto, url] = fuente.split(/: (?=https:\/\/)/);
  const li = document.createElement("li");
  const enlace = document.createElement("a");
  enlace.href = url;
  enlace.textContent = texto;
  li.append(enlace);
  lista.append(li);
}

calcular();
