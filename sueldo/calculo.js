// Sueldo neto de un autónomo en 2026: lo que queda tras gastos, cuota e IRPF de su comunidad.
// Reutiliza los cálculos de la cuota y del IRPF, que son copias de los del servidor MCP.
import { calcularCuota } from "../cuota/calculo.js";
import { calcularIrpf } from "../irpf/calculo.js";

const aCentimos = (valor) => Math.round(valor * 100) / 100;

// cuotaMensual: null para usar la cuota mínima del tramo que corresponde.
export function calcularSueldoNeto({ ingresos, gastos, cuotaMensual, modalidad, cumpleRequisitosArt32, inicioActividad, comunidad = "cataluna" }) {
  const cuota = calcularCuota({ ingresos, gastos, modalidad, cumpleRequisitosArt32 });
  const cuotaAnual = cuotaMensual === null ? cuota.cuota_anual_minima : aCentimos(cuotaMensual * 12);
  const irpf = calcularIrpf({
    ejercicio: 2026,
    comunidad,
    ingresos,
    gastos,
    cuotasAutonomo: cuotaAnual,
    pagosACuenta: 0,
    modalidad,
    cumpleRequisitosArt32,
    inicioActividad,
    descendientesMenores25: 0,
    descendientesMenores3: 0,
    minimoDescendientesCompartido: false,
  });
  const netoAnual = aCentimos(ingresos - gastos - cuotaAnual - irpf.cuota_integra);
  return {
    netoAnual,
    netoMensual: aCentimos(netoAnual / 12),
    cuotaAnual,
    cuotaMensual: aCentimos(cuotaAnual / 12),
    irpf: irpf.cuota_integra,
    tipoMedioIrpf: irpf.tipo_medio_porcentaje,
    tramo: cuota.tramo,
    tabla: cuota.tabla,
    porCada100: ingresos > 0 ? aCentimos((netoAnual / ingresos) * 100) : 0,
  };
}
