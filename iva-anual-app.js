// Calculadora del IVA anual de 2027 (Real Decreto-ley 43/2026). Todo ocurre en el navegador.
import { calcularIvaAnual2027 } from "./iva-anual/calculo.js";
import { idioma, euros, importe, elemento, fila, tabla, total, mostrar, error, conectar } from "./comun.js";

const TEXTOS = {
  es: {
    error: "Revisa los importes: deben ser números positivos.",
    errorFecha: "Revisa la fecha de inicio: tiene que ser un día de 2026.",
    sociedad: ["Las sociedades no pueden", "El IVA anual es solo para autónomos personas físicas y para comunidades de bienes o sociedades civiles en las que todos los socios son personas físicas. Una sociedad limitada sigue presentando el modelo 303 cada trimestre."],
    recargo: ["No te afecta", "Con el recargo de equivalencia no presentas el IVA de esas ventas: lo paga tu proveedor. El régimen de declaración anual no se aplica a las operaciones del recargo de equivalencia."],
    supera: (v) => `No puedes: tu volumen de operaciones de 2026 es de ${v}, más de 85.000 €.`,
    superaTitulo: "No puedes acogerte en 2027",
    puede: "Puedes acogerte al IVA anual en 2027",
    puedeNota: "Una sola declaración al año en enero y tres pagos fijos que Hacienda te carga en la cuenta.",
    inicioNota: "Como empiezas la actividad en 2027, puedes pedirlo al darte de alta y tus pagos a cuenta de 2027 son cero: pagarías todo el IVA del año en enero de 2028.",
    calendario: "Tus pagos con el IVA anual",
    cabecera: ["Cuándo", "Importe"],
    fechas: ["20 de abril de 2027 (cargo en cuenta)", "20 de julio de 2027 (cargo en cuenta)", "20 de octubre de 2027 (cargo en cuenta)"],
    enero: "Declaración anual, del 1 al 30 de enero de 2028",
    eneroDevolver: (c) => `${c} a devolver o compensar`,
    eneroFalta: "Lo que falte del IVA de 2027",
    cuotaReferencia: "IVA de 2026 (cobrado menos deducible)",
    volumen: "Volumen de operaciones de 2026",
    volumenElevado: (d) => `Volumen de operaciones de 2026 elevado al año (${d} días de actividad)`,
    pagoNota: "Cada pago es la cuarta parte de tu IVA de 2026. En enero pagas lo que falte o te devuelven lo que sobre. Es una estimación: Hacienda te enseñará el importe exacto en su sede electrónica en los primeros días de abril.",
    pagoCero: "Tu IVA de 2026 no salió a pagar, así que tus tres pagos a cuenta son cero.",
    general: "Con el régimen general seguirías presentando cuatro modelos 303 (hasta el 20 de abril, el 20 de julio, el 20 de octubre y el 30 de enero), cada uno con el IVA de su trimestre.",
    criterioCaja: "Al optar en marzo de 2027 dejas el criterio de caja. Las facturas de 2027 que ya lleven la mención «régimen especial del criterio de caja» habrá que rectificarlas para quitarla.",
    redeme: "Saldrás del registro de devolución mensual (REDEME) desde el 1 de enero de 2027: ya no te devolverán el IVA cada mes.",
    simplificado: "Para optar tendrías que renunciar al régimen simplificado del IVA (módulos), y eso también afecta a los módulos del IRPF. Consúltalo con un asesor antes de decidir.",
    comoPedirlo: "Cómo pedirlo: en marzo de 2027, con la declaración censal, indicando la cuenta bancaria para los cargos. Los pagos a cuenta no se pueden aplazar ni fraccionar, y si después renuncias, la renuncia dura al menos tres años.",
    comoPedirloAlta: "Cómo pedirlo: en la declaración censal de alta, indicando la cuenta bancaria para los cargos; si te das de alta antes de marzo de 2027, se pide en marzo. Los pagos a cuenta no se pueden aplazar ni fraccionar, y si después renuncias, la renuncia dura al menos tres años.",
    convalidacion: "Son reglas del Real Decreto-ley 43/2026, en vigor desde el 26 de noviembre de 2026. El Congreso tiene que convalidarlo; si no lo hiciera, el IVA anual no existiría.",
  },
  ca: {
    error: "Revisa els imports: han de ser nombres positius.",
    errorFecha: "Revisa la data d'inici: ha de ser un dia del 2026.",
    sociedad: ["Les societats no poden", "L'IVA anual és només per a autònoms persones físiques i per a comunitats de béns o societats civils en què tots els socis són persones físiques. Una societat limitada continua presentant el model 303 cada trimestre."],
    recargo: ["No t'afecta", "Amb el recàrrec d'equivalència no presentes l'IVA d'aquestes vendes: el paga el teu proveïdor. El règim de declaració anual no s'aplica a les operacions del recàrrec d'equivalència."],
    supera: (v) => `No pots: el teu volum d'operacions del 2026 és de ${v}, més de 85.000 €.`,
    superaTitulo: "No t'hi pots acollir el 2027",
    puede: "Et pots acollir a l'IVA anual el 2027",
    puedeNota: "Una sola declaració a l'any el gener i tres pagaments fixos que Hisenda et carrega al compte.",
    inicioNota: "Com que comences l'activitat el 2027, ho pots demanar quan et donis d'alta i els teus pagaments a compte del 2027 són zero: pagaries tot l'IVA de l'any el gener del 2028.",
    calendario: "Els teus pagaments amb l'IVA anual",
    cabecera: ["Quan", "Import"],
    fechas: ["20 d'abril de 2027 (càrrec al compte)", "20 de juliol de 2027 (càrrec al compte)", "20 d'octubre de 2027 (càrrec al compte)"],
    enero: "Declaració anual, de l'1 al 30 de gener de 2028",
    eneroDevolver: (c) => `${c} a retornar o compensar`,
    eneroFalta: "El que falti de l'IVA del 2027",
    cuotaReferencia: "IVA del 2026 (cobrat menys deduïble)",
    volumen: "Volum d'operacions del 2026",
    volumenElevado: (d) => `Volum d'operacions del 2026 elevat a l'any (${d} dies d'activitat)`,
    pagoNota: "Cada pagament és la quarta part del teu IVA del 2026. El gener pagues el que falti o et retornen el que sobri. És una estimació: Hisenda t'ensenyarà l'import exacte a la seu electrònica els primers dies d'abril.",
    pagoCero: "El teu IVA del 2026 no va sortir a pagar, així que els teus tres pagaments a compte són zero.",
    general: "Amb el règim general continuaries presentant quatre models 303 (fins al 20 d'abril, el 20 de juliol, el 20 d'octubre i el 30 de gener), cadascun amb l'IVA del seu trimestre.",
    criterioCaja: "En optar el març del 2027 deixes el criteri de caixa. Les factures del 2027 que ja portin la menció «règim especial del criteri de caixa» s'hauran de rectificar per treure-la.",
    redeme: "Sortiràs del registre de devolució mensual (REDEME) des de l'1 de gener de 2027: ja no et retornaran l'IVA cada mes.",
    simplificado: "Per optar hauries de renunciar al règim simplificat de l'IVA (mòduls), i això també afecta els mòduls de l'IRPF. Consulta-ho amb un assessor abans de decidir.",
    comoPedirlo: "Com demanar-ho: el març del 2027, amb la declaració censal, indicant el compte bancari per als càrrecs. Els pagaments a compte no es poden ajornar ni fraccionar, i si després hi renuncies, la renúncia dura almenys tres anys.",
    comoPedirloAlta: "Com demanar-ho: a la declaració censal d'alta, indicant el compte bancari per als càrrecs; si et dones d'alta abans del març del 2027, es demana el març. Els pagaments a compte no es poden ajornar ni fraccionar, i si després hi renuncies, la renúncia dura almenys tres anys.",
    convalidacion: "Són regles del Reial decret llei 43/2026, en vigor des del 26 de novembre de 2026. El Congrés l'ha de convalidar; si no ho fes, l'IVA anual no existiria.",
  },
};
const t = TEXTOS[idioma];
const resultado = document.getElementById("resultado");
const bloqueFecha = document.getElementById("bloque-fecha");
const bloquesIva = document.querySelectorAll(".solo-con-2026");

