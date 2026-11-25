// Calculadora de la regularización de la cuota de autónomos de 2026. Todo ocurre en el navegador.
import { calcularRegularizacion, CUOTA_MAXIMA_2026, CUOTA_MINIMA_2026 } from "./regularizacion/calculo.js";
import { idioma, euros, importe, elemento, fila, tabla, total, mostrar, error, conectar } from "./comun.js";

const TEXTOS = {
  es: {
    error: "Revisa los importes: deben ser números positivos.",
    errorCuota: `Revisa la cuota: en 2026 va de ${euros.format(CUOTA_MINIMA_2026)} a ${euros.format(CUOTA_MAXIMA_2026)} al mes, salvo con la tarifa plana.`,
    tarifa: "Los meses con tarifa plana no se regularizan (art. 38 ter.6 de la Ley 20/2007). En la prórroga tampoco, si tus rendimientos del año quedan por debajo del salario mínimo. Esta calculadora es para quien ha pagado la cuota normal todo el tiempo de alta.",
    pagar: "Tendrás que pagar",
    devolver: "Te devolverán",
    nada: "No tendrás que pagar ni te devolverán nada",
    notaPagar: (d, m) => `${euros.format(d)} al mes durante ${m} ${m === 1 ? "mes" : "meses"}: lo que te faltó para llegar a la cuota mínima de tu tramo real.`,
    notaDevolver: (d, m) => `${euros.format(d)} al mes durante ${m} ${m === 1 ? "mes" : "meses"}: lo que pagaste por encima de la cuota máxima de tu tramo real.`,
    notaNada: "Tu cuota está entre la mínima y la máxima de tu tramo real.",
    tablas: { reducida: "reducida", general: "general" },
    filas: {
      previo: "Ingresos menos gastos",
      cuotas: (m) => `Cuotas pagadas (${m} ${m === 1 ? "mes" : "meses"})`,
      dificil: "Gastos de difícil justificación (10 %, máx. 3.000 €)",
      neto: "Rendimiento neto del IRPF",
      computable: "Rendimiento computable (neto + cuotas)",
      deduccion: "Deducción del 7 % por gastos genéricos",
      mensual: (m) => `Rendimiento al mes (entre ${m} ${m === 1 ? "mes" : "meses"})`,
      tramo: "Tu tramo real",
      tramoTexto: (n, t) => `Tramo ${n} de la tabla ${t}`,
      minima: "Cuota mínima de ese tramo",
      maxima: "Cuota máxima de ese tramo",
      tuya: "Tu cuota al mes",
    },
    cuandoPagar: "Plazo: hasta el último día del mes siguiente a que te notifiquen la regularización, sin recargo ni intereses si pagas a tiempo.",
    cuandoDevolver: "La Seguridad Social te lo devuelve de oficio, sin intereses, antes del 30 de abril del año siguiente a aquel en que Hacienda le comunique tus rendimientos.",
    cuando: "La regularización de 2026 llegará a partir de 2027, cuando Hacienda comunique a la Seguridad Social los rendimientos de tu declaración de la renta de 2026.",
  },
  ca: {
    error: "Revisa els imports: han de ser nombres positius.",
    errorCuota: `Revisa la quota: el 2026 va de ${euros.format(CUOTA_MINIMA_2026)} a ${euros.format(CUOTA_MAXIMA_2026)} al mes, excepte amb la tarifa plana.`,
    tarifa: "Els mesos amb tarifa plana no es regularitzen (art. 38 ter.6 de la Llei 20/2007). A la pròrroga tampoc, si els teus rendiments de l'any queden per sota del salari mínim. Aquesta calculadora és per a qui ha pagat la quota normal tot el temps d'alta.",
    pagar: "Hauràs de pagar",
    devolver: "Et retornaran",
    nada: "No hauràs de pagar ni et retornaran res",
    notaPagar: (d, m) => `${euros.format(d)} al mes durant ${m} ${m === 1 ? "mes" : "mesos"}: el que et va faltar per arribar a la quota mínima del teu tram real.`,
    notaDevolver: (d, m) => `${euros.format(d)} al mes durant ${m} ${m === 1 ? "mes" : "mesos"}: el que vas pagar per sobre de la quota màxima del teu tram real.`,
    notaNada: "La teva quota és entre la mínima i la màxima del teu tram real.",
    tablas: { reducida: "reduïda", general: "general" },
    filas: {
      previo: "Ingressos menys despeses",
      cuotas: (m) => `Quotes pagades (${m} ${m === 1 ? "mes" : "mesos"})`,
      dificil: "Despeses de difícil justificació (10 %, màx. 3.000 €)",
      neto: "Rendiment net de l'IRPF",
      computable: "Rendiment computable (net + quotes)",
      deduccion: "Deducció del 7 % per despeses genèriques",
      mensual: (m) => `Rendiment al mes (entre ${m} ${m === 1 ? "mes" : "mesos"})`,
      tramo: "El teu tram real",
      tramoTexto: (n, t) => `Tram ${n} de la taula ${t}`,
      minima: "Quota mínima d'aquest tram",
      maxima: "Quota màxima d'aquest tram",
      tuya: "La teva quota al mes",
    },
    cuandoPagar: "Termini: fins a l'últim dia del mes següent al que et notifiquin la regularització, sense recàrrec ni interessos si pagues a temps.",
    cuandoDevolver: "La Seguretat Social te'l retorna d'ofici, sense interessos, abans del 30 d'abril de l'any següent a aquell en què Hisenda li comuniqui els teus rendiments.",
    cuando: "La regularització del 2026 arribarà a partir del 2027, quan Hisenda comuniqui a la Seguretat Social els rendiments de la teva declaració de la renda del 2026.",
  },
};
const t = TEXTOS[idioma];
const resultado = document.getElementById("resultado");

