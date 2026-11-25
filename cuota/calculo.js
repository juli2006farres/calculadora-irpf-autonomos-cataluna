import { TABLAS } from "../irpf/tablas.js";
import { DEDUCCION_GASTOS_GENERICOS, TIPOS_CUOTA_2026, TRAMOS_CUOTA_2026 } from "./tablas.js";
const aCentimos = (valor) => Math.round(valor * 100) / 100;
export const TIPO_TOTAL = Object.values(TIPOS_CUOTA_2026).reduce((suma, tipo) => suma + tipo, 0);
// Busca el tramo por el rendimiento mensual. Se compara en céntimos para que
// 1.166,70 caiga en el tramo correcto sin errores de redondeo.
export function buscarTramo(rendimientoMensual) {
    const centimos = Math.round(rendimientoMensual * 100);
    for (const tramo of TRAMOS_CUOTA_2026) {
        const limite = Math.round(tramo.hasta * 100);
        if (tramo.incluyeLimite ? centimos <= limite : centimos < limite)
            return tramo;
    }
    return TRAMOS_CUOTA_2026[TRAMOS_CUOTA_2026.length - 1];
}
const cuotaDe = (base) => aCentimos((base * TIPO_TOTAL) / 100);
// Las cuotas son de 2026: los rendimientos se calculan con las reglas del IRPF de 2026.
const DIFICIL = TABLAS[2026];
// El rendimiento que cuenta para la cuota es el rendimiento neto fiscal más las propias
// cuotas (art. 308 LGSS), así que no depende de ellas, salvo por un detalle: en estimación
// directa simplificada, los gastos de difícil justificación (en 2026, 10 % con un máximo de 3.000 €,
// los mismos del IRPF de ese año) se calculan después de restar las cuotas. Por eso se repite el
// cálculo hasta que la cuota no cambia.
export function calcularCuota(entrada) {
    const aplicaDificil = entrada.modalidad === "directa_simplificada" && !entrada.cumpleRequisitosArt32;
    let cuotaAnual = 0;
    let computable = 0;
    let tramo = TRAMOS_CUOTA_2026[0];
    for (let vuelta = 0; vuelta < 20; vuelta++) {
        const previo = entrada.ingresos - entrada.gastos - cuotaAnual;
        const dificil = aplicaDificil && previo > 0 ? Math.min((previo * DIFICIL.porcentajeGastosDificilJustificacion) / 100, DIFICIL.limiteGastosDificilJustificacion) : 0;
        computable = entrada.ingresos - entrada.gastos - dificil;
        const mensual = Math.max((computable * (100 - DEDUCCION_GASTOS_GENERICOS)) / 100 / 12, 0);
        tramo = buscarTramo(mensual);
        const nueva = cuotaDe(tramo.baseMinima) * 12;
        if (nueva === cuotaAnual)
            break;
        cuotaAnual = nueva;
    }
    const deduccion = Math.max((computable * DEDUCCION_GASTOS_GENERICOS) / 100, 0);
    return {
        rendimiento_computable_anual: aCentimos(computable),
        deduccion_gastos_genericos: aCentimos(deduccion),
        rendimiento_mensual: aCentimos(Math.max((computable - deduccion) / 12, 0)),
        tabla: tramo.tabla,
        tramo: tramo.numero,
        base_minima: tramo.baseMinima,
        base_maxima: tramo.baseMaxima,
        tipo_total_porcentaje: aCentimos(TIPO_TOTAL),
        cuota_mensual_minima: cuotaDe(tramo.baseMinima),
        cuota_mensual_maxima: cuotaDe(tramo.baseMaxima),
        cuota_anual_minima: aCentimos(cuotaDe(tramo.baseMinima) * 12),
    };
}
//# sourceMappingURL=calculo.js.map