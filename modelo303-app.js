// Calculadora del modelo 303 (IVA trimestral). modelo303/calculo.js es copia de la compilación del servidor MCP.
import { calcularModelo303 } from "./modelo303/calculo.js";
import { idioma, euros, importe, fila, tabla, total, mostrar, error, conectar, elemento } from "./comun.js";

const TEXTOS = {
  es: {
    error: "Revisa los importes: deben ser números positivos.",
    situacion: {
      a_ingresar: "A ingresar en el modelo 303",
      resultado_cero: "Resultado cero: no pagas nada",
      a_compensar: "A compensar en los próximos trimestres",
      a_devolver_o_compensar: "A devolver o a compensar",
    },
    nota: (t) => `${t}T · plazo: ${["", "1 al 20 de abril", "1 al 20 de julio", "1 al 20 de octubre", "1 al 30 de enero"][t]}`,
    repercutido: (tipo) => `IVA de tus facturas al ${tipo} %`,
    soportado: (tipo) => `IVA de tus gastos al ${tipo} %`,
    c27: "Total IVA repercutido (casilla 27)",
    c45: "Total IVA deducible (casilla 45)",
    c46: "Diferencia (casilla 46)",
    c78: "Pendiente de trimestres anteriores que aplicas (casilla 78)",
    c71: "Resultado (casilla 71)",
    pendiente: (x) => `Te quedan ${x} pendientes de compensar en los próximos trimestres del año.`,
    cuarto: "En el 4T puedes pedir la devolución indicando tu cuenta bancaria, o seguir compensándolo.",
  },
  ca: {
    error: "Revisa els imports: han de ser nombres positius.",
    situacion: {
      a_ingresar: "A ingressar al model 303",
      resultado_cero: "Resultat zero: no pagues res",
      a_compensar: "A compensar els propers trimestres",
      a_devolver_o_compensar: "A retornar o a compensar",
    },
    nota: (t) => `${t}T · termini: ${["", "de l'1 al 20 d'abril", "de l'1 al 20 de juliol", "de l'1 al 20 d'octubre", "de l'1 al 30 de gener"][t]}`,
    repercutido: (tipo) => `IVA de les teves factures al ${tipo} %`,
    soportado: (tipo) => `IVA de les teves despeses al ${tipo} %`,
    c27: "Total IVA repercutit (casella 27)",
    c45: "Total IVA deduïble (casella 45)",
    c46: "Diferència (casella 46)",
    c78: "Pendent de trimestres anteriors que apliques (casella 78)",
    c71: "Resultat (casella 71)",
    pendiente: (x) => `Et queden ${x} pendents de compensar els propers trimestres de l'any.`,
    cuarto: "Al 4T pots demanar la devolució indicant el teu compte bancari, o continuar compensant-ho.",
  },
};
const t = TEXTOS[idioma];
const resultado = document.getElementById("resultado");

function calcular() {
  const leer = (p) => ({ 21: importe(`${p}21`), 10: importe(`${p}10`), 4: importe(`${p}4`) });
  const ventas = leer("v");
  const gastos = leer("g");
  const compensar = importe("compensar");
  if ([...Object.values(ventas), ...Object.values(gastos), compensar].some((v) => v === null)) {
    return mostrar(resultado, error(t.error));
  }
  const trimestre = Number(document.getElementById("trimestre").value);
  const r = calcularModelo303({ trimestre, ventas, gastos, compensarAnteriores: compensar });
  const filas = [
    ...r.iva_repercutido.filter((x) => x.base > 0).map((x) => fila([t.repercutido(x.tipo), euros.format(x.cuota)])),
    fila([t.c27, euros.format(r.casilla_27)], true),
    ...r.iva_soportado.filter((x) => x.base > 0).map((x) => fila([t.soportado(x.tipo), `− ${euros.format(x.cuota)}`])),
    fila([t.c45, `− ${euros.format(r.casilla_45)}`], true),
    fila([t.c46, euros.format(r.casilla_46)]),
  ];
  if (r.casilla_110 > 0) filas.push(fila([t.c78, `− ${euros.format(r.casilla_78)}`]));
  filas.push(fila([t.c71, euros.format(r.casilla_71)], true));
  const notas = [];
  if (r.pendiente_para_siguientes > 0) notas.push(t.pendiente(euros.format(r.pendiente_para_siguientes)));
  if (r.situacion === "a_devolver_o_compensar") notas.push(t.cuarto);
  mostrar(
    resultado,
    total(t.situacion[r.situacion], euros.format(r.importe), t.nota(trimestre)),
    tabla(filas),
    ...notas.map((x) => elemento("p", x, "nota")),
  );
}

conectar(calcular);
