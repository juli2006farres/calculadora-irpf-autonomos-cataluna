// Tarifa plana de autónomos (cuota reducida por inicio de actividad, art. 38 ter de la Ley 20/2007).
// Compara la cuota reducida con la cuota normal de tu tramo, que calcula el módulo verificado de la cuota.
import { calcularCuota } from "../cuota/calculo.js";
import { DEDUCCION_GASTOS_GENERICOS } from "../cuota/tablas.js";
import { TABLAS } from "../irpf/tablas.js";

const aCentimos = (valor) => Math.round(valor * 100) / 100;

// Importe en 2026 según la guía de la Seguridad Social: 80 € de cuota reducida más la
// cotización del Mecanismo de Equidad Intergeneracional (0,9 %), 88,64 € en total.
export const TARIFA_PLANA_2026 = { cuotaReducida: 80, mei: 8.64, total: 88.64 };

// Salario mínimo interprofesional anual: 1.221 €/mes x 14 en 2026 (RD 126/2026)
// y 1.286 €/mes x 14 en 2027 (RD 1013/2026).
export const SMI_ANUAL = { 2026: 17_094, 2027: 18_004 };

// Meses de cuota reducida (art. 38 ter, apartados 1, 2 y 10).
export const MESES = {
  general: { inicial: 12, prorroga: 12 },
  especial: { inicial: 24, prorroga: 36 },
};

// Importe del segundo periodo en los casos especiales entre 2023 y 2025 (disposición
// transitoria 5.ª del RD-ley 13/2022). Para 2026 no hay una cifra publicada.
export const CUOTA_ESPECIAL_PRORROGA_2023_2025 = 160;

// El rendimiento que se compara con el SMI es el del art. 308.1.c LGSS: rendimiento neto
// más las cuotas, menos el 7 % de gastos genéricos. Como con la tarifa plana se pagan menos
// cuotas, los gastos de difícil justificación (en simplificada; en 2026, 10 % con un máximo de
// 3.000 € según el Real Decreto-ley 43/2026) se calculan con ella.
export function rendimientoParaSmi({ ingresos, gastos, modalidad, cumpleRequisitosArt32 }) {
  const cuotasTarifa = TARIFA_PLANA_2026.total * 12;
  const previo = ingresos - gastos - cuotasTarifa;
  const aplicaDificil = modalidad === "directa_simplificada" && !cumpleRequisitosArt32;
  const { porcentajeGastosDificilJustificacion: porcentaje, limiteGastosDificilJustificacion: limite } = TABLAS[2026];
  const dificil = aplicaDificil && previo > 0 ? Math.min((previo * porcentaje) / 100, limite) : 0;
  const computable = ingresos - gastos - dificil;
  return aCentimos(Math.max((computable * (100 - DEDUCCION_GASTOS_GENERICOS)) / 100, 0));
}

export function calcularTarifaPlana({ ingresos, gastos, modalidad, cumpleRequisitosArt32, especial = false }) {
  const normal = calcularCuota({ ingresos, gastos, modalidad, cumpleRequisitosArt32 });
  const meses = especial ? MESES.especial : MESES.general;
  const ahorroMensual = aCentimos(Math.max(normal.cuota_mensual_minima - TARIFA_PLANA_2026.total, 0));
  const rendimiento = rendimientoParaSmi({ ingresos, gastos, modalidad, cumpleRequisitosArt32 });
  const prorroga = Object.fromEntries(
    Object.entries(SMI_ANUAL).map(([anio, smi]) => [anio, { smi, cumple: rendimiento < smi }]),
  );
  return {
    tarifaMensual: TARIFA_PLANA_2026.total,
    cuotaNormalMensual: normal.cuota_mensual_minima,
    tramo: normal.tramo,
    tabla: normal.tabla,
    ahorroMensual,
    mesesIniciales: meses.inicial,
    mesesProrroga: meses.prorroga,
    pagadoPeriodoInicial: aCentimos(TARIFA_PLANA_2026.total * meses.inicial),
    ahorroPeriodoInicial: aCentimos(ahorroMensual * meses.inicial),
    // En los casos especiales el importe del segundo periodo de 2026 no está publicado,
    // así que solo se calcula el ahorro de la prórroga general.
    ahorroProrroga: especial ? null : aCentimos(ahorroMensual * meses.prorroga),
    rendimientoParaSmi: rendimiento,
    prorroga,
  };
}
