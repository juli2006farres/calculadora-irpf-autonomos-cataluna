// Cotización de los autónomos (RETA) en 2026. Es igual en toda España.
// Fuente: art. 18 y art. 37 de la Orden PJC/297/2026 (BOE-A-2026-7296).
export const TRAMOS_CUOTA_2026 = [
    { tabla: "reducida", numero: 1, hasta: 670, incluyeLimite: true, baseMinima: 653.59, baseMaxima: 718.94 },
    { tabla: "reducida", numero: 2, hasta: 900, incluyeLimite: true, baseMinima: 718.95, baseMaxima: 900 },
    { tabla: "reducida", numero: 3, hasta: 1_166.7, incluyeLimite: false, baseMinima: 849.67, baseMaxima: 1_166.7 },
    { tabla: "general", numero: 1, hasta: 1_300, incluyeLimite: true, baseMinima: 950.98, baseMaxima: 1_300 },
    { tabla: "general", numero: 2, hasta: 1_500, incluyeLimite: true, baseMinima: 960.78, baseMaxima: 1_500 },
    { tabla: "general", numero: 3, hasta: 1_700, incluyeLimite: true, baseMinima: 960.78, baseMaxima: 1_700 },
    { tabla: "general", numero: 4, hasta: 1_850, incluyeLimite: true, baseMinima: 1_143.79, baseMaxima: 1_850 },
    { tabla: "general", numero: 5, hasta: 2_030, incluyeLimite: true, baseMinima: 1_209.15, baseMaxima: 2_030 },
    { tabla: "general", numero: 6, hasta: 2_330, incluyeLimite: true, baseMinima: 1_274.51, baseMaxima: 2_330 },
    { tabla: "general", numero: 7, hasta: 2_760, incluyeLimite: true, baseMinima: 1_356.21, baseMaxima: 2_760 },
    { tabla: "general", numero: 8, hasta: 3_190, incluyeLimite: true, baseMinima: 1_437.91, baseMaxima: 3_190 },
    { tabla: "general", numero: 9, hasta: 3_620, incluyeLimite: true, baseMinima: 1_519.61, baseMaxima: 3_620 },
    { tabla: "general", numero: 10, hasta: 4_050, incluyeLimite: true, baseMinima: 1_601.31, baseMaxima: 4_050 },
    { tabla: "general", numero: 11, hasta: 6_000, incluyeLimite: true, baseMinima: 1_732.03, baseMaxima: 5_101.2 },
    { tabla: "general", numero: 12, hasta: Number.POSITIVE_INFINITY, incluyeLimite: true, baseMinima: 1_928.1, baseMaxima: 5_101.2 },
];
// Tipos de cotización en porcentaje. Suman el 31,5 %.
export const TIPOS_CUOTA_2026 = {
    contingencias_comunes: 28.3,
    contingencias_profesionales: 1.3,
    cese_de_actividad: 0.9,
    formacion_profesional: 0.1,
    mecanismo_equidad_intergeneracional: 0.9,
};
// Deducción por gastos genéricos del art. 308 LGSS para el autónomo persona física.
export const DEDUCCION_GASTOS_GENERICOS = 7;
export const EJERCICIOS_CUOTA = [2026];
export const FECHA_REVISION_CUOTA = "2026-11-16";
export const FUENTES_CUOTA = [
    "Orden PJC/297/2026, arts. 18 y 37 (bases y tipos del RETA en 2026): https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-7296",
    "Ley General de la Seguridad Social, art. 308 (rendimientos computables y deducción del 7 %): https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724",
];
//# sourceMappingURL=tablas.js.map