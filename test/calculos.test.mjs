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

import { calcularRegularizacion, CUOTA_MAXIMA_2026, CUOTA_MINIMA_2026 } from "../regularizacion/calculo.js";

test("regularización: con la cuota mínima del tramo 1 y rendimientos del tramo 5 se paga la diferencia", () => {
  // 30.000 - 3.000 - 3.594,72 de cuotas = 23.405,28; 10 % de difícil justificación = 2.340,53.
  // Computable: 27.000 - 2.340,53 = 24.659,47; menos el 7 %, entre 12 = 1.911,11 → tramo 5 de la general.
  const r = calcularRegularizacion({ ingresos: 30000, gastos: 3000, cuotaMensual: 299.56, meses: 12, modalidad: "directa_simplificada", cumpleRequisitosArt32: false });
  assert.equal(r.rendimientoMensual, 1911.11);
  assert.equal(r.tabla, "general");
  assert.equal(r.tramo, 5);
  assert.equal(r.cuotaMinima, 380.88);
  assert.equal(r.cuotaMaxima, 639.45);
  assert.equal(r.resultado, "pagar");
  assert.equal(r.diferenciaMensual, 81.32);
  assert.equal(r.importe, 975.84);
});

test("regularización: por encima de la máxima del tramo real se devuelve el exceso", () => {
  // Directa normal: 12.000 × 0,93 / 12 = 930 € al mes → tramo 3 de la reducida (de 267,65 a 367,51 €).
  const datos = { ingresos: 15000, gastos: 3000, meses: 12, modalidad: "directa_normal", cumpleRequisitosArt32: false };
  const r = calcularRegularizacion({ ...datos, cuotaMensual: 500 });
  assert.equal(r.rendimientoMensual, 930);
  assert.equal(r.tabla, "reducida");
  assert.equal(r.tramo, 3);
  assert.equal(r.cuotaMinima, 267.65);
  assert.equal(r.cuotaMaxima, 367.51);
  assert.equal(r.resultado, "devolver");
  assert.equal(r.importe, 1589.88);
  // Entre la mínima y la máxima no cambia nada.
  const n = calcularRegularizacion({ ...datos, cuotaMensual: 300 });
  assert.equal(n.resultado, "nada");
  assert.equal(n.importe, 0);
});

test("regularización: el rendimiento se reparte entre los meses de alta", () => {
  // 6 meses: 12.000 × 0,93 / 6 = 1.860 € al mes → tramo 5 de la general (mínima 380,88 €).
  const r = calcularRegularizacion({ ingresos: 15000, gastos: 3000, cuotaMensual: 300, meses: 6, modalidad: "directa_normal", cumpleRequisitosArt32: false });
  assert.equal(r.rendimientoMensual, 1860);
  assert.equal(r.tramo, 5);
  assert.equal(r.importe, Math.round((380.88 - 300) * 6 * 100) / 100);
  assert.equal(CUOTA_MINIMA_2026, 205.88);
  assert.equal(CUOTA_MAXIMA_2026, 1606.88);
});

// ---- Novedades de 2027 (Real Decreto-ley 43/2026)
import { calcularModelo130En2027, diasActividad2025 } from "../modelo130-2027/calculo.js";
import { calcularIvaAnual2027, diasActividad2026 } from "../iva-anual/calculo.js";

const base130 = { metodo: "directa", inicio: "antes", cifraNegocios: 30000, cuotaDiferencial: -600, pagosFraccionados: 400, profesionalRetenciones70: false };

test("130 en 2027: dispensa si la cifra es inferior a 85.000 € y lo devuelto cubre los pagos", () => {
  const r = calcularModelo130En2027(base130);
  assert.equal(r.caso, "dispensa");
  assert.equal(r.porcentaje, null);
  // Igual al límite: lo devuelto igual a los pagos también cuenta.
  assert.equal(calcularModelo130En2027({ ...base130, cuotaDiferencial: -400 }).caso, "dispensa");
  // Sin pagos y a devolver: también (la condición es «igual o superior» a 0).
  assert.equal(calcularModelo130En2027({ ...base130, pagosFraccionados: 0, cuotaDiferencial: -1 }).caso, "dispensa");
});

test("130 en 2027: sin dispensa si lo devuelto no cubre los pagos, si sale a pagar o si la cifra llega a 85.000 €", () => {
  const poco = calcularModelo130En2027({ ...base130, cuotaDiferencial: -399.99 });
  assert.equal(poco.caso, "presenta");
  assert.equal(poco.porcentaje, 19);
  assert.equal(poco.puedeDomiciliar, true);
  assert.equal(calcularModelo130En2027({ ...base130, cuotaDiferencial: 100 }).caso, "presenta");
  assert.equal(calcularModelo130En2027({ ...base130, cuotaDiferencial: 0 }).caso, "presenta");
  const justo = calcularModelo130En2027({ ...base130, cifraNegocios: 85000 });
  assert.equal(justo.caso, "presenta");
  assert.equal(justo.puedeDomiciliar, true);
  assert.equal(calcularModelo130En2027({ ...base130, cifraNegocios: 84999.99 }).caso, "dispensa");
});

