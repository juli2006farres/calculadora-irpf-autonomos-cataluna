// Datos fiscales públicos. Están aquí, y no en una API, porque Hacienda no ofrece
// ninguna API abierta con estos valores. Si cambia la ley, solo se toca este archivo.
// Art. 63 de la Ley 35/2006, texto consolidado del BOE.
const ESCALA_ESTATAL = [
    { hasta: 12_450, tipo: 9.5 },
    { hasta: 20_200, tipo: 12 },
    { hasta: 35_200, tipo: 15 },
    { hasta: 60_000, tipo: 18.5 },
    { hasta: 300_000, tipo: 22.5 },
    { hasta: Number.POSITIVE_INFINITY, tipo: 24.5 },
];
// Art. 611-1 del Código tributario de Cataluña, según el art. 3.1 del Decreto-ley 5/2025
// (texto oficial en el BOE: BOE-A-2025-10270).
const ESCALA_CATALUNA = [
    { hasta: 12_500, tipo: 9.5 },
    { hasta: 22_000, tipo: 12.5 },
    { hasta: 33_000, tipo: 16 },
    { hasta: 53_000, tipo: 19 },
    { hasta: 90_000, tipo: 21.5 },
    { hasta: 120_000, tipo: 23.5 },
    { hasta: 175_000, tipo: 24.5 },
    { hasta: Number.POSITIVE_INFINITY, tipo: 25.5 },
];
const TABLA_2025_2026 = {
    escalaEstatal: ESCALA_ESTATAL,
    escalaCataluna: ESCALA_CATALUNA,
    minimoContribuyente: 5_550, // art. 57 LIRPF
    minimoDescendientes: [2_400, 2_700, 4_000, 4_500], // art. 58.1 LIRPF
    incrementoMenor3: 2_800, // art. 58.2 LIRPF
    porcentajeGastosDificilJustificacion: 5, // AEAT; el 10 % de 2026 es solo para Ceuta
    limiteGastosDificilJustificacion: 2_000, // art. 30.2.4.ª LIRPF
};
// Solo hay ejercicios comprobados: pedir otro año es un error de validación.
export const EJERCICIOS = [2025, 2026];
export const TABLAS = {
    2025: TABLA_2025_2026,
    2026: TABLA_2025_2026,
};
export const FECHA_REVISION_TABLAS = "2026-11-04";
export const FUENTES_FISCALES = [
    "Ley 35/2006 del IRPF, arts. 30, 32, 57, 58 y 63: https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764",
    "AEAT, estimación directa simplificada: https://sede.agenciatributaria.gob.es/Sede/irpf/empresarios-individuales-profesionales/regimenes-determinar-rendimiento-actividad/estimacion-directa-simplificada.html",
    "Escala de Cataluña (art. 611-1 del Código tributario de Cataluña, según el art. 3.1 del Decreto-ley 5/2025): https://www.boe.es/diario_boe/txt.php?id=BOE-A-2025-10270",
    "AEAT, mínimo personal en Cataluña: https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025/c14-adecuacion-impuesto-circunstancias-personales/minimo-autonomico-personal-familiar/comunidad-autonoma-cataluna-importes-minimo-familiar.html",
];
//# sourceMappingURL=tablas.js.map