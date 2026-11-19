// Calculadora de IRPF de autónomos para todas las comunidades de régimen común.
// irpf/calculo.js e irpf/tablas.js son copias exactas de la compilación del servidor MCP.
import { calcularIrpf } from "./irpf/calculo.js";
import { COMUNIDADES, NOMBRES_COMUNIDADES } from "./irpf/tablas.js";
import { idioma, euros, numero, importe, fila, tabla, total, mostrar, error, conectar, elemento } from "./comun.js";

const NOMBRES_CA = {
  andalucia: "Andalusia",
  aragon: "Aragó",
  asturias: "Principat d'Astúries",
  baleares: "Illes Balears",
  canarias: "Canàries",
  cantabria: "Cantàbria",
  castilla_la_mancha: "Castella-la Manxa",
  castilla_y_leon: "Castella i Lleó",
  cataluna: "Catalunya",
  extremadura: "Extremadura",
  galicia: "Galícia",
  la_rioja: "La Rioja",
  madrid: "Comunitat de Madrid",
  murcia: "Regió de Múrcia",
  valenciana: "Comunitat Valenciana",
};
const nombre = (c) => (idioma === "ca" ? NOMBRES_CA[c] : NOMBRES_COMUNIDADES[c]);

const TEXTOS = {
  es: {
    errorImportes: "Revisa los importes: deben ser números positivos y los descendientes, números enteros.",
    errorMenores: "Los menores de 3 años no pueden ser más que el total de descendientes.",
    aPagar: "Resultado: a pagar",
    aDevolver: "Resultado: a devolver",
    resumen: (total, tipo) => `IRPF total del año: ${total} · tipo medio ${tipo} %`,
    filas: ["Ingresos menos gastos y cuotas", "Gastos de difícil justificación", "Reducción por rendimientos (art. 32.2)",
      "Reducción por inicio de actividad (20 %)", "Base liquidable", "Cuota estatal", "IRPF total del año", "Retenciones y pagos a cuenta"],
    autonomica: (c) => `Cuota autonómica (${c})`,
    comparar: "El mismo caso en cada comunidad",
    cabecera: ["Comunidad", "IRPF del año", "Diferencia"],
  },
  ca: {
    errorImportes: "Revisa els imports: han de ser nombres positius i els descendents, nombres enters.",
    errorMenores: "Els menors de 3 anys no poden ser més que el total de descendents.",
    aPagar: "Resultat: a pagar",
    aDevolver: "Resultat: a retornar",
    resumen: (total, tipo) => `IRPF total de l'any: ${total} · tipus mitjà ${tipo} %`,
    filas: ["Ingressos menys despeses i quotes", "Despeses de difícil justificació", "Reducció per rendiments (art. 32.2)",
      "Reducció per inici d'activitat (20 %)", "Base liquidable", "Quota estatal", "IRPF total de l'any", "Retencions i pagaments a compte"],
    autonomica: (c) => `Quota autonòmica (${c})`,
    comparar: "El mateix cas a cada comunitat",
    cabecera: ["Comunitat", "IRPF de l'any", "Diferència"],
  },
};
const t = TEXTOS[idioma];
const resultado = document.getElementById("resultado");
const selector = document.getElementById("comunidad");

function entero(id) {
  const valor = importe(id);
  return valor !== null && Number.isInteger(valor) && valor <= 20 ? valor : null;
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
  if (Object.values(datos).some((v) => v === null)) return mostrar(resultado, error(t.errorImportes));
  if (datos.descendientesMenores3 > datos.descendientesMenores25) return mostrar(resultado, error(t.errorMenores));
  const comun = {
    ...datos,
    ejercicio: Number(document.getElementById("anio").value),
    modalidad: document.getElementById("modalidad").value,
    cumpleRequisitosArt32: document.getElementById("cliente").checked,
    inicioActividad: document.getElementById("inicio").checked,
    minimoDescendientesCompartido: document.getElementById("compartido").checked,
  };
  const elegida = selector.value;
  const r = calcularIrpf({ ...comun, comunidad: elegida });
  const [previo, dificil, art32, inicio, base, estatal, irpf, pagos] = t.filas;
  const detalle = tabla([
    fila([previo, euros.format(r.rendimiento_previo)]),
    fila([dificil, `− ${euros.format(r.gastos_dificil_justificacion)}`]),
    fila([art32, `− ${euros.format(r.reduccion_art_32)}`]),
    fila([inicio, `− ${euros.format(r.reduccion_inicio_actividad)}`]),
    fila([base, euros.format(r.base_liquidable_general)], true),
    fila([estatal, euros.format(r.cuota_estatal)]),
    fila([t.autonomica(nombre(elegida)), euros.format(r.cuota_autonomica)]),
    fila([irpf, euros.format(r.cuota_integra)], true),
    fila([pagos, `− ${euros.format(r.pagos_a_cuenta)}`]),
  ]);
  // Comparativa: el mismo caso en las 15 comunidades, de menos a más IRPF.
  const todas = COMUNIDADES.map((c) => ({ c, irpf: calcularIrpf({ ...comun, comunidad: c }).cuota_integra })).sort((a, b) => a.irpf - b.irpf);
  const filas = todas.map(({ c, irpf: valor }) => {
    const diferencia = valor - r.cuota_integra;
    const texto = Math.abs(diferencia) < 0.005 ? "—" : `${diferencia > 0 ? "+" : "−"} ${euros.format(Math.abs(diferencia))}`;
    return fila([nombre(c), euros.format(valor), texto], c === elegida);
  });
  const comparativa = tabla(filas, t.cabecera);
  mostrar(
    resultado,
    total(r.resultado_estimado >= 0 ? t.aPagar : t.aDevolver, euros.format(Math.abs(r.resultado_estimado)),
      t.resumen(euros.format(r.cuota_integra), numero.format(r.tipo_medio_porcentaje))),
    detalle,
    elemento("p", t.comparar, "nota"),
    comparativa,
  );
}

conectar(calcular);
