// Modelo 130 en 2027: si hay que presentarlo, con qué porcentaje y si se puede elegir el pago domiciliado.
// Reglas del Real Decreto-ley 43/2026 (BOE del 25-11-2026), con efectos desde el 1 de enero de 2027:
// - Art. 101.11.a de la Ley del IRPF: pago fraccionado del 19 % si la cifra de negocios del periodo de
//   referencia es inferior a 250.000 € (o si en ese periodo no se ejercía la actividad); si no, el 20 %.
// - Art. 109.2 del Reglamento del IRPF: no hay que presentarlo si la cifra de negocios es inferior a
//   85.000 € y la cuota diferencial de ese periodo fue negativa e igual o mayor, en valor absoluto, que los
//   pagos fraccionados de ese periodo. Los profesionales con al menos el 70 % de ingresos con retención
//   en el año anterior siguen sin tener que presentarlo.
// - Art. 110.5 del Reglamento del IRPF: con cifra de negocios inferior a 250.000 € y cuota diferencial
//   negativa habiendo hecho pagos fraccionados, se puede optar por pagar cada trimestre el 25 % del
//   rendimiento neto del periodo de referencia por la suma de los tipos medios estatal y autonómico.
//   Para 2027 la opción se ejerce en marzo de 2027 (disposición transitoria vigésima segunda del Reglamento).
// El periodo de referencia de 2027 es el IRPF de 2025: es el último cuyo plazo de declaración (hasta el
// 30 de junio de 2026) acaba antes del primer pago fraccionado de 2027 (abril).

export const LIMITE_DISPENSA = 85_000;
export const LIMITE_19 = 250_000;
export const DIAS_2025 = 365;

// Redondeo al céntimo, con los medios céntimos hacia arriba (lejos del cero). toPrecision(15) quita el
// ruido de los decimales del ordenador: 4.518,315 × 100 da 451.831,49999… y debe redondear a 4.518,32.
const aCentimos = (valor) => {
  const r = Math.round(Math.abs(Number((valor * 100).toPrecision(15)))) / 100;
  return valor < 0 && r !== 0 ? -r : r;
};

// Días de actividad en 2025 desde la fecha de inicio (AAAA-MM-DD), contando ese día y el 31 de diciembre.
export function diasActividad2025(fechaInicio) {
  const m = /^2025-(\d{2})-(\d{2})$/.exec(fechaInicio ?? "");
  if (!m) return null;
  const inicio = Date.UTC(2025, Number(m[1]) - 1, Number(m[2]));
  const comprobada = new Date(inicio);
  if (comprobada.getUTCMonth() !== Number(m[1]) - 1 || comprobada.getUTCDate() !== Number(m[2])) return null;
  return Math.round((Date.UTC(2025, 11, 31) - inicio) / 86_400_000) + 1;
}

// metodo: "directa" (normal o simplificada), "objetiva" o "agraria".
// inicio: "antes" (antes de 2025), "2025" (empezó en 2025, con fechaInicio) o "despues" (en 2026 o 2027).
// cifraNegocios: ingresos de la actividad en 2025, sin IVA. cuotaDiferencial: la de la renta de 2025, en
// negativo si salió a devolver. pagosFraccionados: lo ingresado con el modelo 130 por 2025.
// rendimientoNeto, tipoMedioEstatal y tipoMedioAutonomico (en %): opcionales, para el pago domiciliado.
export function calcularModelo130En2027({
  metodo,
  inicio,
  fechaInicio,
  cifraNegocios,
  cuotaDiferencial,
  pagosFraccionados,
  profesionalRetenciones70,
  rendimientoNeto = null,
  tipoMedioEstatal = null,
  tipoMedioAutonomico = null,
}) {
  if (metodo === "objetiva" || metodo === "agraria") {
    return { caso: metodo };
  }
  // La regla del 70 % mira el año anterior (2026), así que vale también para quien empezó en 2026.
  if (profesionalRetenciones70) {
    return { caso: "retenciones_70" };
  }
  if (inicio === "despues") {
    // Sin actividad en 2025: la ley fija el 19 % (art. 101.11.a, tercer párrafo). Para la dispensa,
    // la norma no dice qué pasa si no hubo actividad en el periodo de referencia.
    return { caso: "sin_actividad_2025", porcentaje: 19 };
  }

  let dias = DIAS_2025;
  if (inicio === "2025") {
    dias = diasActividad2025(fechaInicio);
    if (dias === null) return { caso: "fecha_invalida" };
  }
  // Si empezó en 2025, la cifra de negocios se eleva al año (en proporción a los días de actividad).
  const cifraAnual = aCentimos((cifraNegocios * DIAS_2025) / dias);

  const aDevolver = cuotaDiferencial < 0;
  const cumpleCifraDispensa = cifraAnual < LIMITE_DISPENSA;
  const cubrePagos = aDevolver && -cuotaDiferencial >= pagosFraccionados;
  const dispensa = cumpleCifraDispensa && cubrePagos;
  const porcentaje = cifraAnual < LIMITE_19 ? 19 : 20;

  const puedeDomiciliar = !dispensa && cifraAnual < LIMITE_19 && aDevolver && pagosFraccionados > 0;
  let pagoDomiciliado = null;
  let tipoMedio = null;
  if (puedeDomiciliar && rendimientoNeto !== null && tipoMedioEstatal !== null && tipoMedioAutonomico !== null) {
    tipoMedio = aCentimos(tipoMedioEstatal + tipoMedioAutonomico);
    pagoDomiciliado = rendimientoNeto > 0 ? aCentimos((rendimientoNeto * tipoMedio) / 100 / 4) : 0;
  }

  return {
    caso: dispensa ? "dispensa" : "presenta",
    dispensa,
    porcentaje: dispensa ? null : porcentaje,
    cifraAnual,
    elevada: inicio === "2025",
    dias,
    cumpleCifraDispensa,
    aDevolver,
    cubrePagos,
    puedeDomiciliar,
    tipoMedio,
    pagoDomiciliado,
  };
}
