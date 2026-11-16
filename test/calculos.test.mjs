import { test } from "node:test";
import assert from "node:assert/strict";
import { calcularFactura } from "../factura/calculo.js";
import { calcularModelo130, minoracionPorRendimiento } from "../modelo130/calculo.js";
import { calcularSueldoNeto } from "../sueldo/calculo.js";

test("factura desde la base: 1.000 € con IVA 21 % y retención 15 %", () => {
  assert.deepEqual(calcularFactura({ importe: 1000, modo: "base", tipoIva: 21, tipoRetencion: 15 }), {
    base: 1000, iva: 210, retencion: 150, total: 1060,
  });
});

test("factura a partir de lo que quieres cobrar", () => {
  const r = calcularFactura({ importe: 1060, modo: "cobrar", tipoIva: 21, tipoRetencion: 15 });
  assert.equal(r.base, 1000);
  assert.equal(r.total, 1060);
  const nuevo = calcularFactura({ importe: 500, modo: "cobrar", tipoIva: 21, tipoRetencion: 7 });
  assert.ok(Math.abs(nuevo.total - 500) <= 0.01);
});

test("factura a particular sin retención", () => {
  assert.equal(calcularFactura({ importe: 100, modo: "base", tipoIva: 21, tipoRetencion: 0 }).total, 121);
});

test("minoración del art. 110.3.c en sus límites", () => {
  assert.equal(minoracionPorRendimiento(null), 0);
  assert.equal(minoracionPorRendimiento(-500), 100);
  assert.equal(minoracionPorRendimiento(9000), 100);
  assert.equal(minoracionPorRendimiento(9000.01), 75);
  assert.equal(minoracionPorRendimiento(10000), 75);
  assert.equal(minoracionPorRendimiento(11000), 50);
  assert.equal(minoracionPorRendimiento(12000), 25);
  assert.equal(minoracionPorRendimiento(12000.01), 0);
});

test("modelo 130 acumulado en simplificada sin retenciones", () => {
  const t = { ingresos: 10000, gastos: 2000, retenciones: 0 };
  const r = calcularModelo130({ trimestres: [t, t, t, t], modalidad: "directa_simplificada", minoracion: 0 });
  // T1: 8.000 − 5 % = 7.600 → 1.520. T2: 16.000 − 800 = 15.200 → 3.040 − 1.520.
  assert.equal(r[0].a_ingresar, 1520);
  assert.equal(r[1].pagos_anteriores, 1520);
  assert.equal(r[1].a_ingresar, 1520);
  // T3: 24.000 − 1.200 = 22.800 → 4.560 − 3.040. T4: 32.000 − 1.600 = 30.400 → 6.080 − 4.560.
  assert.equal(r[2].a_ingresar, 1520);
  assert.equal(r[3].a_ingresar, 1520);
});

test("modelo 130: el límite de 2.000 € de difícil justificación es anual", () => {
  const t = { ingresos: 20000, gastos: 0, retenciones: 0 };
  const r = calcularModelo130({ trimestres: [t, t, t], modalidad: "directa_simplificada", minoracion: 0 });
  assert.equal(r[0].dificil, 1000);
  assert.equal(r[1].dificil, 2000);
  assert.equal(r[2].dificil, 2000);
  assert.equal(calcularModelo130({ trimestres: [t], modalidad: "directa_normal", minoracion: 0 })[0].dificil, 0);
});

test("modelo 130 de un profesional con retenciones", () => {
  const t = { ingresos: 10000, gastos: 2000, retenciones: 1500 };
  const r = calcularModelo130({ trimestres: [t, t], modalidad: "directa_simplificada", minoracion: 0 });
  assert.equal(r[0].a_ingresar, 20);
  // T2: 3.040 − 20 − 3.000 = 20.
  assert.equal(r[1].a_ingresar, 20);
});