function calcular() {
  if (document.getElementById("tarifa").checked) return mostrar(resultado, elemento("p", t.tarifa, "aviso"));
  const ingresos = importe("ingresos");
  const gastos = importe("gastos");
  const cuotaMensual = importe("cuota", null);
  if (ingresos === null || gastos === null || cuotaMensual === null) return mostrar(resultado, error(t.error));
  if (cuotaMensual < CUOTA_MINIMA_2026 || cuotaMensual > CUOTA_MAXIMA_2026) return mostrar(resultado, error(t.errorCuota));
  const meses = Number(document.getElementById("meses").value);
  const r = calcularRegularizacion({
    ingresos,
    gastos,
    cuotaMensual,
    meses,
    modalidad: document.getElementById("modalidad").value,
    cumpleRequisitosArt32: document.getElementById("cliente").checked,
  });
  const f = t.filas;
  const titulo = { pagar: t.pagar, devolver: t.devolver, nada: t.nada }[r.resultado];
  const nota = r.resultado === "pagar" ? t.notaPagar(r.diferenciaMensual, meses)
    : r.resultado === "devolver" ? t.notaDevolver(r.diferenciaMensual, meses) : t.notaNada;
  const filas = [
    fila([f.previo, euros.format(ingresos - gastos)]),
    fila([f.cuotas(meses), `− ${euros.format(r.cuotasPagadas)}`]),
  ];
  if (r.gastosDificil > 0) filas.push(fila([f.dificil, `− ${euros.format(r.gastosDificil)}`]));
  filas.push(
    fila([f.neto, euros.format(r.rendimientoNeto)], true),
    fila([f.computable, euros.format(r.rendimientoComputable)]),
    fila([f.deduccion, `− ${euros.format(r.deduccion)}`]),
    fila([f.mensual(meses), euros.format(r.rendimientoMensual)], true),
    fila([f.tramo, f.tramoTexto(r.tramo, t.tablas[r.tabla])]),
    fila([f.minima, euros.format(r.cuotaMinima)]),
    fila([f.maxima, euros.format(r.cuotaMaxima)]),
    fila([f.tuya, euros.format(cuotaMensual)], true),
  );
  const cuando = r.resultado === "pagar" ? t.cuandoPagar : r.resultado === "devolver" ? t.cuandoDevolver : "";
  mostrar(
    resultado,
    total(titulo, euros.format(r.importe), nota),
    tabla(filas),
    ...(cuando ? [elemento("p", cuando, "nota")] : []),
    elemento("p", t.cuando, "nota"),
  );
}

conectar(calcular);
