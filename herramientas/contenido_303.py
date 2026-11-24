"""Páginas del modelo 303 y de la plantilla de factura, en castellano y en catalán."""
from contenido import BOE_IVA, campo, seleccion
from contenido_extra import PAGINAS as PAGINAS_ANTERIORES

AEAT_303 = "https://sede.agenciatributaria.gob.es/Sede/todas-gestiones/impuestos-tasas/iva/modelo-303-iva-autoliquidacion_/instrucciones-2025.html"
BOE_FACTURACION = "https://www.boe.es/buscar/act.php?id=BOE-A-2012-14696#a6"
AEAT_VERIFACTU = "https://sede.agenciatributaria.gob.es/Sede/iva/sistemas-informaticos-facturacion-verifactu/preguntas-frecuentes/cuestiones-generales-ambitos-aplicacion.html"
BOE_RDL_15_2025 = "https://www.boe.es/buscar/doc.php?id=BOE-A-2025-24446"
# Referencia del Consejo de Ministros del 24-11-2026: real decreto-ley que retrasa Verifactu a octubre de 2028 (aún no estaba en el BOE ese día).
MONCLOA_VERIFACTU = "https://www.lamoncloa.gob.es/consejodeministros/referencias/Paginas/2026/20261124-referencia-rueda-de-consejo-ministros.aspx"


def bases(prefijo, leyenda, lang, valor21=""):
    nombre = {"es": "Base al {t} % (€)", "ca": "Base al {t} % (€)"}[lang]
    campos = []
    for tipo in (21, 10, 4):
        v = valor21 if tipo == 21 else ""
        valor = f' value="{v}"' if v else ""
        campos.append(
            f'        <label for="{prefijo}{tipo}">{nombre.format(t=tipo)}</label>\n'
            f'        <input id="{prefijo}{tipo}" name="{prefijo}{tipo}" type="number" inputmode="decimal" min="0" step="0.01"{valor}>'
        )
    return f"      <fieldset>\n        <legend>{leyenda}</legend>\n" + "\n".join(campos) + "\n      </fieldset>"


def formulario_303(lang):
    if lang == "es":
        cab, trim, ayuda_t, comp, ayuda_c = ("Tus datos del trimestre", "Trimestre", "En el 4T se puede pedir la devolución.",
                                             "Pendiente de trimestres anteriores (€)", "Lo que te quedó «a compensar» antes en el año.")
        nota = "Escribe las bases sin IVA, sumando todas las facturas del trimestre. Si no tienes nada a un tipo, déjalo vacío."
        ventas, gastos = "Ventas (facturas emitidas)", "Gastos con IVA deducible"
        trimestres = [("1", "1T (enero a marzo)"), ("2", "2T (abril a junio)"), ("3", "3T (julio a septiembre)"), ("4", "4T (octubre a diciembre)")]
    else:
        cab, trim, ayuda_t, comp, ayuda_c = ("Les teves dades del trimestre", "Trimestre", "Al 4T es pot demanar la devolució.",
                                             "Pendent de trimestres anteriors (€)", "El que et va quedar «a compensar» abans durant l'any.")
        nota = "Escriu les bases sense IVA, sumant totes les factures del trimestre. Si no tens res a un tipus, deixa-ho buit."
        ventas, gastos = "Vendes (factures emeses)", "Despeses amb IVA deduïble"
        trimestres = [("1", "1T (gener a març)"), ("2", "2T (abril a juny)"), ("3", "3T (juliol a setembre)"), ("4", "4T (octubre a desembre)")]
    return f"""    <h2>{cab}</h2>
    <div class="rejilla">
{seleccion("trimestre", trim, trimestres, ayuda_t)}
{campo("compensar", comp, ayuda_c, "0")}
    </div>
    <p class="nota">{nota}</p>
    <div class="trimestres">
{bases("v", ventas, lang, "10000")}
{bases("g", gastos, lang, "2000")}
    </div>"""