test("modelo 130: un trimestre con pérdidas no se arrastra dos veces", () => {
  const r = calcularModelo130({
    trimestres: [
      { ingresos: 1000, gastos: 3000, retenciones: 0 },
      { ingresos: 10000, gastos: 0, retenciones: 0 },
    ],
    modalidad: "directa_normal",
    minoracion: 0,
  });
  assert.equal(r[0].casilla_07, 0);
  assert.equal(r[0].a_ingresar, 0);
  // Acumulado: 11.000 − 3.000 = 8.000 → 1.600.
  assert.equal(r[1].a_ingresar, 1600);
});

test("modelo 130: la minoración sobrante pasa al trimestre siguiente, pero no del cuarto", () => {
  const r = calcularModelo130({
    trimestres: [
      { ingresos: 200, gastos: 0, retenciones: 0 },
      { ingresos: 1000, gastos: 0, retenciones: 0 },
      { ingresos: 0, gastos: 0, retenciones: 0 },
      { ingresos: 0, gastos: 0, retenciones: 0 },
    ],
    modalidad: "directa_normal",
    minoracion: 100,
  });
  assert.equal(r[0].resultado, -60); // 40 − 100
  assert.equal(r[1].negativos_anteriores, 60); // 200 − 100 = 100, menos 60 pendientes
  assert.equal(r[1].a_ingresar, 40);
  assert.equal(r[3].resultado, -100);
});

test("sueldo neto con el ejemplo de 40.000 € y 5.000 € de gastos", () => {
  const r = calcularSueldoNeto({
    ingresos: 40000, gastos: 5000, cuotaMensual: null,
    modalidad: "directa_simplificada", cumpleRequisitosArt32: false, inicioActividad: false,
  });
  assert.equal(r.tramo, 7);
  assert.equal(r.cuotaMensual, 427.21);
  assert.equal(r.netoAnual, Math.round((40000 - 5000 - r.cuotaAnual - r.irpf) * 100) / 100);
  assert.ok(r.netoMensual > 1500 && r.netoMensual < 2500);
});

test("sueldo neto con una cuota indicada por el usuario", () => {
  const r = calcularSueldoNeto({
    ingresos: 30000, gastos: 0, cuotaMensual: 100,
    modalidad: "directa_normal", cumpleRequisitosArt32: false, inicioActividad: false,
  });
  assert.equal(r.cuotaAnual, 1200);
});

import { calcularIva } from "../iva/calculo.js";
import { facturacionParaNeto } from "../objetivo/calculo.js";

test("añadir IVA del 21 %", () => {
  assert.deepEqual(calcularIva({ importe: 100, modo: "anadir", tipo: 21 }), { base: 100, iva: 21, total: 121 });
});

test("quitar IVA: base e IVA suman siempre el precio", () => {
  assert.deepEqual(calcularIva({ importe: 121, modo: "quitar", tipo: 21 }), { base: 100, iva: 21, total: 121 });
  for (const importe of [9.99, 1, 0.05, 333.33, 12345.67]) {
    for (const tipo of [21, 10, 4]) {
      const r = calcularIva({ importe, modo: "quitar", tipo });
      assert.equal(Math.round((r.base + r.iva) * 100), Math.round(importe * 100));
    }
  }
});

test("cuánto facturar: es la inversa del sueldo neto", () => {
  const datos = { gastos: 5000, modalidad: "directa_simplificada", cumpleRequisitosArt32: false, inicioActividad: false };
  const r = facturacionParaNeto({ netoMensual: 2016.04, ...datos });
  assert.ok(Math.abs(r.ingresos - 40000) < 5, `facturación ${r.ingresos}`);
  assert.ok(r.netoMensual >= 2016.04);
  // Un euro menos de facturación ya no llega al objetivo (un céntimo puede no notarse al redondear).
  const menos = calcularSueldoNeto({ ingresos: r.ingresos - 1, cuotaMensual: null, ...datos });
  assert.ok(menos.netoAnual < 2016.04 * 12);
});

test("cuánto facturar con objetivo cero o imposible", () => {
  const datos = { gastos: 0, modalidad: "directa_normal", cumpleRequisitosArt32: false, inicioActividad: false };
  assert.ok(facturacionParaNeto({ netoMensual: 0, ...datos }).ingresos > 0);
  assert.equal(facturacionParaNeto({ netoMensual: 9_000_000, ...datos }), null);
});