function nota(texto) {
  return elemento("p", texto, "nota");
}

function calcular() {
  const titular = document.getElementById("titular").value;
  const inicio = document.getElementById("inicio").value;
  const regimen = document.getElementById("regimen").value;
  bloqueFecha.hidden = inicio !== "2026";
  for (const bloque of bloquesIva) bloque.hidden = inicio === "2027";

  if (titular === "sociedad") return mostrar(resultado, total(t.sociedad[0], "", t.sociedad[1]));
  if (regimen === "recargo") return mostrar(resultado, total(t.recargo[0], "", t.recargo[1]));

  const volumen = importe("volumen");
  const repercutido = importe("repercutido");
  const soportado = importe("soportado");
  const textoPrevisto = document.getElementById("previsto").value.trim();
  const previsto = textoPrevisto === "" ? null : importe("previsto", null);
  if (volumen === null || repercutido === null || soportado === null || (textoPrevisto !== "" && previsto === null)) {
    return mostrar(resultado, error(t.error));
  }

  const r = calcularIvaAnual2027({
    titular,
    inicio,
    fechaInicio: document.getElementById("fecha").value,
    volumen,
    regimen,
    ivaRepercutido: repercutido,
    ivaSoportado: soportado,
    ivaPrevisto2027: previsto,
  });
  if (r.caso === "fecha_invalida") return mostrar(resultado, error(t.errorFecha));
  if (r.caso === "supera") {
    return mostrar(
      resultado,
      total(t.superaTitulo, "", t.supera(euros.format(r.volumenAnual))),
      tabla([fila([r.elevado ? t.volumenElevado(r.dias) : t.volumen, euros.format(r.volumenAnual)])]),
      nota(t.general),
    );
  }

  const piezas = [total(t.puede, "", r.inicio === "2027" ? t.inicioNota : t.puedeNota)];
  if (r.inicio !== "2027") {
    piezas.push(tabla([
      fila([r.elevado ? t.volumenElevado(r.dias) : t.volumen, euros.format(r.volumenAnual)]),
      fila([t.cuotaReferencia, euros.format(r.cuotaReferencia)]),
    ]));
  }
  const filas = t.fechas.map((fecha) => fila([fecha, euros.format(r.pagoACuenta)]));
  let eneroTexto = t.eneroFalta;
  if (r.enero !== null) eneroTexto = r.enero < 0 ? t.eneroDevolver(euros.format(-r.enero)) : euros.format(r.enero);
  filas.push(fila([t.enero, eneroTexto], true));
  piezas.push(elemento("h3", t.calendario), tabla(filas, t.cabecera));
  if (r.inicio !== "2027") piezas.push(nota(r.pagoACuenta === 0 ? t.pagoCero : t.pagoNota));
  if (regimen === "criterio_caja") piezas.push(nota(t.criterioCaja));
  if (regimen === "redeme_voluntario") piezas.push(nota(t.redeme));
  if (regimen === "simplificado") piezas.push(nota(t.simplificado));
  piezas.push(nota(r.inicio === "2027" ? t.comoPedirloAlta : t.comoPedirlo), nota(t.general), nota(t.convalidacion));
  mostrar(resultado, ...piezas);
}

conectar(calcular);