M303_ES = {
    "lang": "es",
    "clave": "m303",
    "script": "modelo303-app.js",
    "titulo": "Calculadora modelo 303 · IVA trimestral de autónomos gratis",
    "descripcion": "Calcula gratis tu modelo 303: IVA repercutido menos IVA soportado, compensación de trimestres anteriores y resultado a ingresar. Toda España.",
    "og_titulo": "Calculadora del modelo 303 (IVA trimestral)",
    "og_descripcion": "Cuánto IVA pagas este trimestre: el de tus facturas menos el de tus gastos.",
    "h1": "Calculadora del modelo 303: el IVA de cada trimestre",
    "entradilla": "Calcula cuánto IVA tienes que pagar este trimestre: el IVA de tus facturas menos el de tus gastos, con lo pendiente de trimestres anteriores. Vale para toda España salvo Canarias, Ceuta, Melilla, País Vasco y Navarra.",
    "formulario": formulario_303("es"),
    "faq": [
        ("¿Qué es el modelo 303?",
         "Es la declaración trimestral del IVA. En ella ingresas a Hacienda la diferencia entre el IVA que has cobrado en tus facturas (IVA repercutido) y el que has pagado en los gastos de tu actividad (IVA soportado)."),
        ("¿Cuándo se presenta el modelo 303?",
         "Del 1 al 20 de abril, julio y octubre, y del 1 al 30 de enero del año siguiente para el cuarto trimestre."),
        ("¿Qué IVA de mis gastos puedo deducir?",
         "Solo el de gastos relacionados con tu actividad y con factura completa a tu nombre. Algunos gastos tienen reglas especiales, como los vehículos, así que consúltalo si tienes dudas."),
        ("¿Qué pasa si me sale negativo?",
         "En los trimestres 1 a 3 queda «a compensar» y lo restas en los siguientes. En el cuarto trimestre puedes pedir que Hacienda te lo devuelva o seguir compensándolo."),
        ("¿Quién no presenta el modelo 303?",
         "Los autónomos que solo hacen operaciones exentas de IVA, como muchos servicios sanitarios o de enseñanza, y los de Canarias, Ceuta y Melilla, que tienen otros impuestos. En el País Vasco y Navarra se presenta ante sus haciendas forales."),
    ],
    "aviso": "es una estimación orientativa y no sustituye el consejo de un asesor fiscal. No incluye prorrata, recargo de equivalencia, criterio de caja, operaciones intracomunitarias ni inversión del sujeto pasivo. Fuentes:",
    "fuentes": [
        ("Instrucciones del modelo 303 (Agencia Tributaria)", AEAT_303),
        ("Ley 37/1992 del IVA, artículos 90 y 91 (BOE)", BOE_IVA),
    ],
}

M303_CA = {
    "lang": "ca",
    "clave": "m303",
    "script": "modelo303-app.js",
    "titulo": "Calculadora model 303 · IVA trimestral d'autònoms gratis",
    "descripcion": "Calcula gratis el teu model 303: IVA repercutit menys IVA suportat, compensació de trimestres anteriors i resultat a ingressar. Tot Espanya.",
    "og_titulo": "Calculadora del model 303 (IVA trimestral)",
    "og_descripcion": "Quant IVA pagues aquest trimestre: el de les teves factures menys el de les despeses.",
    "h1": "Calculadora del model 303: l'IVA de cada trimestre",
    "entradilla": "Calcula quant IVA has de pagar aquest trimestre: l'IVA de les teves factures menys el de les despeses, amb el pendent de trimestres anteriors. Serveix per a tot Espanya excepte les Canàries, Ceuta, Melilla, el País Basc i Navarra.",
    "formulario": formulario_303("ca"),
    "faq": [
        ("Què és el model 303?",
         "És la declaració trimestral de l'IVA. Hi ingresses a Hisenda la diferència entre l'IVA que has cobrat a les factures (IVA repercutit) i el que has pagat a les despeses de l'activitat (IVA suportat)."),
        ("Quan es presenta el model 303?",
         "De l'1 al 20 d'abril, juliol i octubre, i de l'1 al 30 de gener de l'any següent per al quart trimestre."),
        ("Quin IVA de les despeses puc deduir?",
         "Només el de despeses relacionades amb l'activitat i amb factura completa al teu nom. Algunes despeses tenen regles especials, com els vehicles, així que consulta-ho si tens dubtes."),
        ("Què passa si em surt negatiu?",
         "Als trimestres 1 a 3 queda «a compensar» i el restes als següents. Al quart trimestre pots demanar que Hisenda te'l retorni o continuar compensant-lo."),
        ("Qui no presenta el model 303?",
         "Els autònoms que només fan operacions exemptes d'IVA, com molts serveis sanitaris o d'ensenyament, i els de les Canàries, Ceuta i Melilla, que tenen altres impostos. Al País Basc i Navarra es presenta davant les seves hisendes forals."),
    ],
    "aviso": "és una estimació orientativa i no substitueix el consell d'un assessor fiscal. No inclou prorrata, recàrrec d'equivalència, criteri de caixa, operacions intracomunitàries ni inversió del subjecte passiu. Fonts, en castellà:",
    "fuentes": M303_ES["fuentes"],
}


