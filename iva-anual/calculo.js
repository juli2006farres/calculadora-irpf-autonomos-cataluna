// IVA anual en 2027: régimen especial de declaración anual para pequeños empresarios y profesionales.
// Reglas del Real Decreto-ley 43/2026 (BOE del 25-11-2026), con efectos desde el 1 de enero de 2027:
// - Arts. 163 novovicies a duotricies de la Ley del IVA: pueden optar las personas físicas (y las
//   entidades en atribución de rentas con todos los socios personas físicas) cuyo volumen de operaciones
//   del año anterior no haya superado 85.000 € (elevado al año si empezaron ese año). Quien empieza la
//   actividad en el año puede optar ese mismo año. No pueden optar quienes estén en el régimen
//   simplificado, el grupo de entidades, el criterio de caja, la cuenta corriente tributaria o el periodo
//   mensual (salvo si es solo por la devolución mensual del art. 30 del Reglamento).
// - Una sola declaración al año y tres pagos a cuenta en abril, julio y octubre. Cada pago es la cuarta
//   parte de la cuota del año anterior; el primer año, la suma de las cuotas de los modelos 303 del año
//   anterior. Si esa cuota no es positiva, o si se empieza la actividad, el pago es cero.
// - Disposición transitoria séptima del Reglamento del IVA: para 2027 se opta en marzo de 2027, y en esa
//   opción se puede renunciar a los regímenes incompatibles (por ejemplo, al criterio de caja).
// - Art. 61 octodecies del Reglamento: los pagos se cargan por domiciliación el 20 de abril, el 20 de
//   julio y el 20 de octubre. Art. 71.4: la declaración del único periodo del año, del 1 al 30 de enero.

export const LIMITE_VOLUMEN = 85_000;
export const DIAS_2026 = 365;

// Redondeo al céntimo, con los medios céntimos hacia arriba (lejos del cero). toPrecision(15) quita el
// ruido de los decimales del ordenador: 4.518,315 × 100 da 451.831,49999… y debe redondear a 4.518,32.
const aCentimos = (valor) => {
  const r = Math.round(Math.abs(Number((valor * 100).toPrecision(15)))) / 100;
  return valor < 0 && r !== 0 ? -r : r;
};

// Días de actividad en 2026 desde la fecha de inicio (AAAA-MM-DD), contando ese día y el 31 de diciembre.
export function diasActividad2026(fechaInicio) {
  const m = /^2026-(\d{2})-(\d{2})$/.exec(fechaInicio ?? "");
  if (!m) return null;
  const inicio = Date.UTC(2026, Number(m[1]) - 1, Number(m[2]));
  const comprobada = new Date(inicio);
  if (comprobada.getUTCMonth() !== Number(m[1]) - 1 || comprobada.getUTCDate() !== Number(m[2])) return null;
  return Math.round((Date.UTC(2026, 11, 31) - inicio) / 86_400_000) + 1;
}

// titular: "persona" (autónomo persona física), "atribucion_fisicas" (comunidad de bienes o sociedad civil
// con todos los socios personas físicas) o "sociedad". inicio: "antes" (antes de 2026), "2026" (con
// fechaInicio) o "2027". volumen: lo facturado en 2026 sin IVA. regimen: "general", "criterio_caja",
// "redeme_voluntario" (devolución mensual del art. 30), "simplificado" o "recargo".
// ivaRepercutido e ivaSoportado: el IVA de 2026 de los modelos 303 (cobrado y deducible).
// ivaPrevisto2027: el IVA a pagar que esperas en 2027 (opcional; si no, el mismo que en 2026).
export function calcularIvaAnual2027({
  titular,
  inicio,
  fechaInicio,
  volumen,
  regimen,
  ivaRepercutido,
  ivaSoportado,
  ivaPrevisto2027 = null,
}) {
  if (titular === "sociedad") return { caso: "sociedad" };
  if (regimen === "recargo") return { caso: "recargo" };

  let dias = DIAS_2026;
  if (inicio === "2026") {
    dias = diasActividad2026(fechaInicio);
    if (dias === null) return { caso: "fecha_invalida" };
  }
  const volumenAnual = inicio === "2027" ? 0 : aCentimos((volumen * DIAS_2026) / dias);
  if (volumenAnual > LIMITE_VOLUMEN) {
    return { caso: "supera", volumenAnual, elevado: inicio === "2026", dias };
  }

  // Cuota de referencia: el IVA de 2026 (cobrado menos deducible), como la suma de los modelos 303.
  const cuotaReferencia = inicio === "2027" ? 0 : aCentimos(ivaRepercutido - ivaSoportado);
  const pagoACuenta = cuotaReferencia > 0 ? aCentimos(cuotaReferencia / 4) : 0;
  const previsto = inicio === "2027" ? ivaPrevisto2027 : (ivaPrevisto2027 ?? cuotaReferencia);
  const enero = previsto === null ? null : aCentimos(previsto - 3 * pagoACuenta);

  return {
    caso: "puede",
    regimen,
    inicio,
    volumenAnual,
    elevado: inicio === "2026",
    dias,
    cuotaReferencia,
    pagoACuenta,
    previsto,
    enero,
  };
}
