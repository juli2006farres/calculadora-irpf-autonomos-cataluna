import { TABLAS } from "./tablas.js";
// Redondea a céntimos, que es como se expresan los importes fiscales.
function aCentimos(valor) {
    return Math.round(valor * 100) / 100;
}
// Aplica una escala progresiva: cada tipo grava solo la parte de base de su tramo,
// no toda la base. Por eso "subir de tramo" no encarece lo ya ganado por debajo.
export function aplicarEscala(base, tramos) {
    let cuota = 0;
    let limiteAnterior = 0;
    for (const { hasta, tipo } of tramos) {
        if (base <= limiteAnterior)
            break;
        cuota += ((Math.min(base, hasta) - limiteAnterior) * tipo) / 100;
        limiteAnterior = hasta;
    }
    return cuota;
}
// Gastos de difícil justificación: 5 % del rendimiento positivo, con un máximo de
// 2.000 €. Solo en simplificada y nunca junto a la reducción del art. 32.2.1.º.
function calcularGastosDificilJustificacion(entrada, previo, tabla) {
    if (entrada.modalidad !== "directa_simplificada" || entrada.cumpleRequisitosArt32 || previo <= 0) {
        return 0;
    }
    return Math.min((previo * tabla.porcentajeGastosDificilJustificacion) / 100, tabla.limiteGastosDificilJustificacion);
}
// Reducción del art. 32.2 de la Ley del IRPF. Se calcula suponiendo que el usuario
// no tiene otras rentas, ya que esta herramienta solo trabaja con su actividad.
function calcularReduccionArt32(rendimientoNeto, cumpleRequisitos) {
    if (rendimientoNeto <= 0)
        return 0;
    if (cumpleRequisitos) {
        // Art. 32.2.1.º: 2.000 € y un extra para rendimientos bajos.
        let reduccion = 2_000;
        if (rendimientoNeto <= 14_047.5) {
            reduccion += 6_498;
        }
        else if (rendimientoNeto < 19_747.5) {
            reduccion += 6_498 - 1.14 * (rendimientoNeto - 14_047.5);
        }
        return reduccion;
    }
    // Art. 32.2.3.º: para quien no cumple lo anterior y tiene rentas menores de 12.000 €.
    if (rendimientoNeto <= 8_000)
        return 1_620;
    if (rendimientoNeto < 12_000)
        return 1_620 - 0.405 * (rendimientoNeto - 8_000);
    return 0;
}
// Reducción por inicio de actividad (art. 32.3): 20 % del rendimiento positivo que queda
// tras las reducciones anteriores, y como máximo sobre 100.000 € al año.
function calcularReduccionInicio(rendimientoReducido, inicioActividad) {
    if (!inicioActividad || rendimientoReducido <= 0)
        return 0;
    return Math.min(rendimientoReducido, 100_000) * 0.2;
}
// Mínimo por descendientes (art. 58): cada hijo suma una cantidad según su orden,
// y los menores de 3 años añaden un incremento.
function calcularMinimoDescendientes(entrada, tabla) {
    let total = entrada.descendientesMenores3 * tabla.incrementoMenor3;
    for (let orden = 0; orden < entrada.descendientesMenores25; orden++) {
        total += tabla.minimoDescendientes[Math.min(orden, 3)] ?? 0;
    }
    // Si ambos progenitores tienen derecho al mínimo, se reparte a partes iguales.
    return entrada.minimoDescendientesCompartido ? total / 2 : total;
}
// Cálculo completo. Es una función pura: no usa red ni guarda nada, y con las
// mismas entradas siempre da el mismo resultado, lo que facilita probarla.
export function calcularIrpf(entrada) {
    const tabla = TABLAS[entrada.ejercicio];
    // Fase 1: de los ingresos al rendimiento de la actividad.
    const previo = entrada.ingresos - entrada.gastos - entrada.cuotasAutonomo;
    const dificilJustificacion = calcularGastosDificilJustificacion(entrada, previo, tabla);
    const rendimientoNeto = previo - dificilJustificacion;
    // La reducción no puede dejar el rendimiento en negativo (art. 32.2.4.º).
    const reduccion = Math.min(calcularReduccionArt32(rendimientoNeto, entrada.cumpleRequisitosArt32), Math.max(rendimientoNeto, 0));
    const rendimientoReducido = Math.max(rendimientoNeto - reduccion, 0);
    const reduccionInicio = calcularReduccionInicio(rendimientoReducido, entrada.inicioActividad);
    const base = rendimientoReducido - reduccionInicio;
    // Fase 2: la escala se aplica a la base y también al mínimo, y se restan ambas
    // cuotas. Así funciona el mínimo personal: no reduce la base, sino la cuota.
    const minimo = tabla.minimoContribuyente + calcularMinimoDescendientes(entrada, tabla);
    const minimoAplicable = Math.min(minimo, base);
    const cuotaEstatal = aplicarEscala(base, tabla.escalaEstatal) - aplicarEscala(minimoAplicable, tabla.escalaEstatal);
    const cuotaAutonomica = aplicarEscala(base, tabla.escalaCataluna) - aplicarEscala(minimoAplicable, tabla.escalaCataluna);
    const cuotaIntegra = cuotaEstatal + cuotaAutonomica;
    return {
        rendimiento_previo: aCentimos(previo),
        gastos_dificil_justificacion: aCentimos(dificilJustificacion),
        rendimiento_neto: aCentimos(rendimientoNeto),
        reduccion_art_32: aCentimos(reduccion),
        reduccion_inicio_actividad: aCentimos(reduccionInicio),
        base_liquidable_general: aCentimos(base),
        minimo_personal_y_familiar: aCentimos(minimo),
        cuota_estatal: aCentimos(cuotaEstatal),
        cuota_autonomica: aCentimos(cuotaAutonomica),
        cuota_integra: aCentimos(cuotaIntegra),
        tipo_medio_porcentaje: base > 0 ? aCentimos((cuotaIntegra / base) * 100) : 0,
        pagos_a_cuenta: aCentimos(entrada.pagosACuenta),
        resultado_estimado: aCentimos(cuotaIntegra - entrada.pagosACuenta),
    };
}
//# sourceMappingURL=calculo.js.map