def cuerpo_plantilla(lang):
    raiz = "../" * (2 if lang == "ca" else 1)
    if lang == "es":
        textos = ("Descarga la plantilla", "Elige el formato que uses. Las dos son gratis y no hace falta registrarse.",
                  "Excel", "El IVA, la retención y el total se calculan solos.", "Descargar Excel",
                  "Word", "Para rellenar a mano y guardar en PDF.", "Descargar Word",
                  "Qué incluye", ["Número de factura, fecha de expedición y fecha de la operación.",
                                  "Tus datos y los del cliente: nombre o razón social, NIF y domicilio.",
                                  "Hasta 8 conceptos con cantidad y precio unitario sin IVA.",
                                  "IVA del 21 %, 10 %, 4 % o 0 %, y retención del 15 %, 7 % o 0 %.",
                                  "Forma de pago y notas de uso."],
                  "¿Prefieres calcular primero el total?", "Usa la calculadora de factura", "factura-autonomos/")
        archivo = "factura-autonomo"
    else:
        textos = ("Descarrega la plantilla", "Tria el format que facis servir. Totes dues són gratuïtes i no cal registrar-se.",
                  "Excel", "L'IVA, la retenció i el total es calculen sols.", "Descarregar Excel",
                  "Word", "Per omplir a mà i desar en PDF.", "Descarregar Word",
                  "Què inclou", ["Número de factura, data d'expedició i data de l'operació.",
                                 "Les teves dades i les del client: nom o raó social, NIF i domicili.",
                                 "Fins a 8 conceptes amb quantitat i preu unitari sense IVA.",
                                 "IVA del 21 %, 10 %, 4 % o 0 %, i retenció del 15 %, 7 % o 0 %.",
                                 "Forma de pagament i notes d'ús."],
                  "Prefereixes calcular primer el total?", "Fes servir la calculadora de factura", "ca/factura-autonoms/")
        archivo = "factura-autonom"
    (titulo, intro, x_nombre, x_texto, x_boton, w_nombre, w_texto, w_boton, incluye, lista, pregunta, enlace, ruta_factura) = textos
    items = "".join(f"<li>{x}</li>" for x in lista)
    return f"""<section class="tarjeta">
    <h2>{titulo}</h2>
    <p>{intro}</p>
    <div class="descargas">
      <a class="descarga" href="{raiz}plantillas/{archivo}.xlsx" download>
        <span class="icono" aria-hidden="true">📊</span>
        <span><strong>{x_nombre}</strong><span>{x_texto}</span></span>
        <span class="boton">{x_boton}</span>
      </a>
      <a class="descarga" href="{raiz}plantillas/{archivo}.docx" download>
        <span class="icono" aria-hidden="true">📝</span>
        <span><strong>{w_nombre}</strong><span>{w_texto}</span></span>
        <span class="boton">{w_boton}</span>
      </a>
    </div>
    <h3 class="subtitulo">{incluye}</h3>
    <ul class="lista">{items}</ul>
    <p class="nota">{pregunta} <a href="{raiz}{ruta_factura}">{enlace}</a>.</p>
  </section>"""


PLANTILLA_ES = {
    "lang": "es",
    "clave": "plantilla",
    "script": None,
    "cuerpo": cuerpo_plantilla("es"),
    "titulo": "Plantilla de factura para autónomos gratis · Excel y Word 2026",
    "descripcion": "Descarga gratis una plantilla de factura de autónomo en Excel y Word, con el IVA y la retención de IRPF calculados y todos los datos obligatorios.",
    "og_titulo": "Plantilla de factura para autónomos (Excel y Word)",
    "og_descripcion": "Factura gratis lista para rellenar, con IVA y retención de IRPF.",
    "h1": "Plantilla de factura para autónomos en Excel y Word",
    "entradilla": "Descarga gratis una factura lista para rellenar, con todos los datos que exige la ley. En el Excel, el IVA, la retención de IRPF y el total se calculan solos.",
    "faq": [
        ("¿Qué datos tiene que llevar una factura de autónomo?",
         f'Número y serie correlativos, fecha de expedición, nombre o razón social, NIF y domicilio tuyos y del cliente, descripción de lo que facturas con el precio unitario sin IVA, el tipo de IVA y su cuota, y la fecha de la operación si es distinta, según el <a href="{BOE_FACTURACION}">artículo 6 del Reglamento de facturación</a>.'),
        ("¿Puedo seguir usando Excel o Word con Verifactu?",
         f'Según la <a href="{AEAT_VERIFACTU}">Agencia Tributaria</a>, sí, si los usas solo para escribir, emitir, imprimir y guardar las facturas. Si los usas con macros para generar el libro registro u otras obligaciones fiscales, cuentan como sistema de facturación y deben cumplir Verifactu, obligatorio para los autónomos desde el 1 de julio de 2027 según el <a href="{BOE_RDL_15_2025}">Real Decreto-ley 15/2025</a>. El 24 de noviembre de 2026 el <a href="{MONCLOA_VERIFACTU}">Consejo de Ministros aprobó un real decreto-ley que lo retrasa hasta octubre de 2028</a>. Hasta que se publique en el BOE, sigue valiendo la fecha de 2027. Esta plantilla no lleva macros.'),
        ("¿Tengo que poner la retención de IRPF?",
         "Si eres profesional y facturas a una empresa o a otro autónomo, sí: el 15 %, o el 7 % el año de inicio y los dos siguientes. Si facturas a un particular, o tu actividad es empresarial, normalmente no."),
        ("¿Cómo numero las facturas?",
         "Con una numeración correlativa dentro de cada serie, sin saltos, por ejemplo 2026-001, 2026-002. Las facturas rectificativas van en una serie aparte."),
        ("¿Funciona en Google Sheets o LibreOffice?",
         "Sí. Puedes abrir el Excel en Google Sheets o LibreOffice, y las fórmulas se recalculan al abrirlo."),
    ],
    "aviso": "es una plantilla orientativa y no sustituye el consejo de un asesor fiscal. Revisa que tus facturas incluyan todos los datos que te correspondan. Fuentes:",
    "fuentes": [
        ("Reglamento de facturación (Real Decreto 1619/2012), artículo 6 (BOE)", BOE_FACTURACION),
        ("Verifactu: ámbito de aplicación (Agencia Tributaria)", AEAT_VERIFACTU),
        ("Real Decreto-ley 15/2025 (BOE)", BOE_RDL_15_2025),
        ("Consejo de Ministros del 24 de noviembre de 2026: aplazamiento de Verifactu (La Moncloa)", MONCLOA_VERIFACTU),
    ],
}