test("130 en 2027: 19 % por debajo de 250.000 € y 20 % desde 250.000 €", () => {
  const sin = { ...base130, cuotaDiferencial: 500 };
  assert.equal(calcularModelo130En2027({ ...sin, cifraNegocios: 249999.99 }).porcentaje, 19);
  const alto = calcularModelo130En2027({ ...sin, cifraNegocios: 250000 });
  assert.equal(alto.porcentaje, 20);
  assert.equal(alto.puedeDomiciliar, false);
});

test("130 en 2027: pago domiciliado = 25 % del rendimiento de 2025 por la suma de tipos medios", () => {
  const r = calcularModelo130En2027({ ...base130, cifraNegocios: 120000, rendimientoNeto: 40000, tipoMedioEstatal: 9.5, tipoMedioAutonomico: 10.25 });
  assert.equal(r.caso, "presenta");
  assert.equal(r.puedeDomiciliar, true);
  assert.equal(r.tipoMedio, 19.75);
  assert.equal(r.pagoDomiciliado, 1975); // 40.000 × 19,75 % ÷ 4
  // Sin pagos fraccionados en 2025 no se puede domiciliar.
  assert.equal(calcularModelo130En2027({ ...base130, cifraNegocios: 120000, pagosFraccionados: 0 }).puedeDomiciliar, false);
});

test("130 en 2027: si empezó en 2025 la cifra se eleva al año por días", () => {
  assert.equal(diasActividad2025("2025-01-01"), 365);
  assert.equal(diasActividad2025("2025-07-01"), 184);
  assert.equal(diasActividad2025("2025-12-31"), 1);
  assert.equal(diasActividad2025("2025-02-30"), null);
  assert.equal(diasActividad2025("2024-05-01"), null);
  const r = calcularModelo130En2027({ ...base130, inicio: "2025", fechaInicio: "2025-07-01", cifraNegocios: 50000 });
  assert.equal(r.cifraAnual, 99184.78); // 50.000 × 365 ÷ 184
  assert.equal(r.caso, "presenta");
});

test("130 en 2027: casos sin cálculo", () => {
  assert.equal(calcularModelo130En2027({ ...base130, metodo: "objetiva" }).caso, "objetiva");
  assert.equal(calcularModelo130En2027({ ...base130, metodo: "agraria" }).caso, "agraria");
  assert.equal(calcularModelo130En2027({ ...base130, profesionalRetenciones70: true }).caso, "retenciones_70");
  assert.equal(calcularModelo130En2027({ ...base130, inicio: "despues", profesionalRetenciones70: true }).caso, "retenciones_70");
  assert.deepEqual(calcularModelo130En2027({ ...base130, inicio: "despues" }), { caso: "sin_actividad_2025", porcentaje: 19 });
});

const baseIva = { titular: "persona", inicio: "antes", volumen: 40000, regimen: "general", ivaRepercutido: 8400, ivaSoportado: 2400 };

test("IVA anual 2027: pagos a cuenta de la cuarta parte del IVA de 2026 y el resto en enero", () => {
  const r = calcularIvaAnual2027(baseIva);
  assert.equal(r.caso, "puede");
  assert.equal(r.cuotaReferencia, 6000);
  assert.equal(r.pagoACuenta, 1500);
  assert.equal(r.enero, 1500);
  const menos = calcularIvaAnual2027({ ...baseIva, ivaPrevisto2027: 3000 });
  assert.equal(menos.enero, -1500); // a devolver o compensar
  const centimos = calcularIvaAnual2027({ ...baseIva, ivaRepercutido: 1000.01, ivaSoportado: 0 });
  assert.equal(centimos.pagoACuenta, 250);
});

test("IVA anual 2027: límite de 85.000 € (incluido) y elevación al año", () => {
  assert.equal(calcularIvaAnual2027({ ...baseIva, volumen: 85000 }).caso, "puede");
  assert.equal(calcularIvaAnual2027({ ...baseIva, volumen: 85000.01 }).caso, "supera");
  assert.equal(diasActividad2026("2026-10-01"), 92);
  const r = calcularIvaAnual2027({ ...baseIva, inicio: "2026", fechaInicio: "2026-10-01", volumen: 25000 });
  assert.equal(r.caso, "supera");
  assert.equal(r.volumenAnual, 99184.78); // 25.000 × 365 ÷ 92
});

test("IVA anual 2027: pagos cero si el IVA de 2026 no sale a pagar o si se empieza en 2027", () => {
  assert.equal(calcularIvaAnual2027({ ...baseIva, ivaRepercutido: 1000, ivaSoportado: 1500 }).pagoACuenta, 0);
  assert.equal(calcularIvaAnual2027({ ...baseIva, ivaRepercutido: 1000, ivaSoportado: 1000 }).pagoACuenta, 0);
  const nuevo = calcularIvaAnual2027({ ...baseIva, inicio: "2027", ivaPrevisto2027: 2000 });
  assert.equal(nuevo.pagoACuenta, 0);
  assert.equal(nuevo.enero, 2000);
  assert.equal(calcularIvaAnual2027({ ...baseIva, inicio: "2027" }).enero, null);
});

test("IVA anual 2027: sociedades y recargo de equivalencia", () => {
  assert.equal(calcularIvaAnual2027({ ...baseIva, titular: "sociedad" }).caso, "sociedad");
  assert.equal(calcularIvaAnual2027({ ...baseIva, regimen: "recargo" }).caso, "recargo");
  assert.equal(calcularIvaAnual2027({ ...baseIva, titular: "atribucion_fisicas" }).caso, "puede");
});
