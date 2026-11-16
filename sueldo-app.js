// Calculadora del sueldo neto de un autónomo en Cataluña en 2026.
import { calcularSueldoNeto } from "./sueldo/calculo.js";
import { idioma, euros, numero, importe, fila, tabla, total, barra, mostrar, error, conectar } from "./comun.js";

const TEXTOS = {
  es: {
    error: "Revisa los importes: deben ser números positivos.",
    total: "Te quedan al mes (12 pagas)",
    nota: (anual, cada100) => `${anual} al año · de cada 100 € que facturas te quedan ${cada100} €`,
    partes: ["Para ti", "Gastos", "Cuota", "IRPF"],
    ingresos: "Ingresos sin IVA",
    gastos: "Gastos de la actividad",
    cuota: (tramo, tipo, mes) => `Cuota de autónomos (tramo ${tramo} de la tabla ${tipo}, ${mes} al mes)`,
    cuotaPropia: (mes) => `Cuota de autónomos (${mes} al mes)`,
    tablas: { reducida: "reducida", general: "general" },
    irpf: (tipo) => `IRPF del año (tipo medio ${tipo} %)`,
    netoAnual: "Neto al año",
    neto14: "Neto al mes en 14 pagas",
    negativo: "Con estos datos no queda beneficio: los gastos, la cuota y el IRPF superan los ingresos.",
  },
  ca: {
    error: "Revisa els imports: han de ser nombres positius.",
    total: "Et queden al mes (12 pagues)",
    nota: (anual, cada100) => `${anual} a l'any · de cada 100 € que factures et queden ${cada100} €`,
    partes: ["Per a tu", "Despeses", "Quota", "IRPF"],
    ingresos: "Ingressos sense IVA",
    gastos: "Despeses de l'activitat",
    cuota: (tramo, tipo, mes) => `Quota d'autònoms (tram ${tramo} de la taula ${tipo}, ${mes} al mes)`,
    cuotaPropia: (mes) => `Quota d'autònoms (${mes} al mes)`,
    tablas: { reducida: "reduïda", general: "general" },
    irpf: (tipo) => `IRPF de l'any (tipus mitjà ${tipo} %)`,
    netoAnual: "Net a l'any",
    neto14: "Net al mes en 14 pagues",
    negativo: "Amb aquestes dades no queda benefici: les despeses, la quota i l'IRPF superen els ingressos.",
  },
};
const t = TEXTOS[idioma];
const resultado = document.getElementById("resultado");

function calcular() {
  const ingresos = importe("ingresos");
  const gastos = importe("gastos");
  const cuotaMensual = importe("cuota", "vacia");
  if (ingresos === null || gastos === null || cuotaMensual === null) return mostrar(resultado, error(t.error));
  const propia = cuotaMensual !== "vacia";
  const r = calcularSueldoNeto({
    ingresos,
    gastos,
    cuotaMensual: propia ? cuotaMensual : null,
    modalidad: document.getElementById("modalidad").value,
    cumpleRequisitosArt32: document.getElementById("cliente").checked,
    inicioActividad: document.getElementById("inicio").checked,
  });
  const concepto = propia
    ? t.cuotaPropia(euros.format(r.cuotaMensual))
    : t.cuota(r.tramo, t.tablas[r.tabla], euros.format(r.cuotaMensual));
  const filas = [
    fila([t.ingresos, euros.format(ingresos)]),
    fila([t.gastos, `− ${euros.format(gastos)}`]),
    fila([concepto, `− ${euros.format(r.cuotaAnual)}`]),
    fila([t.irpf(numero.format(r.tipoMedioIrpf)), `− ${euros.format(r.irpf)}`]),
    fila([t.netoAnual, euros.format(r.netoAnual)], true),
    fila([t.neto14, euros.format(Math.round((r.netoAnual / 14) * 100) / 100)]),
  ];
  const [paraTi, cGastos, cCuota, cIrpf] = t.partes;
  const reparto = barra([
    { texto: paraTi, valor: r.netoAnual, color: "#2f8f6a" },
    { texto: cGastos, valor: gastos, color: "#8a96a3" },
    { texto: cCuota, valor: r.cuotaAnual, color: "#d08a2e" },
    { texto: cIrpf, valor: r.irpf, color: "#1d5f8f" },
  ]);
  const cabeza =
    r.netoAnual < 0
      ? error(t.negativo)
      : total(t.total, euros.format(r.netoMensual), t.nota(euros.format(r.netoAnual), numero.format(r.porCada100)));
  mostrar(resultado, cabeza, reparto, tabla(filas));
}

conectar(calcular);
