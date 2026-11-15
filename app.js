// Conecta el formulario con el cálculo. Todo ocurre en el navegador: no se envía nada.
// irpf/calculo.js e irpf/tablas.js son copias exactas de la compilación del servidor MCP,
// así la web y el servidor siempre dan el mismo resultado.
// La misma lógica sirve para la página en castellano y en catalán: solo cambian los textos.
import { calcularIrpf } from "./irpf/calculo.js";
import { FECHA_REVISION_TABLAS, FUENTES_FISCALES } from "./irpf/tablas.js";

const TEXTOS = {
  es: {
    locale: "es-ES",
    errorImportes: "Revisa los importes: deben ser números positivos y los descendientes, números enteros.",
    errorMenores: "Los menores de 3 años no pueden ser más que el total de descendientes.",
    aPagar: "Resultado: a pagar",
    aDevolver: "Resultado: a devolver",
    resumen: (total, tipo) => `IRPF total del año: ${total} · tipo medio ${tipo} %`,
    filas: [
      "Ingresos menos gastos y cuotas",
      "Gastos de difícil justificación",
      "Reducción por rendimientos de actividades (art. 32.2)",
      "Reducción por inicio de actividad (20 %)",
      "Base liquidable",
      "Mínimo personal y familiar (no tributa)",
      "Cuota estatal",
      "Cuota catalana",
      "IRPF total del año",
      "Retenciones y pagos a cuenta",
    ],
  },
  ca: {
    locale: "ca-ES",
    errorImportes: "Revisa els imports: han de ser nombres positius i els descendents, nombres enters.",
    errorMenores: "Els menors de 3 anys no poden ser més que el total de descendents.",
    aPagar: "Resultat: a pagar",
    aDevolver: "Resultat: a retornar",
    resumen: (total, tipo) => `IRPF total de l'any: ${total} · tipus mitjà ${tipo} %`,
    filas: [
      "Ingressos menys despeses i quotes",
      "Despeses de difícil justificació",
      "Reducció per rendiments d'activitats (art. 32.2)",
      "Reducció per inici d'activitat (20 %)",
      "Base liquidable",
      "Mínim personal i familiar (no tributa)",
      "Quota estatal",
      "Quota catalana",
      "IRPF total de l'any",
      "Retencions i pagaments a compte",
    ],
  },
};

const t = TEXTOS[document.documentElement.lang] ?? TEXTOS.es;
const IMPORTE_MAXIMO = 10_000_000;
const formulario = document.getElementById("formulario");
const resultado = document.getElementById("resultado");

const euros = new Intl.NumberFormat(t.locale, { style: "currency", currency: "EUR" });
const porcentaje = new Intl.NumberFormat(t.locale, { maximumFractionDigits: 2 });

// Lee un importe. Devuelve null si no es un número válido, para no calcular con datos inventados.
function importe(id) {
  const texto = document.getElementById(id).value.trim();
  if (texto === "") return 0;
  const valor = Number(texto);
  return Number.isFinite(valor) && valor >= 0 && valor <= IMPORTE_MAXIMO ? valor : null;
}

function entero(id) {
  const valor = importe(id);
  return valor !== null && Number.isInteger(valor) && valor <= 20 ? valor : null;
}

const marcado = (id) => document.getElementById(id).checked;

// Crea una fila de la tabla con textContent, nunca con HTML, para no interpretar lo escrito.
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

function mostrarError(mensaje) {
  const p = document.createElement("p");
  p.className = "error";
  p.textContent = mensaje;
  resultado.replaceChildren(p);
}

function calcular() {
  const datos = {
    ingresos: importe("ingresos"),
    gastos: importe("gastos"),
    cuotasAutonomo: importe("cuotas"),
    pagosACuenta: importe("pagos"),
    descendientesMenores25: entero("hijos"),
    descendientesMenores3: entero("menores3"),
  };
  if (Object.values(datos).some((v) => v === null)) {
    mostrarError(t.errorImportes);
    return;
  }
  if (datos.descendientesMenores3 > datos.descendientesMenores25) {
    mostrarError(t.errorMenores);
    return;
  }

  const r = calcularIrpf({
    ...datos,
    ejercicio: Number(document.getElementById("anio").value),
    modalidad: document.getElementById("modalidad").value,
    cumpleRequisitosArt32: marcado("cliente"),
    inicioActividad: marcado("inicio"),
    minimoDescendientesCompartido: marcado("compartido"),
  });

  const total = document.createElement("div");
  total.className = "total";
  const etiqueta = document.createElement("div");
  const cifra = document.createElement("div");
  cifra.className = "cifra";
  const nota = document.createElement("div");
  etiqueta.textContent = r.resultado_estimado >= 0 ? t.aPagar : t.aDevolver;
  cifra.textContent = euros.format(Math.abs(r.resultado_estimado));
  nota.textContent = t.resumen(euros.format(r.cuota_integra), porcentaje.format(r.tipo_medio_porcentaje));
  total.append(etiqueta, cifra, nota);

  const [previo, dificil, art32, inicio, base, minimo, estatal, catalana, irpf, pagos] = t.filas;
  const tabla = document.createElement("table");
  const cuerpo = document.createElement("tbody");
  cuerpo.append(
    fila(previo, euros.format(r.rendimiento_previo)),
    fila(dificil, `− ${euros.format(r.gastos_dificil_justificacion)}`),
    fila(art32, `− ${euros.format(r.reduccion_art_32)}`),
    fila(inicio, `− ${euros.format(r.reduccion_inicio_actividad)}`),
    fila(base, euros.format(r.base_liquidable_general), true),
    fila(minimo, euros.format(r.minimo_personal_y_familiar)),
    fila(estatal, euros.format(r.cuota_estatal)),
    fila(catalana, euros.format(r.cuota_autonomica)),
    fila(irpf, euros.format(r.cuota_integra), true),
    fila(pagos, `− ${euros.format(r.pagos_a_cuenta)}`),
  );
  tabla.append(cuerpo);
  resultado.replaceChildren(total, tabla);
}

formulario.addEventListener("input", calcular);
formulario.addEventListener("submit", (evento) => evento.preventDefault());

document.getElementById("fecha-revision").textContent = new Date(`${FECHA_REVISION_TABLAS}T00:00:00Z`).toLocaleDateString(t.locale, {
  day: "numeric",
  month: "long",
  year: "numeric",
  timeZone: "UTC",
});
const lista = document.getElementById("fuentes");
for (const fuente of FUENTES_FISCALES) {
  const [texto, url] = fuente.split(/: (?=https:\/\/)/);
  const li = document.createElement("li");
  const enlace = document.createElement("a");
  enlace.href = url;
  enlace.textContent = texto;
  li.append(enlace);
  lista.append(li);
}

calcular();
