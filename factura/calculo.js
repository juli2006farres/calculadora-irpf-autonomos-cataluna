// Cálculo de una factura de autónomo: base imponible, IVA y retención de IRPF.
// Tipos de IVA: art. 90 y 91 de la Ley del IVA. Retención de profesionales:
// art. 95.1 del Reglamento del IRPF (15 % general y 7 % en el año de inicio y los dos siguientes).
// La web de calculadoras usa una copia de la compilación de este archivo.
export const TIPOS_IVA = [21, 10, 4, 0];
export const TIPOS_RETENCION = [15, 7, 0];
const aCentimos = (valor) => Math.round(valor * 100) / 100;
// modo "base": el importe es la base imponible (el precio sin IVA).
// modo "cobrar": el importe es lo que se quiere recibir, y se calcula la base.
export function calcularFactura({ importe, modo, tipoIva, tipoRetencion }) {
    const base = aCentimos(modo === "cobrar" ? importe / (1 + (tipoIva - tipoRetencion) / 100) : importe);
    const iva = aCentimos((base * tipoIva) / 100);
    const retencion = aCentimos((base * tipoRetencion) / 100);
    return { base, iva, retencion, total: aCentimos(base + iva - retencion) };
}
//# sourceMappingURL=calculo.js.map