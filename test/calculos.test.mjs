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
  // T3: 24.000 − 1.200 = 22.800 → 4.560 − 3.040. T4 de 2026 (Real Decreto-ley 43/2026): 10 % de 32.000,
  // con el máximo de 3.000 € → 29.000 → 5.800 − 4.560.
  assert.equal(r[2].a_ingresar, 1520);
  assert.equal(r[3].dificil, 3000);
  assert.equal(r[3].a_ingresar, 1240);
});

test("modelo 130: el límite de difícil justificación es anual (2.000 € hasta el 3T y 3.000 € en el 4T)", () => {
  const t = { ingresos: 20000, gastos: 0, retenciones: 0 };
  const r = calcularModelo130({ trimestres: [t, t, t, t], modalidad: "directa_simplificada", minoracion: 0 });
  assert.equal(r[0].dificil, 1000);
  assert.equal(r[1].dificil, 2000);
  assert.equal(r[2].dificil, 2000);
  assert.equal(r[3].dificil, 3000);
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
  // Con 40.000 € y 5.000 € de gastos quedan 2.054,63 € al mes en 2026 (calculado aparte, con el 10 % de
  // difícil justificación y su máximo de 3.000 €).
  assert.equal(calcularSueldoNeto({ ingresos: 40000, cuotaMensual: null, ...datos }).netoMensual, 2054.63);
  const r = facturacionParaNeto({ netoMensual: 2054.63, ...datos });
  assert.ok(Math.abs(r.ingresos - 40000) < 5, `facturación ${r.ingresos}`);
  assert.ok(r.netoMensual >= 2054.63);
  // Un euro menos de facturación ya no llega al objetivo (un céntimo puede no notarse al redondear).
  const menos = calcularSueldoNeto({ ingresos: r.ingresos - 1, cuotaMensual: null, ...datos });
  assert.ok(menos.netoAnual < 2054.63 * 12);
});

test("cuánto facturar con objetivo cero o imposible", () => {
  const datos = { gastos: 0, modalidad: "directa_normal", cumpleRequisitosArt32: false, inicioActividad: false };
  assert.ok(facturacionParaNeto({ netoMensual: 0, ...datos }).ingresos > 0);
  assert.equal(facturacionParaNeto({ netoMensual: 9_000_000, ...datos }), null);
});

test("sueldo neto en otra comunidad: Madrid paga menos IRPF que Cataluña", () => {
  const datos = { ingresos: 40000, gastos: 5000, cuotaMensual: null, modalidad: "directa_simplificada", cumpleRequisitosArt32: false, inicioActividad: false };
  const cat = calcularSueldoNeto({ ...datos, comunidad: "cataluna" });
  const mad = calcularSueldoNeto({ ...datos, comunidad: "madrid" });
  assert.equal(cat.irpf, calcularSueldoNeto(datos).irpf);
  assert.ok(mad.irpf < cat.irpf);
  assert.ok(mad.netoMensual > cat.netoMensual);
});

import { calcularTarifaPlana, rendimientoParaSmi, SMI_ANUAL, TARIFA_PLANA_2026 } from "../tarifa/calculo.js";

test("tarifa plana: 88,64 € frente a la cuota normal de 427,21 €", () => {
  const r = calcularTarifaPlana({ ingresos: 40000, gastos: 5000, modalidad: "directa_simplificada", cumpleRequisitosArt32: false });
  assert.equal(TARIFA_PLANA_2026.total, TARIFA_PLANA_2026.cuotaReducida + TARIFA_PLANA_2026.mei);
  assert.equal(r.tarifaMensual, 88.64);
  assert.equal(r.cuotaNormalMensual, 427.21);
  assert.equal(r.ahorroMensual, 338.57);
  assert.equal(r.mesesIniciales, 12);
  assert.equal(r.pagadoPeriodoInicial, 1063.68);
  assert.equal(r.ahorroPeriodoInicial, 4062.84);
  // 2026: el 10 % de 33.936,32 supera el máximo, así que 35.000 - 3.000 = 32.000; menos el 7 % = 29.760, por encima del SMI.
  assert.equal(r.rendimientoParaSmi, 29760);
  assert.equal(r.prorroga[2026].cumple, false);
  assert.equal(r.prorroga[2027].cumple, false);
});

test("tarifa plana: con rendimientos bajos se puede alargar", () => {
  const r = calcularTarifaPlana({ ingresos: 18000, gastos: 3000, modalidad: "directa_simplificada", cumpleRequisitosArt32: false });
  // 15.000 - 10 % de 13.936,32 = 13.606,37; menos el 7 % = 12.653,92.
  assert.equal(r.rendimientoParaSmi, 12653.92);
  assert.equal(r.prorroga[2026].cumple, true);
  assert.equal(r.prorroga[2027].cumple, true);
  assert.equal(r.ahorroProrroga, Math.round(r.ahorroMensual * 12 * 100) / 100);
});

test("tarifa plana: entre los dos SMI solo se puede alargar en 2027", () => {
  // Directa normal, sin difícil justificación: 19.000 x 0,93 = 17.670, entre 17.094 y 18.004.
  const r = calcularTarifaPlana({ ingresos: 19000, gastos: 0, modalidad: "directa_normal", cumpleRequisitosArt32: false });
  assert.equal(r.rendimientoParaSmi, 17670);
  assert.equal(r.prorroga[2026].cumple, false);
  assert.equal(r.prorroga[2027].cumple, true);
  assert.equal(SMI_ANUAL[2026], 1221 * 14);
  assert.equal(SMI_ANUAL[2027], 1286 * 14);
});

test("tarifa plana: casos especiales con 24 meses y sin cifra de prórroga", () => {
  const r = calcularTarifaPlana({ ingresos: 30000, gastos: 4000, modalidad: "directa_simplificada", cumpleRequisitosArt32: false, especial: true });
  assert.equal(r.mesesIniciales, 24);
  assert.equal(r.mesesProrroga, 36);
  assert.equal(r.pagadoPeriodoInicial, 2127.36);
  assert.equal(r.ahorroProrroga, null);
  assert.equal(r.ahorroPeriodoInicial, Math.round(r.ahorroMensual * 24 * 100) / 100);
});

test("tarifa plana: el SMI se compara con un rendimiento que nunca es negativo", () => {
  assert.equal(rendimientoParaSmi({ ingresos: 0, gastos: 5000, modalidad: "directa_simplificada", cumpleRequisitosArt32: false }), 0);
  const r = calcularTarifaPlana({ ingresos: 0, gastos: 0, modalidad: "directa_simplificada", cumpleRequisitosArt32: false });
  assert.ok(r.ahorroMensual > 0);
});
