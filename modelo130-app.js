// Calculadora del modelo 130, trimestre a trimestre.
import { calcularModelo130, minoracionPorRendimiento } from "./modelo130/calculo.js";
import { idioma, euros, importe, fila, tabla, total, mostrar, error, conectar, elemento } from "./comun.js";

const TEXTOS = {
  es: {
    error: "Revisa los importes: deben ser números positivos.",
    total: (n) => `A ingresar en el modelo 130 del ${n}T`,
    nota: (suma) => `Total ingresado en el año hasta este trimestre: ${suma}`,
    cabecera: ["", "Rendimiento acumulado", "20 %", "Pagos anteriores", "Retenciones", "Minoración", "Resultado"],
    negativo: (n) =>
      n < 4
        ? "Resultado negativo: no pagas nada y lo restas en los trimestres siguientes."
        : "Resultado negativo: se presenta como negativa y no se paga nada.",
    cero: "No pagas nada este trimestre.",
    dificil: (n, cantidad) => `Incluye ${cantidad} de gastos de difícil justificación hasta el ${n}T.`,
  },
  ca: {
    error: "Revisa els imports: han de ser nombres positius.",
    total: (n) => `A ingressar al model 130 del ${n}T`,
    nota: (suma) => `Total ingressat a l'any fins a aquest trimestre: ${suma}`,
    cabecera: ["", "Rendiment acumulat", "20 %", "Pagaments anteriors", "Retencions", "Minoració", "Resultat"],
    negativo: (n) =>
      n < 4
        ? "Resultat negatiu: no pagues res i ho restes als trimestres següents."
        : "Resultat negatiu: es presenta com a negativa i no es paga res.",
    cero: "No pagues res aquest trimestre.",
    dificil: (n, cantidad) => `Inclou ${cantidad} de despeses de difícil justificació fins al ${n}T.`,
  },
};
const t = TEXTOS[idioma];
const resultado = document.getElementById("resultado");
const vacio = (id) => document.getElementById(id).value.trim() === "";

function calcular() {
  const trimestres = [];
  let ultimo = 1;
  for (let n = 1; n <= 4; n++) {
    const datos = { ingresos: importe(`i${n}`), gastos: importe(`g${n}`), retenciones: importe(`r${n}`) };
    if (Object.values(datos).some((v) => v === null)) return mostrar(resultado, error(t.error));
    if (!["i", "g", "r"].every((p) => vacio(`${p}${n}`))) ultimo = n;
    trimestres.push(datos);
  }
  const anterior = document.getElementById("anterior").value;
  const r = calcularModelo130({
    trimestres: trimestres.slice(0, ultimo),
    modalidad: document.getElementById("modalidad").value,
    minoracion: minoracionPorRendimiento(anterior === "mas" ? null : Number(anterior)),
  });
  const actual = r[r.length - 1];
  const suma = r.reduce((s, q) => s + q.a_ingresar, 0);
  const filas = r.map((q) =>
    fila(
      [
        `${q.trimestre}T`,
        euros.format(q.rendimiento),
        euros.format(q.pago_bruto),
        `− ${euros.format(q.pagos_anteriores)}`,
        `− ${euros.format(q.retenciones)}`,
        `− ${euros.format(q.minoracion + q.negativos_anteriores)}`,
        euros.format(q.resultado),
      ],
      q === actual,
    ),
  );
  const notas = [];
  if (actual.resultado < 0) notas.push(t.negativo(actual.trimestre));
  else if (actual.a_ingresar === 0) notas.push(t.cero);
  if (actual.dificil > 0) notas.push(t.dificil(actual.trimestre, euros.format(actual.dificil)));
  const envoltorio = elemento("div", undefined, "tabla-ancha");
  envoltorio.append(tabla(filas, t.cabecera));
  mostrar(
    resultado,
    total(t.total(actual.trimestre), euros.format(actual.a_ingresar), t.nota(euros.format(suma))),
    envoltorio,
    ...notas.map((texto) => elemento("p", texto, "nota")),
  );
}

conectar(calcular);
