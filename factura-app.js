// Calculadora de factura con IVA y retención de IRPF.
import { calcularFactura } from "./factura/calculo.js";
import { idioma, euros, importe, fila, tabla, total, mostrar, error, conectar, elemento } from "./comun.js";

const TEXTOS = {
  es: {
    error: "Revisa el importe: debe ser un número positivo.",
    ayuda: { base: "El precio de tu trabajo, sin IVA.", cobrar: "Lo que quieres recibir en tu cuenta." },
    total: "Total de la factura (lo que cobras)",
    nota: (base) => `Base imponible: ${base}`,
    base: "Base imponible",
    iva: (tipo) => `IVA (${tipo} %)`,
    retencion: (tipo) => `Retención de IRPF (${tipo} %)`,
    totalFila: "Total a cobrar",
    explica: (iva, ret) =>
      `El IVA (${iva}) lo ingresas a Hacienda en el modelo 303. La retención (${ret}) la ingresa tu cliente a Hacienda como adelanto de tu IRPF.`,
    sinRet: (iva) => `El IVA (${iva}) lo ingresas a Hacienda en el modelo 303.`,
  },
  ca: {
    error: "Revisa l'import: ha de ser un nombre positiu.",
    ayuda: { base: "El preu de la teva feina, sense IVA.", cobrar: "El que vols rebre al teu compte." },
    total: "Total de la factura (el que cobres)",
    nota: (base) => `Base imposable: ${base}`,
    base: "Base imposable",
    iva: (tipo) => `IVA (${tipo} %)`,
    retencion: (tipo) => `Retenció d'IRPF (${tipo} %)`,
    totalFila: "Total a cobrar",
    explica: (iva, ret) =>
      `L'IVA (${iva}) l'ingresses a Hisenda amb el model 303. La retenció (${ret}) la ingressa el teu client a Hisenda com a avançament del teu IRPF.`,
    sinRet: (iva) => `L'IVA (${iva}) l'ingresses a Hisenda amb el model 303.`,
  },
};
const t = TEXTOS[idioma];
const resultado = document.getElementById("resultado");

function calcular() {
  const modo = document.querySelector('input[name="modo"]:checked').value;
  document.getElementById("ayuda-importe").textContent = t.ayuda[modo];
  const cantidad = importe("importe");
  if (cantidad === null) return mostrar(resultado, error(t.error));
  const tipoIva = Number(document.getElementById("iva").value);
  const tipoRetencion = Number(document.getElementById("retencion").value);
  const r = calcularFactura({ importe: cantidad, modo, tipoIva, tipoRetencion });
  const filas = [fila([t.base, euros.format(r.base)]), fila([t.iva(tipoIva), `+ ${euros.format(r.iva)}`])];
  if (tipoRetencion > 0) filas.push(fila([t.retencion(tipoRetencion), `− ${euros.format(r.retencion)}`]));
  filas.push(fila([t.totalFila, euros.format(r.total)], true));
  const explicacion =
    tipoRetencion > 0 ? t.explica(euros.format(r.iva), euros.format(r.retencion)) : t.sinRet(euros.format(r.iva));
  mostrar(
    resultado,
    total(t.total, euros.format(r.total), t.nota(euros.format(r.base))),
    tabla(filas),
    elemento("p", explicacion, "nota"),
  );
}

conectar(calcular);
