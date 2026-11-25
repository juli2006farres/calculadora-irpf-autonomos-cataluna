// Regularización de la cuota de autónomos de 2026 (art. 308.1.c de la Ley General de la Seguridad Social).
// Cuando Hacienda comunica los rendimientos reales del año, la Seguridad Social mira en qué tramo caen:
// si pagaste menos que la cuota mínima de ese tramo, pagas la diferencia; si pagaste más que la máxima,
// te devuelve el exceso; si estás entre las dos, no cambia nada. Calcula el caso de una cuota igual
// todos los meses de alta, sin tarifa plana (que no se regulariza: art. 38 ter.6 de la Ley 20/2007).
import { buscarTramo, TIPO_TOTAL } from "../cuota/calculo.js";
import { DEDUCCION_GASTOS_GENERICOS, TRAMOS_CUOTA_2026 } from "../cuota/tablas.js";
import { TABLAS } from "../irpf/tablas.js";

const aCentimos = (valor) => Math.round(valor * 100) / 100;
const cuotaDe = (base) => aCentimos((base * TIPO_TOTAL) / 100);

// Cuotas posibles en 2026: la de la base mínima del primer tramo y la de la base máxima del último.
export const CUOTA_MINIMA_2026 = cuotaDe(TRAMOS_CUOTA_2026[0].baseMinima);
export const CUOTA_MAXIMA_2026 = cuotaDe(TRAMOS_CUOTA_2026[TRAMOS_CUOTA_2026.length - 1].baseMaxima);

// ingresos y gastos: del año, sin IVA y sin las cuotas. cuotaMensual: la que has pagado cada mes.
// meses: meses de alta en 2026 (de 1 a 12).
export function calcularRegularizacion({ ingresos, gastos, cuotaMensual, meses, modalidad, cumpleRequisitosArt32 }) {
  const cuotasPagadas = aCentimos(cuotaMensual * meses);
  // Rendimiento neto del IRPF de 2026: en simplificada se restan los gastos de difícil justificación,
  // que en 2026 son el 10 % con un máximo de 3.000 € (Real Decreto-ley 43/2026).
  const previo = ingresos - gastos - cuotasPagadas;
  const { porcentajeGastosDificilJustificacion: porcentaje, limiteGastosDificilJustificacion: limite } = TABLAS[2026];
  const aplicaDificil = modalidad === "directa_simplificada" && !cumpleRequisitosArt32;
  const dificil = aplicaDificil && previo > 0 ? Math.min((previo * porcentaje) / 100, limite) : 0;
  const rendimientoNeto = previo - dificil;
  // Rendimiento computable (art. 308.1.c, regla 1.ª): el neto más las cuotas pagadas; después, el 7 %
  // de gastos genéricos (regla 2.ª), y se reparte entre los meses de alta (regla 3.ª).
  const computable = rendimientoNeto + cuotasPagadas;
  const deduccion = Math.max((computable * DEDUCCION_GASTOS_GENERICOS) / 100, 0);
  const mensual = Math.max((computable - deduccion) / meses, 0);
  const tramo = buscarTramo(mensual);
  const cuotaMinima = cuotaDe(tramo.baseMinima);
  const cuotaMaxima = cuotaDe(tramo.baseMaxima);
  // Regla 4.ª: diferencia con la cuota mínima o con la máxima del tramo, en cada mes de alta.
  let resultado = "nada";
  let diferenciaMensual = 0;
  if (cuotaMensual < cuotaMinima) {
    resultado = "pagar";
    diferenciaMensual = aCentimos(cuotaMinima - cuotaMensual);
  } else if (cuotaMensual > cuotaMaxima) {
    resultado = "devolver";
    diferenciaMensual = aCentimos(cuotaMensual - cuotaMaxima);
  }
  return {
    resultado,
    importe: aCentimos(diferenciaMensual * meses),
    diferenciaMensual,
    cuotasPagadas,
    gastosDificil: aCentimos(dificil),
    rendimientoNeto: aCentimos(rendimientoNeto),
    rendimientoComputable: aCentimos(computable),
    deduccion: aCentimos(deduccion),
    rendimientoMensual: aCentimos(mensual),
    tabla: tramo.tabla,
    tramo: tramo.numero,
    baseMinima: tramo.baseMinima,
    baseMaxima: tramo.baseMaxima,
    cuotaMinima,
    cuotaMaxima,
  };
}
