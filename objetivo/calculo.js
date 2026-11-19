// Cuánto facturar para ganar un neto concreto: la calculadora de sueldo neto al revés.
import { calcularSueldoNeto } from "../sueldo/calculo.js";

const aCentimos = (valor) => Math.round(valor * 100) / 100;
const MAXIMO = 10_000_000;

// Busca por bisección la facturación anual (sin IVA) con la que queda `netoMensual` en 12 pagas.
// El neto crece con la facturación salvo pequeños saltos al cambiar de tramo de cuota, así que
// el resultado es una facturación con la que se alcanza el objetivo, redondeada al céntimo.
// Devuelve null si el objetivo no se alcanza ni con la facturación máxima admitida.
export function facturacionParaNeto({ netoMensual, gastos, modalidad, cumpleRequisitosArt32, inicioActividad, comunidad = "cataluna" }) {
  const objetivo = netoMensual * 12;
  const neto = (ingresos) =>
    calcularSueldoNeto({ ingresos, gastos, cuotaMensual: null, modalidad, cumpleRequisitosArt32, inicioActividad, comunidad }).netoAnual;
  if (neto(MAXIMO) < objetivo) return null;
  let bajo = gastos;
  let alto = Math.max(gastos + objetivo * 2 + 10_000, 1);
  while (neto(alto) < objetivo) alto = Math.min(alto * 2, MAXIMO);
  for (let i = 0; i < 80 && alto - bajo > 0.005; i++) {
    const medio = (bajo + alto) / 2;
    if (neto(medio) >= objetivo) alto = medio;
    else bajo = medio;
  }
  // Redondea hacia arriba al céntimo para no quedarse por debajo del objetivo.
  let ingresos = Math.ceil(alto * 100) / 100;
  while (neto(ingresos) < objetivo) ingresos = aCentimos(ingresos + 0.01);
  const detalle = calcularSueldoNeto({ ingresos, gastos, cuotaMensual: null, modalidad, cumpleRequisitosArt32, inicioActividad, comunidad });
  return { ingresos, ...detalle };
}
