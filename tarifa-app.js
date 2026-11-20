// Calculadora de la tarifa plana de autónomos en 2026. Todo ocurre en el navegador: no se envía nada.
import { calcularTarifaPlana, TARIFA_PLANA_2026, CUOTA_ESPECIAL_PRORROGA_2023_2025 } from "./tarifa/calculo.js";
import { idioma, locale, euros, importe, elemento, fila, tabla, total, mostrar, error, conectar } from "./comun.js";

const enteros = new Intl.NumberFormat(locale, { style: "currency", currency: "EUR", maximumFractionDigits: 0, useGrouping: "always" });

const TEXTOS = {
  es: {
    error: "Revisa los importes: deben ser números positivos.",
    total: "Con la tarifa plana pagas al mes",
    nota: (meses) => `${enteros.format(TARIFA_PLANA_2026.cuotaReducida)} de cuota reducida + ${euros.format(TARIFA_PLANA_2026.mei)} del MEI, durante ${meses} meses`,
    tablas: { reducida: "reducida", general: "general" },
    normal: (tramo, tabla) => `Cuota normal de tu tramo (tramo ${tramo} de la tabla ${tabla})`,
    tarifa: "Cuota con la tarifa plana",
    ahorroMes: "Te ahorras al mes",
    ahorroPeriodo: (meses) => `Te ahorras en los primeros ${meses} meses`,
    pagado: (meses) => `Pagas en total en esos ${meses} meses`,
    prorrogaTitulo: (meses) => `¿Puedes alargarla ${meses} meses más?`,
    rendimiento: (r) => `Para alargarla, tu rendimiento neto del año, tal como lo calcula la Seguridad Social, tiene que quedar por debajo del salario mínimo de cada año que dure la prórroga. Con tus datos es de ${euros.format(r)} al año.`,
    cabecera: ["Año", "Salario mínimo anual", "¿Estás por debajo?"],
    si: "Sí",
    no: "No",
    ahorroProrroga: (ahorro) => `En los años en que estés por debajo, te ahorrarías otros ${euros.format(ahorro)} en esos 12 meses, con las tablas de 2026.`,
    especial: (meses) => `En tu caso la prórroga dura ${meses} meses. Entre 2023 y 2025 la cuota de ese periodo era de ${enteros.format(CUOTA_ESPECIAL_PRORROGA_2023_2025)} al mes; para 2026 no se ha publicado la cifra.`,
    sinProrroga: "Con estos ingresos no podrías alargarla: al acabar el primer periodo pasarías a pagar la cuota normal de tu tramo.",
  },
  ca: {
    error: "Revisa els imports: han de ser nombres positius.",
    total: "Amb la tarifa plana pagues al mes",
    nota: (meses) => `${enteros.format(TARIFA_PLANA_2026.cuotaReducida)} de quota reduïda + ${euros.format(TARIFA_PLANA_2026.mei)} del MEI, durant ${meses} mesos`,
    tablas: { reducida: "reduïda", general: "general" },
    normal: (tramo, tabla) => `Quota normal del teu tram (tram ${tramo} de la taula ${tabla})`,
    tarifa: "Quota amb la tarifa plana",
    ahorroMes: "T'estalvies al mes",
    ahorroPeriodo: (meses) => `T'estalvies en els primers ${meses} mesos`,
    pagado: (meses) => `Pagues en total en aquests ${meses} mesos`,
    prorrogaTitulo: (meses) => `La pots allargar ${meses} mesos més?`,
    rendimiento: (r) => `Per allargar-la, el teu rendiment net de l'any, tal com el calcula la Seguretat Social, ha de quedar per sota del salari mínim de cada any que duri la pròrroga. Amb les teves dades és de ${euros.format(r)} l'any.`,
    cabecera: ["Any", "Salari mínim anual", "Hi estàs per sota?"],
    si: "Sí",
    no: "No",
    ahorroProrroga: (ahorro) => `Els anys en què hi estiguis per sota, t'estalviaries uns altres ${euros.format(ahorro)} en aquests 12 mesos, amb les taules del 2026.`,
    especial: (meses) => `En el teu cas la pròrroga dura ${meses} mesos. Entre el 2023 i el 2025 la quota d'aquest període era de ${enteros.format(CUOTA_ESPECIAL_PRORROGA_2023_2025)} al mes; per al 2026 no se n'ha publicat la xifra.`,
    sinProrroga: "Amb aquests ingressos no la podries allargar: en acabar el primer període passaries a pagar la quota normal del teu tram.",
  },
};
const t = TEXTOS[idioma];
const resultado = document.getElementById("resultado");

function calcular() {
  const ingresos = importe("ingresos");
  const gastos = importe("gastos");
  if (ingresos === null || gastos === null) return mostrar(resultado, error(t.error));
  const especial = document.getElementById("especial").checked;
  const r = calcularTarifaPlana({
    ingresos,
    gastos,
    modalidad: document.getElementById("modalidad").value,
    cumpleRequisitosArt32: document.getElementById("cliente").checked,
    especial,
  });

  const resumen = tabla([
    fila([t.normal(r.tramo, t.tablas[r.tabla]), euros.format(r.cuotaNormalMensual)]),
    fila([t.tarifa, euros.format(r.tarifaMensual)]),
    fila([t.ahorroMes, euros.format(r.ahorroMensual)], true),
    fila([t.pagado(r.mesesIniciales), euros.format(r.pagadoPeriodoInicial)]),
    fila([t.ahorroPeriodo(r.mesesIniciales), euros.format(r.ahorroPeriodoInicial)], true),
  ]);

  const anios = Object.entries(r.prorroga);
  const smi = tabla(
    anios.map(([anio, p]) => fila([anio, enteros.format(p.smi), p.cumple ? t.si : t.no])),
    t.cabecera,
  );
  let conclusion;
  if (!anios.some(([, p]) => p.cumple)) conclusion = t.sinProrroga;
  else if (especial) conclusion = t.especial(r.mesesProrroga);
  else conclusion = t.ahorroProrroga(r.ahorroProrroga);

  mostrar(
    resultado,
    total(t.total, euros.format(r.tarifaMensual), t.nota(r.mesesIniciales)),
    resumen,
    elemento("h3", t.prorrogaTitulo(r.mesesProrroga)),
    elemento("p", t.rendimiento(r.rendimientoParaSmi)),
    smi,
    elemento("p", conclusion, "nota"),
  );
}

conectar(calcular);
