// Datos fiscales públicos. Están aquí, y no en una API, porque Hacienda no ofrece
// ninguna API abierta con estos valores. Si cambia la ley, solo se toca este archivo.
// Comunidades de régimen común. El País Vasco y Navarra tienen su propio IRPF foral, y Ceuta
// y Melilla no tienen escala autonómica: quedan fuera para no dar un cálculo erróneo.
export const COMUNIDADES = [
    "andalucia",
    "aragon",
    "asturias",
    "baleares",
    "canarias",
    "cantabria",
    "castilla_la_mancha",
    "castilla_y_leon",
    "cataluna",
    "extremadura",
    "galicia",
    "la_rioja",
    "madrid",
    "murcia",
    "valenciana",
];
export const NOMBRES_COMUNIDADES = {
    andalucia: "Andalucía",
    aragon: "Aragón",
    asturias: "Principado de Asturias",
    baleares: "Illes Balears",
    canarias: "Canarias",
    cantabria: "Cantabria",
    castilla_la_mancha: "Castilla-La Mancha",
    castilla_y_leon: "Castilla y León",
    cataluna: "Cataluña",
    extremadura: "Extremadura",
    galicia: "Galicia",
    la_rioja: "La Rioja",
    madrid: "Comunidad de Madrid",
    murcia: "Región de Murcia",
    valenciana: "Comunitat Valenciana",
};
// Art. 63 de la Ley 35/2006, texto consolidado del BOE.
const ESCALA_ESTATAL = [
    { hasta: 12_450, tipo: 9.5 },
    { hasta: 20_200, tipo: 12 },
    { hasta: 35_200, tipo: 15 },
    { hasta: 60_000, tipo: 18.5 },
    { hasta: 300_000, tipo: 22.5 },
    { hasta: Number.POSITIVE_INFINITY, tipo: 24.5 },
];
// Arts. 57 y 58 de la Ley 35/2006.
const MINIMOS_ESTATALES = { contribuyente: 5_550, descendientes: [2_400, 2_700, 4_000, 4_500], menor3: 2_800 };
// Escalas autonómicas de 2025 según el Manual práctico de Renta 2025 de la AEAT (cap. 15,
// gravamen autonómico), generadas a partir de sus tablas comprobando las cuotas acumuladas.
// La de Cataluña coincide con el art. 611-1 del Código tributario de Cataluña (BOE-A-2025-10270).
const ESCALA_ANDALUCIA_2025 = [
    { hasta: 13_000, tipo: 9.5 },
    { hasta: 21_100, tipo: 12 },
    { hasta: 35_200, tipo: 15 },
    { hasta: 60_000, tipo: 18.5 },
    { hasta: Number.POSITIVE_INFINITY, tipo: 22.5 },
];
const ESCALA_ARAGON_2025 = [
    { hasta: 13_072.5, tipo: 9.5 },
    { hasta: 21_210, tipo: 12 },
    { hasta: 36_960, tipo: 15 },
    { hasta: 52_500, tipo: 18.5 },
    { hasta: 60_000, tipo: 20.5 },
    { hasta: 80_000, tipo: 23 },
    { hasta: 90_000, tipo: 24 },
    { hasta: 130_000, tipo: 25 },
    { hasta: Number.POSITIVE_INFINITY, tipo: 25.5 },
];
const ESCALA_ASTURIAS_2025 = [
    { hasta: 12_450, tipo: 9 },
    { hasta: 17_707.2, tipo: 12 },
    { hasta: 33_007.2, tipo: 14 },
    { hasta: 53_407.2, tipo: 19.2 },
    { hasta: 70_000, tipo: 21.5 },
    { hasta: 90_000, tipo: 22.5 },
    { hasta: 175_000, tipo: 25 },
    { hasta: Number.POSITIVE_INFINITY, tipo: 26 },
];
const ESCALA_BALEARES_2025 = [
    { hasta: 10_000, tipo: 9 },
    { hasta: 18_000, tipo: 11.25 },
    { hasta: 30_000, tipo: 14.25 },
    { hasta: 48_000, tipo: 17.5 },
    { hasta: 70_000, tipo: 19 },
    { hasta: 90_000, tipo: 21.75 },
    { hasta: 120_000, tipo: 22.75 },
    { hasta: 175_000, tipo: 23.75 },
    { hasta: Number.POSITIVE_INFINITY, tipo: 24.75 },
];
const ESCALA_CANARIAS_2025 = [
    { hasta: 13_748, tipo: 9 },
    { hasta: 19_422, tipo: 11.5 },
    { hasta: 35_924, tipo: 14 },
    { hasta: 57_566, tipo: 18.5 },
    { hasta: 93_268, tipo: 23.5 },
    { hasta: 123_745, tipo: 25 },
    { hasta: Number.POSITIVE_INFINITY, tipo: 26 },
];
const ESCALA_CANTABRIA_2025 = [
    { hasta: 13_000, tipo: 8.5 },
    { hasta: 21_000, tipo: 11 },
    { hasta: 35_200, tipo: 14.5 },
    { hasta: 60_000, tipo: 18 },
    { hasta: 90_000, tipo: 22.5 },
    { hasta: Number.POSITIVE_INFINITY, tipo: 24.5 },
];
const ESCALA_CASTILLA_LA_MANCHA_2025 = [
    { hasta: 12_450, tipo: 9.5 },
    { hasta: 20_200, tipo: 12 },
    { hasta: 35_200, tipo: 15 },
    { hasta: 60_000, tipo: 18.5 },
    { hasta: Number.POSITIVE_INFINITY, tipo: 22.5 },
];
const ESCALA_CASTILLA_Y_LEON_2025 = [
    { hasta: 12_450, tipo: 9 },
    { hasta: 20_200, tipo: 12 },
    { hasta: 35_200, tipo: 14 },
    { hasta: 53_407.2, tipo: 18.5 },
    { hasta: Number.POSITIVE_INFINITY, tipo: 21.5 },
];
const ESCALA_CATALUNA_2025 = [
    { hasta: 12_500, tipo: 9.5 },
    { hasta: 22_000, tipo: 12.5 },
    { hasta: 33_000, tipo: 16 },
    { hasta: 53_000, tipo: 19 },
    { hasta: 90_000, tipo: 21.5 },
    { hasta: 120_000, tipo: 23.5 },
    { hasta: 175_000, tipo: 24.5 },
    { hasta: Number.POSITIVE_INFINITY, tipo: 25.5 },
];
const ESCALA_EXTREMADURA_2025 = [
    { hasta: 12_450, tipo: 8 },
    { hasta: 20_200, tipo: 10 },
    { hasta: 24_200, tipo: 16 },
    { hasta: 35_200, tipo: 17.5 },
    { hasta: 60_000, tipo: 21 },
    { hasta: 80_200, tipo: 23.5 },
    { hasta: 99_200, tipo: 24 },
    { hasta: 120_200, tipo: 24.5 },
    { hasta: Number.POSITIVE_INFINITY, tipo: 25 },
];
const ESCALA_GALICIA_2025 = [
    { hasta: 12_985.35, tipo: 9 },
    { hasta: 21_068.6, tipo: 11.65 },
    { hasta: 35_200, tipo: 14.9 },
    { hasta: 60_000, tipo: 18.4 },
    { hasta: Number.POSITIVE_INFINITY, tipo: 22.5 },
];
const ESCALA_LA_RIOJA_2025 = [
    { hasta: 12_450, tipo: 8 },
    { hasta: 20_200, tipo: 10.6 },
    { hasta: 35_200, tipo: 13.6 },
    { hasta: 40_000, tipo: 17.8 },
    { hasta: 50_000, tipo: 18.3 },
    { hasta: 60_000, tipo: 19 },
    { hasta: 120_000, tipo: 24.5 },
    { hasta: Number.POSITIVE_INFINITY, tipo: 27 },
];
const ESCALA_MADRID_2025 = [
    { hasta: 13_362.22, tipo: 8.5 },
    { hasta: 19_004.63, tipo: 10.7 },
    { hasta: 35_425.68, tipo: 12.8 },
    { hasta: 57_320.4, tipo: 17.4 },
    { hasta: Number.POSITIVE_INFINITY, tipo: 20.5 },
];
const ESCALA_MURCIA_2025 = [
    { hasta: 12_450, tipo: 9.5 },
    { hasta: 20_200, tipo: 11.2 },
    { hasta: 34_000, tipo: 13.3 },
    { hasta: 60_000, tipo: 17.9 },
    { hasta: Number.POSITIVE_INFINITY, tipo: 22.5 },
];
const ESCALA_VALENCIANA_2025 = [
    { hasta: 12_000, tipo: 9 },
    { hasta: 22_000, tipo: 12 },
    { hasta: 32_000, tipo: 15 },
    { hasta: 42_000, tipo: 17.5 },
    { hasta: 52_000, tipo: 20 },
    { hasta: 62_000, tipo: 22.5 },
    { hasta: 72_000, tipo: 25 },
    { hasta: 100_000, tipo: 26.5 },
    { hasta: 150_000, tipo: 27.5 },
    { hasta: 200_000, tipo: 28.5 },
    { hasta: Number.POSITIVE_INFINITY, tipo: 29.5 },
];
const ESCALA_EXTREMADURA_2026 = [
    { hasta: 12_450, tipo: 7.75 },
    { hasta: 20_200, tipo: 9.75 },
    { hasta: 24_200, tipo: 16 },
    { hasta: 35_200, tipo: 17.5 },
    { hasta: 60_000, tipo: 21 },
    { hasta: 80_200, tipo: 23.5 },
    { hasta: 99_200, tipo: 24 },
    { hasta: 120_200, tipo: 24.5 },
    { hasta: Number.POSITIVE_INFINITY, tipo: 25 },
];
const ESCALA_VALENCIANA_2026 = [
    { hasta: 12_000, tipo: 8.8 },
    { hasta: 22_000, tipo: 11.7 },
    { hasta: 32_000, tipo: 14.6 },
    { hasta: 42_000, tipo: 17 },
    { hasta: 52_000, tipo: 19.4 },
    { hasta: 62_000, tipo: 21.9 },
    { hasta: 72_000, tipo: 24.4 },
    { hasta: 100_000, tipo: 26.1 },
    { hasta: 150_000, tipo: 27.35 },
    { hasta: 200_000, tipo: 28.35 },
    { hasta: Number.POSITIVE_INFINITY, tipo: 29.35 },
];
// En 2026 solo cambian Extremadura y la Comunitat Valenciana, según el informe de Hacienda
// "Tributación autonómica. Medidas 2026" (23-9-2026). Valencia: art. 18 de la Ley 5/2026
// (BOE-A-2026-19331). Extremadura: los dos primeros tipos pasan del 8 % y el 10 % al 7,75 % y el 9,75 %.
const ESCALAS_2025 = {
    andalucia: ESCALA_ANDALUCIA_2025,
    aragon: ESCALA_ARAGON_2025,
    asturias: ESCALA_ASTURIAS_2025,
    baleares: ESCALA_BALEARES_2025,
    canarias: ESCALA_CANARIAS_2025,
    cantabria: ESCALA_CANTABRIA_2025,
    castilla_la_mancha: ESCALA_CASTILLA_LA_MANCHA_2025,
    castilla_y_leon: ESCALA_CASTILLA_Y_LEON_2025,
    cataluna: ESCALA_CATALUNA_2025,
    extremadura: ESCALA_EXTREMADURA_2025,
    galicia: ESCALA_GALICIA_2025,
    la_rioja: ESCALA_LA_RIOJA_2025,
    madrid: ESCALA_MADRID_2025,
    murcia: ESCALA_MURCIA_2025,
    valenciana: ESCALA_VALENCIANA_2025,
};
const ESCALAS_2026 = {
    ...ESCALAS_2025,
    extremadura: ESCALA_EXTREMADURA_2026,
    valenciana: ESCALA_VALENCIANA_2026,
};
// Mínimo personal y familiar para el cálculo de la cuota autonómica (solo las partidas que usa
// este cálculo), según el cuadro del Manual práctico de Renta 2025 de la AEAT (cap. 14). El informe
// de Hacienda de 2026 no recoge cambios en estas partidas; las comunidades que no aparecen usan
// los importes estatales.
export const MINIMOS_AUTONOMICOS = {
    andalucia: { contribuyente: 5_790, descendientes: [2_510, 2_820, 4_170, 4_700], menor3: 2_920 },
    aragon: MINIMOS_ESTATALES,
    asturias: { contribuyente: 6_105, descendientes: [2_640, 2_970, 4_400, 4_950], menor3: 3_080 },
    baleares: { contribuyente: 5_550, descendientes: [2_400, 2_970, 4_400, 4_950], menor3: 2_800 },
    canarias: { contribuyente: 5_606, descendientes: [2_424, 2_727, 4_040, 4_545], menor3: 2_828 },
    cantabria: MINIMOS_ESTATALES,
    castilla_la_mancha: MINIMOS_ESTATALES,
    castilla_y_leon: MINIMOS_ESTATALES,
    cataluna: MINIMOS_ESTATALES,
    extremadura: MINIMOS_ESTATALES,
    galicia: { contribuyente: 5_789, descendientes: [2_503, 2_816, 4_172, 4_694], menor3: 2_920 },
    la_rioja: MINIMOS_ESTATALES,
    madrid: { contribuyente: 5_956.65, descendientes: [2_575.85, 2_897.83, 4_400, 4_950], menor3: 3_005.16 },
    murcia: MINIMOS_ESTATALES,
    valenciana: { contribuyente: 6_105, descendientes: [2_640, 2_970, 4_400, 4_950], menor3: 3_080 },
};
function tabla(escalasAutonomicas) {
    return {
        escalaEstatal: ESCALA_ESTATAL,
        minimosEstatales: MINIMOS_ESTATALES,
        escalasAutonomicas,
        porcentajeGastosDificilJustificacion: 5, // AEAT; el 10 % de 2026 es solo para Ceuta
        limiteGastosDificilJustificacion: 2_000, // art. 30.2.4.ª LIRPF
    };
}
// Solo hay ejercicios comprobados: pedir otro año es un error de validación.
export const EJERCICIOS = [2025, 2026];
export const TABLAS = {
    2025: tabla(ESCALAS_2025),
    2026: tabla(ESCALAS_2026),
};
export const FECHA_REVISION_TABLAS = "2026-11-19";
export const FUENTES_FISCALES = [
    "Ley 35/2006 del IRPF, arts. 30, 32, 57, 58 y 63: https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764",
    "AEAT, estimación directa simplificada: https://sede.agenciatributaria.gob.es/Sede/irpf/empresarios-individuales-profesionales/regimenes-determinar-rendimiento-actividad/estimacion-directa-simplificada.html",
    "AEAT, escalas autonómicas (Manual de Renta 2025): https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025/c15-calculo-impuesto-determinacion-cuotas-integras/gravamen-base-liquidable-general/gravamen-autonomico.html",
    "AEAT, mínimos autonómicos (Manual de Renta 2025): https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025/c14-adecuacion-impuesto-circunstancias-personales/minimo-autonomico-personal-familiar/cuadro-minimos-personales-familiares-estatal-autonomicos.html",
    "Hacienda, Tributación autonómica. Medidas 2026: https://www.hacienda.gob.es/sgfal/financiacionterritorial/autonomica/capitulo-i-tributacion-autonomica-2026.pdf",
    "Comunitat Valenciana, Ley 5/2026, art. 18 (BOE): https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-19331",
    "Escala de Cataluña (Decreto-ley 5/2025, BOE): https://www.boe.es/diario_boe/txt.php?id=BOE-A-2025-10270",
];
//# sourceMappingURL=tablas.js.map