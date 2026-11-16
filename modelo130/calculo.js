// Modelo 130: pago fraccionado del IRPF en estimación directa (art. 110 del Reglamento del IRPF
// y las instrucciones del modelo de la AEAT). Cada trimestre se calcula sobre lo acumulado desde
// el 1 de enero, restando lo ya ingresado en los trimestres anteriores.
// La web de calculadoras usa una copia de la compilación de este archivo.
export const PORCENTAJE_PAGO = 20;
export const PORCENTAJE_DIFICIL = 5;
export const LIMITE_DIFICIL = 2000;
export const FECHA_REVISION_MODELO130 = "2026-11-17";
export const FUENTES_MODELO130 = [
    "Reglamento del IRPF, artículos 109 y 110 (BOE): https://www.boe.es/buscar/act.php?id=BOE-A-2007-6820#a110",
    "Instrucciones del modelo 130 (AEAT): https://sede.agenciatributaria.gob.es/Sede/impuestos-tasas/impuesto-sobre-renta-personas-fisicas/modelo-130-irpf______esionales-estimacion-directa-fraccionado_/instrucciones.html",
];
const aCentimos = (valor) => Math.round(valor * 100) / 100;
// Minoración del art. 110.3.c según el rendimiento neto de actividades del año anterior.
// Devuelve el importe por trimestre. null significa "más de 12.000 € o no aplica".
export function minoracionPorRendimiento(rendimientoAnterior) {
    if (rendimientoAnterior === null || rendimientoAnterior === undefined)
        return 0;
    const centimos = Math.round(rendimientoAnterior * 100);
    if (centimos <= 900_000)
        return 100;
    if (centimos <= 1_000_000)
        return 75;
    if (centimos <= 1_100_000)
        return 50;
    if (centimos <= 1_200_000)
        return 25;
    return 0;
}
// trimestres: hasta cuatro, cada uno con lo de ese trimestre (no acumulado). Los gastos incluyen
// las cuotas de autónomo. En simplificada se suman los gastos de difícil justificación a la
// casilla 02, como indican las instrucciones de la AEAT.
export function calcularModelo130({ trimestres, modalidad, minoracion, }) {
    let ingresos = 0;
    let gastos = 0;
    let retenciones = 0;
    let positivosAnteriores = 0; // casilla 05: suma de las casillas 07 positivas anteriores
    let negativoPendiente = 0; // resultados negativos de la casilla 19 aún no deducidos
    return trimestres.map((t, indice) => {
        ingresos += t.ingresos;
        gastos += t.gastos;
        retenciones += t.retenciones;
        const previo = ingresos - gastos;
        const dificil = modalidad === "directa_simplificada" && previo > 0
            ? aCentimos(Math.min((previo * PORCENTAJE_DIFICIL) / 100, LIMITE_DIFICIL))
            : 0;
        const c01 = aCentimos(ingresos);
        const c02 = aCentimos(gastos + dificil);
        const c03 = aCentimos(c01 - c02);
        const c04 = c03 > 0 ? aCentimos((c03 * PORCENTAJE_PAGO) / 100) : 0;
        const c05 = aCentimos(positivosAnteriores);
        const c06 = aCentimos(retenciones);
        const c07 = aCentimos(c04 - c05 - c06);
        if (c07 > 0)
            positivosAnteriores += c07;
        const c12 = Math.max(c07, 0);
        const c13 = minoracion;
        const c14 = aCentimos(c12 - c13);
        const c15 = c14 > 0 ? aCentimos(Math.min(negativoPendiente, c14)) : 0;
        negativoPendiente = aCentimos(negativoPendiente - c15);
        const c19 = aCentimos(c14 - c15);
        // En el cuarto trimestre un resultado negativo ya no se puede trasladar.
        if (c19 < 0 && indice < 3)
            negativoPendiente = aCentimos(negativoPendiente - c19);
        return {
            trimestre: indice + 1,
            ingresos: c01,
            gastos: c02,
            dificil,
            rendimiento: c03,
            pago_bruto: c04,
            pagos_anteriores: c05,
            retenciones: c06,
            casilla_07: c07,
            minoracion: c13,
            negativos_anteriores: c15,
            resultado: c19,
            a_ingresar: Math.max(c19, 0),
        };
    });
}
//# sourceMappingURL=calculo.js.map