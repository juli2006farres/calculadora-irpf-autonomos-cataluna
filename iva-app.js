// Calculadora de IVA: añadir o quitar el IVA de un precio.
import { calcularIva, TIPOS_IVA_PRECIO } from "./iva/calculo.js";
import { idioma, euros, importe, fila, tabla, total, mostrar, error, conectar, elemento } from "./comun.js";

const TEXTOS = {
  es: {
    error: "Revisa el precio: debe ser un número positivo.",
    ayuda: { anadir: "Precio sin IVA.", quitar: "Precio con el IVA ya incluido." },
    total: { anadir: "Precio con IVA", quitar: "Precio sin IVA (base imponible)" },
    nota: { anadir: (iva) => `Incluye ${iva} de IVA`, quitar: (iva) => `El precio incluía ${iva} de IVA` },
    base: "Base imponible",
    iva: (tipo) => `IVA (${tipo} %)`,
    totalFila: "Total con IVA",
    comparar: "Con los otros tipos de IVA",
    cabecera: ["Tipo", "Base", "IVA", "Total"],
  },
  ca: {
    error: "Revisa el preu: ha de ser un nombre positiu.",
    ayuda: { anadir: "Preu sense IVA.", quitar: "Preu amb l'IVA ja inclòs." },
    total: { anadir: "Preu amb IVA", quitar: "Preu sense IVA (base imposable)" },
    nota: { anadir: (iva) => `Inclou ${iva} d'IVA`, quitar: (iva) => `El preu incloïa ${iva} d'IVA` },
    base: "Base imposable",
    iva: (tipo) => `IVA (${tipo} %)`,
    totalFila: "Total amb IVA",
    comparar: "Amb els altres tipus d'IVA",
    cabecera: ["Tipus", "Base", "IVA", "Total"],
  },
};
const t = TEXTOS[idioma];
const resultado = document.getElementById("resultado");

function calcular() {
  const modo = document.querySelector('input[name="modo"]:checked').value;
  document.getElementById("ayuda-importe").textContent = t.ayuda[modo];
  const precio = importe("importe");
  if (precio === null) return mostrar(resultado, error(t.error));
  const tipo = Number(document.getElementById("tipo").value);
  const r = calcularIva({ importe: precio, modo, tipo });
  const cifra = modo === "anadir" ? r.total : r.base;
  const otros = TIPOS_IVA_PRECIO.filter((x) => x !== tipo).map((x) => {
    const o = calcularIva({ importe: precio, modo, tipo: x });
    return fila([`${x} %`, euros.format(o.base), euros.format(o.iva), euros.format(o.total)]);
  });
  mostrar(
    resultado,
    total(t.total[modo], euros.format(cifra), t.nota[modo](euros.format(r.iva))),
    tabla([
      fila([t.base, euros.format(r.base)]),
      fila([t.iva(tipo), `+ ${euros.format(r.iva)}`]),
      fila([t.totalFila, euros.format(r.total)], true),
    ]),
    elemento("p", t.comparar, "nota"),
    tabla(otros, t.cabecera),
  );
}

conectar(calcular);
