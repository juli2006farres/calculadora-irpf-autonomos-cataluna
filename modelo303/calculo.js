// Modelo 303: autoliquidación trimestral del IVA en régimen general, simplificada para un autónomo
// que tributa solo ante la Administración del Estado (casilla 65 = 100 %), sin prorrata, recargo de
// equivalencia, criterio de caja ni operaciones intracomunitarias. Casillas según las instrucciones
// del modelo de la AEAT: 46 = 27 − 45; 69 = 66 + 77 − 78 + 68 + 108; 71 = 69 − 70 + 109.
// La web de calculadoras usa una copia de la compilación de este archivo.
export const TIPOS_IVA_303 = [21, 10, 4];
export const FECHA_REVISION_MODELO303 = "2026-11-18";
export const FUENTES_MODELO303 = [
    "Instrucciones del modelo 303 (AEAT): https://sede.agenciatributaria.gob.es/Sede/todas-gestiones/impuestos-tasas/iva/modelo-303-iva-autoliquidacion_/instrucciones-2025.html",
    "Ley 37/1992 del IVA, artículos 90 y 91 (BOE): https://www.boe.es/buscar/act.php?id=BOE-A-1992-28740#a90",
];
const aCentimos = (valor) => Math.round(valor * 100) / 100;
function cuotas(bases) {
    return TIPOS_IVA_303.map((tipo) => ({ tipo, base: aCentimos(bases[tipo]), cuota: aCentimos((bases[tipo] * tipo) / 100) }));
}
export function calcularModelo303(entrada) {
    const repercutido = cuotas(entrada.ventas);
    const soportado = cuotas(entrada.gastos);
    const c27 = aCentimos(repercutido.reduce((s, x) => s + x.cuota, 0));
    const c45 = aCentimos(soportado.reduce((s, x) => s + x.cuota, 0));
    const c46 = aCentimos(c27 - c45);
    const c66 = c46; // un solo territorio: el 100 % del resultado
    const c110 = aCentimos(entrada.compensarAnteriores);
    // Se aplica la cuantía máxima posible de lo pendiente, sin pasar del resultado positivo.
    const c78 = c66 > 0 ? aCentimos(Math.min(c110, c66)) : 0;
    const c87 = aCentimos(c110 - c78);
    const c71 = aCentimos(c66 - c78);
    let situacion;
    if (c71 > 0)
        situacion = "a_ingresar";
    else if (c71 === 0)
        situacion = "resultado_cero";
    else
        situacion = entrada.trimestre === 4 ? "a_devolver_o_compensar" : "a_compensar";
    const negativo = c71 < 0 ? -c71 : 0;
    return {
        iva_repercutido: repercutido,
        iva_soportado: soportado,
        casilla_27: c27,
        casilla_45: c45,
        casilla_46: c46,
        casilla_110: c110,
        casilla_78: c78,
        casilla_87: c87,
        casilla_71: c71,
        situacion,
        importe: Math.abs(c71),
        pendiente_para_siguientes: aCentimos(c87 + (situacion === "a_compensar" ? negativo : 0)),
    };
}
//# sourceMappingURL=calculo.js.map