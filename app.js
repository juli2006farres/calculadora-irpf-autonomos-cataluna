// Conecta el formulario con el cálculo. Todo ocurre en el navegador: no se envía nada.
// irpf/calculo.js e irpf/tablas.js son copias exactas de la compilación del servidor MCP,
// así la web y el servidor siempre dan el mismo resultado.
import { calcularIrpf } from "./irpf/calculo.js";
import { FECHA_REVISION_TABLAS, FUENTES_FISCALES } from "./irpf/tablas.js";

const IMPORTE_MAXIMO = 10_000_000;
const formulario = document.getElementById("formulario");
const resultado = document.getElementById("resultado");

const euros = new Intl.NumberFormat("es-ES", { style: "currency", currency: "EUR" });
const porcentaje = new Intl.NumberFormat("es-ES", { maximumFractionDigits: 2 });

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
    mostrarError("Revisa los importes: deben ser números positivos y los descendientes, números enteros.");
    return;
  }
  if (datos.descendientesMenores3 > datos.descendientesMenores25) {
    mostrarError("Los menores de 3 años no pueden ser más que el total de descendientes.");
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
  if (r.resultado_estimado >= 0) {
    etiqueta.textContent = "Resultado: a pagar";
    cifra.textContent = euros.format(r.resultado_estimado);
  } else {
    etiqueta.textContent = "Resultado: a devolver";
    cifra.textContent = euros.format(-r.resultado_estimado);
  }
  nota.textContent = `IRPF total del año: ${euros.format(r.cuota_integra)} · tipo medio ${porcentaje.format(r.tipo_medio_porcentaje)} %`;
  total.append(etiqueta, cifra, nota);

  const tabla = document.createElement("table");
  const cuerpo = document.createElement("tbody");
  cuerpo.append(
    fila("Ingresos menos gastos y cuotas", euros.format(r.rendimiento_previo)),
    fila("Gastos de difícil justificación", `− ${euros.format(r.gastos_dificil_justificacion)}`),
    fila("Reducción por rendimientos de actividades (art. 32.2)", `− ${euros.format(r.reduccion_art_32)}`),
    fila("Reducción por inicio de actividad (20 %)", `− ${euros.format(r.reduccion_inicio_actividad)}`),
    fila("Base liquidable", euros.format(r.base_liquidable_general), true),
    fila("Mínimo personal y familiar (no tributa)", euros.format(r.minimo_personal_y_familiar)),
    fila("Cuota estatal", euros.format(r.cuota_estatal)),
    fila("Cuota catalana", euros.format(r.cuota_autonomica)),
    fila("IRPF total del año", euros.format(r.cuota_integra), true),
    fila("Retenciones y pagos a cuenta", `− ${euros.format(r.pagos_a_cuenta)}`),
  );
  tabla.append(cuerpo);
  resultado.replaceChildren(total, tabla);
}

formulario.addEventListener("input", calcular);
formulario.addEventListener("submit", (evento) => evento.preventDefault());

document.getElementById("fecha-revision").textContent = new Date(`${FECHA_REVISION_TABLAS}T00:00:00Z`).toLocaleDateString("es-ES", {
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
