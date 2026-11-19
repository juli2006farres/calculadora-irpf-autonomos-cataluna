// Cuánto facturar como autónomo para ganar un sueldo neto concreto (Cataluña, 2026).
import { facturacionParaNeto } from "./objetivo/calculo.js";
import { idioma, euros, numero, importe, fila, tabla, total, barra, mostrar, error, conectar } from "./comun.js";

const TEXTOS = {
  es: {
    error: "Revisa los importes: deben ser números positivos.",
    imposible: "Con estos datos no se alcanza ese sueldo neto. Prueba con un objetivo menor.",
    total: "Tienes que facturar al año (sin IVA)",
    nota: (mes, hora) => (hora ? `${mes} al mes · precio mínimo por hora: ${hora}` : `${mes} al mes`),
    partes: ["Para ti", "Gastos", "Cuota", "IRPF"],
    facturacion: "Facturación anual sin IVA",
    gastos: "Gastos de la actividad",
    cuota: (tramo, tipo, mes) => `Cuota de autónomos (tramo ${tramo} de la tabla ${tipo}, ${mes} al mes)`,
    tablas: { reducida: "reducida", general: "general" },
    irpf: (tipo) => `IRPF del año (tipo medio ${tipo} %)`,
    netoAnual: "Neto al año",
    netoMes: "Neto al mes (12 pagas)",
  },
  ca: {
    error: "Revisa els imports: han de ser nombres positius.",
    imposible: "Amb aquestes dades no s'arriba a aquest sou net. Prova amb un objectiu més baix.",
    total: "Has de facturar a l'any (sense IVA)",
    nota: (mes, hora) => (hora ? `${mes} al mes · preu mínim per hora: ${hora}` : `${mes} al mes`),
    partes: ["Per a tu", "Despeses", "Quota", "IRPF"],
    facturacion: "Facturació anual sense IVA",
    gastos: "Despeses de l'activitat",
    cuota: (tramo, tipo, mes) => `Quota d'autònoms (tram ${tramo} de la taula ${tipo}, ${mes} al mes)`,
    tablas: { reducida: "reduïda", general: "general" },
    irpf: (tipo) => `IRPF de l'any (tipus mitjà ${tipo} %)`,
    netoAnual: "Net a l'any",
    netoMes: "Net al mes (12 pagues)",
  },
};
const t = TEXTOS[idioma];
const resultado = document.getElementById("resultado");

function calcular() {
  const netoMensual = importe("neto");
  const gastos = importe("gastos");
  const horas = importe("horas");
  if (netoMensual === null || gastos === null || horas === null) return mostrar(resultado, error(t.error));
  const r = facturacionParaNeto({
    netoMensual,
    gastos,
    modalidad: document.getElementById("modalidad").value,
    cumpleRequisitosArt32: document.getElementById("cliente").checked,
    inicioActividad: document.getElementById("inicio").checked,
    comunidad: document.getElementById("comunidad").value,
  });
  if (r === null) return mostrar(resultado, error(t.imposible));
  const porHora = horas > 0 ? euros.format(Math.ceil((r.ingresos / (horas * 12)) * 100) / 100) : null;
  const [paraTi, cGastos, cCuota, cIrpf] = t.partes;
  mostrar(
    resultado,
    total(t.total, euros.format(r.ingresos), t.nota(euros.format(Math.round((r.ingresos / 12) * 100) / 100), porHora)),
    barra([
      { texto: paraTi, valor: r.netoAnual, color: "#2f8f6a" },
      { texto: cGastos, valor: gastos, color: "#8a96a3" },
      { texto: cCuota, valor: r.cuotaAnual, color: "#d08a2e" },
      { texto: cIrpf, valor: r.irpf, color: "#1d5f8f" },
    ]),
    tabla([
      fila([t.facturacion, euros.format(r.ingresos)]),
      fila([t.gastos, `− ${euros.format(gastos)}`]),
      fila([t.cuota(r.tramo, t.tablas[r.tabla], euros.format(r.cuotaMensual)), `− ${euros.format(r.cuotaAnual)}`]),
      fila([t.irpf(numero.format(r.tipoMedioIrpf)), `− ${euros.format(r.irpf)}`]),
      fila([t.netoAnual, euros.format(r.netoAnual)], true),
      fila([t.netoMes, euros.format(r.netoMensual)]),
    ]),
  );
}

conectar(calcular);
