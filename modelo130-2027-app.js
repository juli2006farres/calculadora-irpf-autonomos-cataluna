// Calculadora del modelo 130 en 2027 (Real Decreto-ley 43/2026). Todo ocurre en el navegador.
import { calcularModelo130En2027, LIMITE_DISPENSA, LIMITE_19 } from "./modelo130-2027/calculo.js";
import { idioma, euros, numero, importe, elemento, fila, tabla, total, mostrar, error, conectar } from "./comun.js";

const TEXTOS = {
  es: {
    error: "Revisa los importes: deben ser números positivos.",
    errorFecha: "Revisa la fecha de inicio: tiene que ser un día de 2025.",
    errorTipos: "Revisa los tipos medios: son porcentajes entre 0 y 100.",
    objetiva: ["Con módulos, el decreto no cambia nada", "En estimación objetiva (módulos) se presenta el modelo 131, no el 130, y sus porcentajes siguen igual en 2027: el 4 %, el 3 % con un asalariado o el 2 % sin asalariados."],
    agraria: ["Sin cambios para las actividades agrarias", "En las actividades agrícolas, ganaderas, forestales o pesqueras el pago fraccionado sigue siendo del 2 % en 2027, y la nueva dispensa no se aplica a ellas."],
    retenciones: ["No tienes que presentar el modelo 130", "Como profesional, si en 2026 al menos el 70 % de los ingresos de tu actividad tuvo retención, no estás obligado a presentar el modelo 130 en 2027. Esta regla ya existía y el decreto la mantiene."],
    sinActividad: ["Si lo presentas, será al 19 %", "Si en 2025 no tenías la actividad, el porcentaje de 2027 es el 19 %. Para la nueva dispensa la norma mira tu renta de 2025, pero no dice qué pasa si ese año no tenías la actividad: hasta que Hacienda lo aclare, cuenta con presentarlo cada trimestre."],
    dispensa: "No tienes que presentar el modelo 130 en 2027",
    dispensaNota: "Cumples las dos condiciones de la dispensa: cifra de negocios de 2025 inferior a 85.000 € y una renta de 2025 a devolver que cubre lo que pagaste con el 130 ese año.",
    presenta: (p) => `Tienes que presentar el modelo 130 en 2027, al ${p} %`,
    presentaNota: (p) => (p === 19
      ? "Tu cifra de negocios de 2025 es inferior a 250.000 €, así que pagas el 19 % de tu rendimiento en vez del 20 %."
      : "Tu cifra de negocios de 2025 llega a 250.000 €, así que sigues pagando el 20 % de tu rendimiento."),
    filas: {
      cifra: "Cifra de negocios de 2025",
      cifraElevada: (d) => `Cifra de negocios de 2025 elevada al año (${d} días de actividad)`,
      menos85: "¿Inferior a 85.000 €?",
      menos250: "¿Inferior a 250.000 €?",
      renta: "Renta de 2025",
      cubre: "¿Lo devuelto cubre los pagos del 130 de 2025?",
      si: "Sí",
      no: "No",
      devolver: (c) => `A devolver ${c}`,
      noDevolver: "No salió a devolver",
    },
    domiciliar: "Puedes elegir el pago domiciliado",
    domiciliarTexto: "Como tu renta de 2025 salió a devolver después de haber pagado el 130, puedes pedir que Hacienda te cargue cada trimestre una cantidad fija: el 25 % de tu rendimiento neto de 2025 por la suma de tus tipos medios estatal y autonómico de 2025. No tienes que presentar el modelo: Hacienda te enseña el importe en su sede electrónica y lo carga el último día de cada plazo. Para 2027 se pide en marzo de 2027 con la declaración censal, indicando tu cuenta bancaria.",
    pago: "Pago domiciliado de cada trimestre",
    pagoNota: (t) => `Rendimiento neto de 2025 × ${t} % de tipo medio ÷ 4. Si te conviene más que el 19 % depende de lo que ganes en 2027.`,
    pagoFalta: "Si escribes tu rendimiento neto y tus tipos medios de 2025, te calculo el importe de cada trimestre.",
    pagoTabla: { anual: "Total en el año", tipo: "Suma de los tipos medios" },
    convalidacion: "Son reglas del Real Decreto-ley 43/2026, en vigor desde el 26 de noviembre de 2026. El Congreso tiene que convalidarlo; si no lo hiciera, estas novedades no se aplicarían.",
  },
  ca: {
    error: "Revisa els imports: han de ser nombres positius.",
    errorFecha: "Revisa la data d'inici: ha de ser un dia del 2025.",
    errorTipos: "Revisa els tipus mitjans: són percentatges entre 0 i 100.",
    objetiva: ["Amb mòduls, el decret no canvia res", "En estimació objectiva (mòduls) es presenta el model 131, no el 130, i els seus percentatges continuen igual el 2027: el 4 %, el 3 % amb un assalariat o el 2 % sense assalariats."],
    agraria: ["Sense canvis per a les activitats agràries", "En les activitats agrícoles, ramaderes, forestals o pesqueres el pagament fraccionat continua sent del 2 % el 2027, i la nova dispensa no s'hi aplica."],
    retenciones: ["No has de presentar el model 130", "Com a professional, si el 2026 almenys el 70 % dels ingressos de la teva activitat va tenir retenció, no estàs obligat a presentar el model 130 el 2027. Aquesta regla ja existia i el decret la manté."],
    sinActividad: ["Si el presentes, serà al 19 %", "Si el 2025 no tenies l'activitat, el percentatge del 2027 és el 19 %. Per a la nova dispensa la norma mira la teva renda del 2025, però no diu què passa si aquell any no tenies l'activitat: fins que Hisenda ho aclareixi, compta a presentar-lo cada trimestre."],
    dispensa: "No has de presentar el model 130 el 2027",
    dispensaNota: "Compleixes les dues condicions de la dispensa: xifra de negocis del 2025 inferior a 85.000 € i una renda del 2025 a retornar que cobreix el que vas pagar amb el 130 aquell any.",
    presenta: (p) => `Has de presentar el model 130 el 2027, al ${p} %`,
    presentaNota: (p) => (p === 19
      ? "La teva xifra de negocis del 2025 és inferior a 250.000 €, així que pagues el 19 % del teu rendiment en lloc del 20 %."
      : "La teva xifra de negocis del 2025 arriba a 250.000 €, així que continues pagant el 20 % del teu rendiment."),
    filas: {
      cifra: "Xifra de negocis del 2025",
      cifraElevada: (d) => `Xifra de negocis del 2025 elevada a l'any (${d} dies d'activitat)`,
      menos85: "Inferior a 85.000 €?",
      menos250: "Inferior a 250.000 €?",
      renta: "Renda del 2025",
      cubre: "El que et retornen cobreix els pagaments del 130 del 2025?",
      si: "Sí",
      no: "No",
      devolver: (c) => `A retornar ${c}`,
      noDevolver: "No va sortir a retornar",
    },
    domiciliar: "Pots triar el pagament domiciliat",
    domiciliarTexto: "Com que la teva renda del 2025 va sortir a retornar després d'haver pagat el 130, pots demanar que Hisenda et carregui cada trimestre una quantitat fixa: el 25 % del teu rendiment net del 2025 per la suma dels teus tipus mitjans estatal i autonòmic del 2025. No has de presentar el model: Hisenda t'ensenya l'import a la seu electrònica i el carrega l'últim dia de cada termini. Per al 2027 es demana el març del 2027 amb la declaració censal, indicant el teu compte bancari.",
    pago: "Pagament domiciliat de cada trimestre",
    pagoNota: (t) => `Rendiment net del 2025 × ${t} % de tipus mitjà ÷ 4. Si et convé més que el 19 % depèn del que guanyis el 2027.`,
    pagoFalta: "Si escrius el teu rendiment net i els teus tipus mitjans del 2025, et calculo l'import de cada trimestre.",
    pagoTabla: { anual: "Total a l'any", tipo: "Suma dels tipus mitjans" },
    convalidacion: "Són regles del Reial decret llei 43/2026, en vigor des del 26 de novembre de 2026. El Congrés l'ha de convalidar; si no ho fes, aquestes novetats no s'aplicarien.",
  },
};
const t = TEXTOS[idioma];
const resultado = document.getElementById("resultado");
const bloqueFecha = document.getElementById("bloque-fecha");
const bloquesDirecta = document.querySelectorAll(".solo-directa");