PLANTILLA_CA = {
    "lang": "ca",
    "clave": "plantilla",
    "script": None,
    "cuerpo": cuerpo_plantilla("ca"),
    "titulo": "Plantilla de factura per a autònoms gratis · Excel i Word 2026",
    "descripcion": "Descarrega gratis una plantilla de factura d'autònom en Excel i Word, amb l'IVA i la retenció d'IRPF calculats i totes les dades obligatòries.",
    "og_titulo": "Plantilla de factura per a autònoms (Excel i Word)",
    "og_descripcion": "Factura gratuïta llesta per omplir, amb IVA i retenció d'IRPF.",
    "h1": "Plantilla de factura per a autònoms en Excel i Word",
    "entradilla": "Descarrega gratis una factura llesta per omplir, amb totes les dades que exigeix la llei. A l'Excel, l'IVA, la retenció d'IRPF i el total es calculen sols.",
    "faq": [
        ("Quines dades ha de portar una factura d'autònom?",
         f'Número i sèrie correlatius, data d\'expedició, nom o raó social, NIF i domicili teus i del client, descripció del que factures amb el preu unitari sense IVA, el tipus d\'IVA i la quota, i la data de l\'operació si és diferent, segons l\'<a href="{BOE_FACTURACION}">article 6 del Reglament de facturació</a>.'),
        ("Puc continuar fent servir Excel o Word amb Verifactu?",
         f'Segons l\'<a href="{AEAT_VERIFACTU}">Agència Tributària</a>, sí, si els fas servir només per escriure, emetre, imprimir i desar les factures. Si els fas servir amb macros per generar el llibre registre o altres obligacions fiscals, compten com a sistema de facturació i han de complir Verifactu, obligatori per als autònoms des de l\'1 de juliol de 2027 segons el <a href="{BOE_RDL_15_2025}">Reial decret llei 15/2025</a>. El 24 de novembre de 2026 el <a href="{MONCLOA_VERIFACTU}">Consell de Ministres va aprovar un reial decret llei que l\'endarrereix fins a l\'octubre de 2028</a>. Fins que no es publiqui al BOE, continua valent la data del 2027. Aquesta plantilla no porta macros.'),
        ("He de posar la retenció d'IRPF?",
         "Si ets professional i factures a una empresa o a un altre autònom, sí: el 15 %, o el 7 % l'any d'inici i els dos següents. Si factures a un particular, o la teva activitat és empresarial, normalment no."),
        ("Com numero les factures?",
         "Amb una numeració correlativa dins de cada sèrie, sense salts, per exemple 2026-001, 2026-002. Les factures rectificatives van en una sèrie a part."),
        ("Funciona a Google Sheets o LibreOffice?",
         "Sí. Pots obrir l'Excel a Google Sheets o LibreOffice, i les fórmules es recalculen en obrir-lo."),
    ],
    "aviso": "és una plantilla orientativa i no substitueix el consell d'un assessor fiscal. Revisa que les teves factures incloguin totes les dades que et corresponguin. Fonts, en castellà:",
    "fuentes": PLANTILLA_ES["fuentes"],
}

PAGINAS = [*PAGINAS_ANTERIORES, M303_ES, M303_CA, PLANTILLA_ES, PLANTILLA_CA]
