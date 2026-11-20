// Calcula los datos de las páginas de cada comunidad con los mismos módulos que usan las
// calculadoras (copias del servidor MCP), para que las tablas y los ejemplos coincidan siempre
// con lo que da la calculadora. Uso, desde la carpeta de la web:
//   node herramientas/datos_comunidades.mjs
// Escribe herramientas/datos_comunidades.json, que lee generar.py.
import { writeFileSync } from "node:fs";
import { COMUNIDADES, MINIMOS_AUTONOMICOS, TABLAS } from "../irpf/tablas.js";
import { calcularSueldoNeto } from "../sueldo/calculo.js";

// Ejemplos: autónomo en estimación directa simplificada, sin hijos, sin la reducción por
// inicio de actividad y pagando la cuota mínima de su tramo de 2026.
export const EJEMPLOS = [
  { ingresos: 20_000, gastos: 3_000 },
  { ingresos: 30_000, gastos: 4_000 },
  { ingresos: 40_000, gastos: 5_000 },
  { ingresos: 60_000, gastos: 8_000 },
];

const limite = (hasta) => (Number.isFinite(hasta) ? hasta : null);

// Tipo marginal conjunto: une los cortes de la escala estatal y de la autonómica.
function escalaConjunta(estatal, autonomica) {
  const cortes = [...new Set([...estatal, ...autonomica].map((t) => t.hasta))].sort((a, b) => a - b);
  const tipoEn = (escala, valor) => escala.find((t) => valor <= t.hasta).tipo;
  let desde = 0;
  return cortes.map((hasta) => {
    const punto = Number.isFinite(hasta) ? hasta : desde + 1;
    const fila = {
      desde,
      hasta: limite(hasta),
      estatal: tipoEn(estatal, punto),
      autonomico: tipoEn(autonomica, punto),
    };
    fila.total = Math.round((fila.estatal + fila.autonomico) * 100) / 100;
    desde = hasta;
    return fila;
  });
}

function calcular(comunidad, { ingresos, gastos }) {
  return calcularSueldoNeto({
    ingresos,
    gastos,
    cuotaMensual: null,
    modalidad: "directa_simplificada",
    cumpleRequisitosArt32: false,
    inicioActividad: false,
    comunidad,
  });
}

const t2026 = TABLAS[2026];
const t2025 = TABLAS[2025];
const resultados = EJEMPLOS.map((ejemplo) => {
  const filas = COMUNIDADES.map((c) => ({ c, r: calcular(c, ejemplo) }));
  const orden = [...filas].sort((a, b) => a.r.irpf - b.r.irpf || a.c.localeCompare(b.c));
  return { ejemplo, filas, orden };
});

const datos = {
  ejemplos: EJEMPLOS,
  escala_estatal: t2026.escalaEstatal.map((t) => ({ hasta: limite(t.hasta), tipo: t.tipo })),
  minimos_estatales: t2026.minimosEstatales,
  comunidades: {},
};
for (const c of COMUNIDADES) {
  const escala = t2026.escalasAutonomicas[c];
  const cambia2026 = JSON.stringify(escala) !== JSON.stringify(t2025.escalasAutonomicas[c]);
  datos.comunidades[c] = {
    escala_2026: escala.map((t) => ({ hasta: limite(t.hasta), tipo: t.tipo })),
    escala_2025: cambia2026 ? t2025.escalasAutonomicas[c].map((t) => ({ hasta: limite(t.hasta), tipo: t.tipo })) : null,
    tipo_minimo: escala[0].tipo,
    tipo_maximo: escala[escala.length - 1].tipo,
    marginal_conjunto: escalaConjunta(t2026.escalaEstatal, escala),
    minimos: MINIMOS_AUTONOMICOS[c],
    minimos_propios: MINIMOS_AUTONOMICOS[c] !== t2026.minimosEstatales,
    ejemplos: resultados.map(({ ejemplo, filas, orden }) => {
      const { r } = filas.find((f) => f.c === c);
      const puesto = orden.findIndex((f) => f.c === c) + 1;
      return {
        ...ejemplo,
        cuota_mensual: r.cuotaMensual,
        irpf: r.irpf,
        tipo_medio: r.tipoMedioIrpf,
        neto_anual: r.netoAnual,
        neto_mensual: r.netoMensual,
        puesto,
        mas_barata: orden[0].c,
        irpf_mas_barata: orden[0].r.irpf,
        mas_cara: orden[orden.length - 1].c,
        irpf_mas_cara: orden[orden.length - 1].r.irpf,
      };
    }),
  };
}

writeFileSync(new URL("./datos_comunidades.json", import.meta.url), JSON.stringify(datos, null, 1) + "\n");
console.log(`Datos de ${COMUNIDADES.length} comunidades y ${EJEMPLOS.length} ejemplos escritos.`);