// Importe opcional: undefined si está vacío, null si no es válido.
function opcional(id) {
  const texto = document.getElementById(id).value.trim();
  if (texto === "") return undefined;
  return importe(id, null);
}

function nota(texto) {
  return elemento("p", texto, "nota");
}

function calcular() {
  const metodo = document.getElementById("metodo").value;
  const inicio = document.getElementById("inicio").value;
  bloqueFecha.hidden = metodo !== "directa" || inicio !== "2025";
  for (const bloque of bloquesDirecta) bloque.hidden = metodo !== "directa";

  if (metodo !== "directa") {
    const [titulo, texto] = metodo === "objetiva" ? t.objetiva : t.agraria;
    return mostrar(resultado, total(titulo, "", texto));
  }
  const profesional = document.getElementById("profesional").checked;
  if (profesional) return mostrar(resultado, total(t.retenciones[0], "", t.retenciones[1]), nota(t.convalidacion));
  if (inicio === "despues") return mostrar(resultado, total(t.sinActividad[0], "19 %", t.sinActividad[1]), nota(t.convalidacion));

  const cifra = importe("cifra", null);
  const cuota = importe("cuota");
  const pagos = importe("pagos");
  if (cifra === null || cuota === null || pagos === null) return mostrar(resultado, error(t.error));
  const signo = document.getElementById("signo").value;
  const cuotaDiferencial = signo === "devolver" ? -cuota : signo === "pagar" ? cuota : 0;

  const rendimiento = opcional("rendimiento");
  const estatal = opcional("tipo_estatal");
  const autonomico = opcional("tipo_autonomico");
  if (rendimiento === null || estatal === null || autonomico === null) return mostrar(resultado, error(t.error));
  if ((estatal ?? 0) > 100 || (autonomico ?? 0) > 100) return mostrar(resultado, error(t.errorTipos));

  const r = calcularModelo130En2027({
    metodo,
    inicio,
    fechaInicio: document.getElementById("fecha").value,
    cifraNegocios: cifra,
    cuotaDiferencial,
    pagosFraccionados: pagos,
    profesionalRetenciones70: false,
    rendimientoNeto: rendimiento ?? null,
    tipoMedioEstatal: estatal ?? null,
    tipoMedioAutonomico: autonomico ?? null,
  });
  if (r.caso === "fecha_invalida") return mostrar(resultado, error(t.errorFecha));

  const f = t.filas;
  const filas = [
    fila([r.elevada ? f.cifraElevada(r.dias) : f.cifra, euros.format(r.cifraAnual)]),
    fila([f.menos85, r.cifraAnual < LIMITE_DISPENSA ? f.si : f.no]),
    fila([f.menos250, r.cifraAnual < LIMITE_19 ? f.si : f.no]),
    fila([f.renta, r.aDevolver ? f.devolver(euros.format(-cuotaDiferencial)) : f.noDevolver]),
    fila([f.cubre, r.cubrePagos ? f.si : f.no]),
  ];
  const piezas = r.dispensa
    ? [total(t.dispensa, "", t.dispensaNota), tabla(filas)]
    : [total(t.presenta(r.porcentaje), `${r.porcentaje} %`, t.presentaNota(r.porcentaje)), tabla(filas)];
  if (r.puedeDomiciliar) {
    piezas.push(elemento("h3", t.domiciliar), elemento("p", t.domiciliarTexto));
    if (r.pagoDomiciliado !== null) {
      piezas.push(
        total(t.pago, euros.format(r.pagoDomiciliado), t.pagoNota(numero.format(r.tipoMedio))),
        tabla([
          fila([t.pagoTabla.tipo, `${numero.format(r.tipoMedio)} %`]),
          fila([t.pagoTabla.anual, euros.format(Math.round(r.pagoDomiciliado * 4 * 100) / 100)], true),
        ]),
      );
    } else {
      piezas.push(nota(t.pagoFalta));
    }
  }
  piezas.push(nota(t.convalidacion));
  mostrar(resultado, ...piezas);
}

conectar(calcular);
