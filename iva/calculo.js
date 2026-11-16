// Añadir o quitar el IVA de un precio. Tipos: art. 90 y 91 de la Ley del IVA.
export const TIPOS_IVA_PRECIO = [21, 10, 4];

const aCentimos = (valor) => Math.round(valor * 100) / 100;

// modo "anadir": el importe es la base (sin IVA). modo "quitar": el importe ya lleva el IVA.
// Al quitar, el IVA se obtiene por diferencia para que base + IVA sume exactamente el precio.
export function calcularIva({ importe, modo, tipo }) {
  if (modo === "quitar") {
    const total = aCentimos(importe);
    const base = aCentimos(total / (1 + tipo / 100));
    return { base, iva: aCentimos(total - base), total };
  }
  const base = aCentimos(importe);
  const iva = aCentimos((base * tipo) / 100);
  return { base, iva, total: aCentimos(base + iva) };
}
