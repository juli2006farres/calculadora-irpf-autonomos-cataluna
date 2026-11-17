"""Textos de las páginas nuevas, en castellano y en catalán."""

BOE_IVA = "https://www.boe.es/buscar/act.php?id=BOE-A-1992-28740#a90"
BOE_RIRPF = "https://www.boe.es/buscar/act.php?id=BOE-A-2007-6820"
BOE_LIRPF = "https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764"
BOE_CUOTA = "https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-7296"
BOE_CAT = "https://www.boe.es/diario_boe/txt.php?id=BOE-A-2025-10270"
AEAT_130 = "https://sede.agenciatributaria.gob.es/Sede/impuestos-tasas/impuesto-sobre-renta-personas-fisicas/modelo-130-irpf______esionales-estimacion-directa-fraccionado_/instrucciones.html"


def campo(id_, etiqueta, ayuda="", valor="", extra=""):
    ayuda_html = f'<span class="ayuda" id="ayuda-{id_}">{ayuda}</span>' if ayuda else ""
    valor_html = f' value="{valor}"' if valor != "" else ""
    return f"""      <div>
        <label for="{id_}">{etiqueta}{ayuda_html}</label>
        <input id="{id_}" name="{id_}" type="number" inputmode="decimal" min="0" step="0.01"{valor_html}{extra}>
      </div>"""


def seleccion(id_, etiqueta, opciones, ayuda=""):
    ops = "\n".join(
        f'          <option value="{v}"{" selected" if i == 0 else ""}>{t}</option>' for i, (v, t) in enumerate(opciones)
    )
    ayuda_html = f'<span class="ayuda">{ayuda}</span>' if ayuda else ""
    return f"""      <div>
        <label for="{id_}">{etiqueta}{ayuda_html}</label>
        <select id="{id_}" name="{id_}">
{ops}
        </select>
      </div>"""


def casilla(id_, etiqueta, ayuda):
    return f"""    <div class="casilla">
      <input id="{id_}" name="{id_}" type="checkbox">
      <label for="{id_}">{etiqueta}<span class="ayuda">{ayuda}</span></label>
    </div>"""


MODALIDAD = {
    "es": [("directa_simplificada", "Directa simplificada"), ("directa_normal", "Directa normal")],
    "ca": [("directa_simplificada", "Directa simplificada"), ("directa_normal", "Directa normal")],
}

# ---------------------------------------------------------------- Factura
FACTURA_ES = {
    "lang": "es",
    "clave": "factura",
    "script": "factura-app.js",
    "titulo": "Calculadora de factura de autónomo con IVA e IRPF · Gratis",
    "descripcion": "Calcula una factura de autónomo con IVA y retención de IRPF del 15 % o 7 %, o cuánto facturar para cobrar una cantidad. Gratis y para toda España.",
    "og_titulo": "Calculadora de factura de autónomo con IVA e IRPF",
    "og_descripcion": "Base, IVA, retención y total de tu factura, o cuánto facturar para cobrar una cantidad.",
    "h1": "Calculadora de factura para autónomos con IVA y retención de IRPF",
    "entradilla": "Calcula el total de tu factura con IVA y retención de IRPF, o al revés: cuánto tienes que facturar para cobrar una cantidad concreta. Vale para toda España.",
    "formulario": f"""    <h2>Datos de la factura</h2>
    <fieldset class="segmentos">
      <legend>¿De qué importe partes?</legend>
      <div class="pastilla">
      <label><input type="radio" name="modo" value="base" checked><span>Precio sin IVA</span></label>
      <label><input type="radio" name="modo" value="cobrar"><span>Lo que quiero cobrar</span></label>
      </div>
    </fieldset>
    <div class="rejilla">
{campo("importe", "Importe (€)", "El precio de tu trabajo, sin IVA.", "1000")}
{seleccion("iva", "IVA", [("21", "21 % (general)"), ("10", "10 % (reducido)"), ("4", "4 % (superreducido)"), ("0", "0 % (exenta o no sujeta)")], "El general es el 21 %.")}
{seleccion("retencion", "Retención de IRPF", [("15", "15 % (profesional)"), ("7", "7 % (nuevo profesional)"), ("0", "Sin retención")], "Sin retención si el cliente es un particular o tu actividad es empresarial.")}
    </div>""",
    "faq": [
        ("¿Qué retención de IRPF pongo en mis facturas?",
         f'Los profesionales aplican un 15 %. Si empiezas una actividad profesional, puedes aplicar un 7 % el año de inicio y los dos siguientes, siempre que no hayas ejercido ninguna actividad profesional el año anterior y se lo comuniques a tu cliente, según el <a href="{BOE_RIRPF}#a95">artículo 95.1 del Reglamento del IRPF</a>.'),
        ("¿Cuándo no hay que poner retención?",
         "En general, cuando el cliente es un particular, porque los particulares no están obligados a retener, y en la mayoría de actividades empresariales, como el comercio o la hostelería. Retienen las empresas y los autónomos que pagan servicios profesionales."),
        ("¿Qué tipo de IVA aplico?",
         "El general es del 21 %. Algunos bienes y servicios llevan el 10 % o el 4 %, y otros están exentos, como muchos servicios sanitarios o de enseñanza. Depende de lo que vendas, así que consúltalo si tienes dudas."),
        ("¿Cómo calculo cuánto facturar para cobrar una cantidad?",
         "Divide lo que quieres cobrar entre 1 + IVA − retención. Por ejemplo, para cobrar 1.060 € con un 21 % de IVA y un 15 % de retención, la base es 1.060 / 1,06 = 1.000 €."),
        ("¿El IVA que cobro es mío?",
         "No. Lo ingresas a Hacienda cada trimestre en el modelo 303, después de restar el IVA de tus gastos de la actividad. La retención tampoco la cobras: la ingresa tu cliente a Hacienda como adelanto de tu IRPF."),
    ],
    "aviso": "es una estimación orientativa y no sustituye el consejo de un asesor fiscal. No incluye otros tipos de retención, como el 1 % de las actividades en módulos, ni el recargo de equivalencia. Fuentes:",
    "fuentes": [
        ("Ley 37/1992 del IVA, artículos 90 y 91 (BOE)", BOE_IVA),
        ("Reglamento del IRPF, artículo 95 (BOE)", BOE_RIRPF + "#a95"),
    ],
}

FACTURA_CA = {
    "lang": "ca",
    "clave": "factura",
    "script": "factura-app.js",
    "titulo": "Calculadora de factura d'autònom amb IVA i IRPF · Gratuïta",
    "descripcion": "Calcula una factura d'autònom amb IVA i retenció d'IRPF del 15 % o el 7 %, o quant facturar per cobrar una quantitat. Gratuïta i per a tot Espanya.",
    "og_titulo": "Calculadora de factura d'autònom amb IVA i IRPF",
    "og_descripcion": "Base, IVA, retenció i total de la teva factura, o quant facturar per cobrar una quantitat.",
    "h1": "Calculadora de factura per a autònoms amb IVA i retenció d'IRPF",
    "entradilla": "Calcula el total de la teva factura amb IVA i retenció d'IRPF, o a l'inrevés: quant has de facturar per cobrar una quantitat concreta. Serveix per a tot Espanya.",
    "formulario": f"""    <h2>Dades de la factura</h2>
    <fieldset class="segmentos">
      <legend>De quin import parteixes?</legend>
      <div class="pastilla">
      <label><input type="radio" name="modo" value="base" checked><span>Preu sense IVA</span></label>
      <label><input type="radio" name="modo" value="cobrar"><span>El que vull cobrar</span></label>
      </div>
    </fieldset>
    <div class="rejilla">
{campo("importe", "Import (€)", "El preu de la teva feina, sense IVA.", "1000")}
{seleccion("iva", "IVA", [("21", "21 % (general)"), ("10", "10 % (reduït)"), ("4", "4 % (superreduït)"), ("0", "0 % (exempta o no subjecta)")], "El general és el 21 %.")}
{seleccion("retencion", "Retenció d'IRPF", [("15", "15 % (professional)"), ("7", "7 % (nou professional)"), ("0", "Sense retenció")], "Sense retenció si el client és un particular o la teva activitat és empresarial.")}
    </div>""",
    "faq": [
        ("Quina retenció d'IRPF poso a les meves factures?",
         f'Els professionals apliquen un 15 %. Si comences una activitat professional, pots aplicar un 7 % l\'any d\'inici i els dos següents, sempre que no hagis exercit cap activitat professional l\'any anterior i ho comuniquis al teu client, segons l\'<a href="{BOE_RIRPF}#a95">article 95.1 del Reglament de l\'IRPF</a>.'),
        ("Quan no s'ha de posar retenció?",
         "En general, quan el client és un particular, perquè els particulars no estan obligats a retenir, i en la majoria d'activitats empresarials, com el comerç o l'hostaleria. Retenen les empreses i els autònoms que paguen serveis professionals."),
        ("Quin tipus d'IVA aplico?",
         "El general és del 21 %. Alguns béns i serveis porten el 10 % o el 4 %, i d'altres estan exempts, com molts serveis sanitaris o d'ensenyament. Depèn del que venguis, així que consulta-ho si tens dubtes."),
        ("Com calculo quant facturar per cobrar una quantitat?",
         "Divideix el que vols cobrar entre 1 + IVA − retenció. Per exemple, per cobrar 1.060 € amb un 21 % d'IVA i un 15 % de retenció, la base és 1.060 / 1,06 = 1.000 €."),
        ("L'IVA que cobro és meu?",
         "No. L'ingresses a Hisenda cada trimestre amb el model 303, després de restar l'IVA de les despeses de l'activitat. La retenció tampoc la cobres: la ingressa el teu client a Hisenda com a avançament del teu IRPF."),
    ],
    "aviso": "és una estimació orientativa i no substitueix el consell d'un assessor fiscal. No inclou altres tipus de retenció, com l'1 % de les activitats en mòduls, ni el recàrrec d'equivalència. Fonts, en castellà:",
    "fuentes": FACTURA_ES["fuentes"],
}

# ---------------------------------------------------------------- Sueldo neto
SUELDO_ES = {
    "lang": "es",
    "clave": "sueldo",
    "script": "sueldo-app.js",
    "titulo": "Calculadora sueldo neto autónomo 2026 en Cataluña · Gratis",
    "descripcion": "Calcula cuánto te queda al mes como autónomo en Cataluña en 2026 tras gastos, cuota de autónomos e IRPF. Gratis, sin registro y con datos oficiales.",
    "og_titulo": "Calculadora de sueldo neto de autónomo 2026",
    "og_descripcion": "Lo que te queda al mes como autónomo en Cataluña tras gastos, cuota e IRPF.",
    "h1": "¿Cuánto te queda como autónomo? Calculadora de sueldo neto 2026",
    "entradilla": "Calcula lo que te queda limpio cada mes después de gastos, cuota de autónomos e IRPF, si vives en Cataluña. La cuota sigue las tablas oficiales de 2026.",
    "formulario": f"""    <h2>Tus previsiones para 2026</h2>
    <div class="rejilla">
{campo("ingresos", "Ingresos anuales (€)", "Lo que prevés facturar en el año, sin IVA.", "40000")}
{campo("gastos", "Gastos deducibles (€)", "Sin contar las cuotas de autónomo.", "5000")}
{campo("cuota", "Cuota de autónomos al mes (€)", "Déjala vacía para usar la cuota mínima de tu tramo.", "", ' placeholder="Mínima de tu tramo"')}
{seleccion("modalidad", "Estimación en el IRPF", MODALIDAD["es"], "La que usas en el IRPF. La más habitual es la simplificada.")}
    </div>
{casilla("inicio", "Acabo de empezar como autónomo", "Reducción del 20 % del IRPF (art. 32.3 de la Ley del IRPF). Márcala solo si no tuviste actividad económica el año anterior al inicio y es tu primer o segundo año con beneficios.")}
{casilla("cliente", "Cumplo los requisitos de la reducción para autónomos dependientes", "Art. 32.2.2.º de la Ley del IRPF: entre otros, un único cliente no vinculado y gastos que no superen el 30 % de los ingresos.")}""",
    "faq": [
        ("¿Cómo se calcula el sueldo neto de un autónomo?",
         "A lo que facturas sin IVA se le restan los gastos de la actividad, la cuota de autónomos y el IRPF del año. El IVA no cuenta, porque lo ingresas a Hacienda."),
        ("¿Cuánto le queda a un autónomo que factura 40.000 € al año?",
         "En Cataluña en 2026, con 5.000 € de gastos y la cuota mínima de su tramo (427,21 € al mes), el IRPF ronda los 5.681 € y le quedan unos 2.016 € al mes en 12 pagas."),
        ("¿Por qué solo vale para Cataluña?",
         "El IRPF tiene una parte autonómica y esta calculadora usa la escala catalana. La cuota de autónomos sí es igual en toda España: puedes calcularla aparte en la calculadora de cuota."),
        ("¿Las retenciones y el modelo 130 cambian lo que me queda?",
         "No. Son adelantos del IRPF: cambian cuándo pagas, no cuánto. El IRPF final se ajusta en la declaración de la renta."),
        ("¿Qué no incluye?",
         "La tarifa plana y otras bonificaciones de la cuota, otras rentas como un sueldo o alquileres, el mínimo por hijos, las deducciones y la tributación conjunta."),
    ],
    "aviso": "es una estimación orientativa y no sustituye el consejo de un asesor fiscal o laboral. Fuentes:",
    "fuentes": [
        ("Cuota de autónomos: Orden PJC/297/2026 (BOE)", BOE_CUOTA),
        ("Ley del IRPF (BOE)", BOE_LIRPF),
        ("Escala catalana: Decreto-ley 5/2025 (BOE)", BOE_CAT),
    ],
}

SUELDO_CA = {
    "lang": "ca",
    "clave": "sueldo",
    "script": "sueldo-app.js",
    "titulo": "Calculadora sou net autònom 2026 a Catalunya · Gratuïta",
    "descripcion": "Calcula quant et queda al mes com a autònom a Catalunya el 2026 després de despeses, quota d'autònoms i IRPF. Gratuïta i amb dades oficials.",
    "og_titulo": "Calculadora de sou net d'autònom 2026",
    "og_descripcion": "El que et queda al mes com a autònom a Catalunya després de despeses, quota i IRPF.",
    "h1": "Quant et queda com a autònom? Calculadora de sou net 2026",
    "entradilla": "Calcula el que et queda net cada mes després de despeses, quota d'autònoms i IRPF, si vius a Catalunya. La quota segueix les taules oficials del 2026.",
    "formulario": f"""    <h2>Les teves previsions per al 2026</h2>
    <div class="rejilla">
{campo("ingresos", "Ingressos anuals (€)", "El que preveus facturar durant l'any, sense IVA.", "40000")}
{campo("gastos", "Despeses deduïbles (€)", "Sense comptar les quotes d'autònom.", "5000")}
{campo("cuota", "Quota d'autònoms al mes (€)", "Deixa-la buida per fer servir la quota mínima del teu tram.", "", ' placeholder="Mínima del teu tram"')}
{seleccion("modalidad", "Estimació a l'IRPF", MODALIDAD["ca"], "La que fas servir a l'IRPF. La més habitual és la simplificada.")}
    </div>
{casilla("inicio", "Acabo de començar com a autònom", "Reducció del 20 % de l'IRPF (art. 32.3 de la Llei de l'IRPF). Marca-la només si no vas tenir activitat econòmica l'any anterior a l'inici i és el teu primer o segon any amb beneficis.")}
{casilla("cliente", "Compleixo els requisits de la reducció per a autònoms dependents", "Art. 32.2.2n de la Llei de l'IRPF: entre d'altres, un únic client no vinculat i despeses que no superin el 30 % dels ingressos.")}""",
    "faq": [
        ("Com es calcula el sou net d'un autònom?",
         "Al que factures sense IVA se li resten les despeses de l'activitat, la quota d'autònoms i l'IRPF de l'any. L'IVA no compta, perquè l'ingresses a Hisenda."),
        ("Quant li queda a un autònom que factura 40.000 € l'any?",
         "A Catalunya el 2026, amb 5.000 € de despeses i la quota mínima del seu tram (427,21 € al mes), l'IRPF és d'uns 5.681 € i li queden uns 2.016 € al mes en 12 pagues."),
        ("Per què només serveix per a Catalunya?",
         "L'IRPF té una part autonòmica i aquesta calculadora fa servir l'escala catalana. La quota d'autònoms sí que és igual a tot Espanya: pots calcular-la a part a la calculadora de quota."),
        ("Les retencions i el model 130 canvien el que em queda?",
         "No. Són avançaments de l'IRPF: canvien quan pagues, no quant. L'IRPF final s'ajusta a la declaració de la renda."),
        ("Què no inclou?",
         "La tarifa plana i altres bonificacions de la quota, altres rendes com un sou o lloguers, el mínim per fills, les deduccions i la tributació conjunta."),
    ],
    "aviso": "és una estimació orientativa i no substitueix el consell d'un assessor fiscal o laboral. Fonts, en castellà:",
    "fuentes": SUELDO_ES["fuentes"],
}

# ---------------------------------------------------------------- Modelo 130


def trimestres(lang):
    nombres = {"es": ("Ingresos", "Gastos", "Retenciones"), "ca": ("Ingressos", "Despeses", "Retencions")}[lang]
    bloques = []
    for n in range(1, 5):
        valores = ("10000", "2000", "0") if n == 1 else ("", "", "")
        campos = "\n".join(
            f'        <label for="{p}{n}">{nombre} (€)</label>\n'
            f'        <input id="{p}{n}" name="{p}{n}" type="number" inputmode="decimal" min="0" step="0.01"{f" value={chr(34)}{v}{chr(34)}" if v else ""}>'
            for p, nombre, v in zip(("i", "g", "r"), nombres, valores)
        )
        bloques.append(f"      <fieldset>\n        <legend>{n}T</legend>\n{campos}\n      </fieldset>")
    return '    <div class="trimestres">\n' + "\n".join(bloques) + "\n    </div>"


M130_ES = {
    "lang": "es",
    "clave": "m130",
    "script": "modelo130-app.js",
    "apilada": True,
    "titulo": "Calculadora modelo 130 · Pago fraccionado del IRPF gratis",
    "descripcion": "Calcula gratis tus pagos trimestrales del modelo 130: 20 % del rendimiento acumulado, menos pagos anteriores, retenciones y minoración. Toda España.",
    "og_titulo": "Calculadora del modelo 130",
    "og_descripcion": "Cuánto pagar en cada modelo 130 del año, trimestre a trimestre.",
    "h1": "Calculadora del modelo 130: el pago trimestral del IRPF",
    "entradilla": "Calcula cuánto pagar en cada modelo 130 del año. Escribe los ingresos, gastos y retenciones de cada trimestre y verás las casillas principales. Vale para toda España, salvo el País Vasco y Navarra, que tienen sus propios modelos.",
    "formulario": f"""    <h2>Tus datos del año</h2>
    <div class="rejilla">
{seleccion("modalidad", "Estimación directa", MODALIDAD["es"], "En simplificada se suman los gastos de difícil justificación.")}
{seleccion("anterior", "Rendimiento neto del año anterior", [("mas", "Más de 12.000 €"), ("9000", "Hasta 9.000 €"), ("10000", "De 9.000 a 10.000 €"), ("11000", "De 10.000 a 11.000 €"), ("12000", "De 11.000 a 12.000 €")], "De todas tus actividades. Si es bajo, pagas algo menos cada trimestre.")}
    </div>
    <p class="nota">Escribe lo de cada trimestre por separado, sin acumular. Los gastos incluyen las cuotas de autónomo. Deja vacíos los trimestres que aún no han llegado.</p>
{trimestres("es")}""",
    "faq": [
        ("¿Quién tiene que presentar el modelo 130?",
         f'Los autónomos en estimación directa, salvo los profesionales que el año anterior tuvieron retención en al menos el 70 % de sus ingresos, según el <a href="{BOE_RIRPF}#a109">artículo 109 del Reglamento del IRPF</a>. Si empiezas la actividad, cuenta el porcentaje del propio trimestre.'),
        ("¿Cómo se calcula el modelo 130?",
         "Se aplica el 20 % al rendimiento neto acumulado desde el 1 de enero y se restan los pagos de los trimestres anteriores y las retenciones del año. Por eso cada trimestre se calcula con lo acumulado y no solo con lo de ese trimestre."),
        ("¿Qué es la minoración por rendimientos bajos?",
         f'Si el rendimiento neto de tus actividades del año anterior fue de 12.000 € o menos, restas entre 25 € y 100 € cada trimestre, según el <a href="{BOE_RIRPF}#a110">artículo 110.3.c del Reglamento del IRPF</a>. Lo que no puedas restar pasa a los trimestres siguientes del mismo año.'),
        ("¿Qué pasa si me sale negativo?",
         "Ese trimestre no pagas nada. Si el negativo viene de la minoración, lo restas en los trimestres siguientes del año. En el cuarto trimestre se presenta como negativa y ya no se traslada."),
        ("¿Cuándo se presenta?",
         "Del 1 al 20 de abril, julio y octubre, y del 1 al 30 de enero del año siguiente para el cuarto trimestre."),
        ("¿Se incluyen los gastos de difícil justificación?",
         "Sí. En estimación directa simplificada se suman a los gastos de la casilla 02, como indican las instrucciones de la AEAT: un 5 % del rendimiento, con un máximo de 2.000 € al año."),
    ],
    "aviso": "es una estimación orientativa y no sustituye el consejo de un asesor fiscal. No incluye la estimación objetiva (módulos, modelo 131), las actividades agrícolas, la deducción por vivienda ni las declaraciones complementarias. Fuentes:",
    "fuentes": [
        ("Reglamento del IRPF, artículos 109 y 110 (BOE)", BOE_RIRPF + "#a110"),
        ("Instrucciones del modelo 130 (Agencia Tributaria)", AEAT_130),
    ],
}

M130_CA = {
    "lang": "ca",
    "clave": "m130",
    "script": "modelo130-app.js",
    "apilada": True,
    "titulo": "Calculadora model 130 · Pagament fraccionat de l'IRPF gratis",
    "descripcion": "Calcula gratis els teus pagaments trimestrals del model 130: 20 % del rendiment acumulat, menys pagaments anteriors, retencions i minoració.",
    "og_titulo": "Calculadora del model 130",
    "og_descripcion": "Quant pagar en cada model 130 de l'any, trimestre a trimestre.",
    "h1": "Calculadora del model 130: el pagament trimestral de l'IRPF",
    "entradilla": "Calcula quant pagar en cada model 130 de l'any. Escriu els ingressos, les despeses i les retencions de cada trimestre i veuràs les caselles principals. Serveix per a tot Espanya, excepte el País Basc i Navarra, que tenen els seus propis models.",
    "formulario": f"""    <h2>Les teves dades de l'any</h2>
    <div class="rejilla">
{seleccion("modalidad", "Estimació directa", MODALIDAD["ca"], "En simplificada se sumen les despeses de difícil justificació.")}
{seleccion("anterior", "Rendiment net de l'any anterior", [("mas", "Més de 12.000 €"), ("9000", "Fins a 9.000 €"), ("10000", "De 9.000 a 10.000 €"), ("11000", "De 10.000 a 11.000 €"), ("12000", "D'11.000 a 12.000 €")], "De totes les teves activitats. Si és baix, pagues una mica menys cada trimestre.")}
    </div>
    <p class="nota">Escriu el de cada trimestre per separat, sense acumular. Les despeses inclouen les quotes d'autònom. Deixa buits els trimestres que encara no han arribat.</p>
{trimestres("ca")}""",
    "faq": [
        ("Qui ha de presentar el model 130?",
         f'Els autònoms en estimació directa, excepte els professionals que l\'any anterior van tenir retenció en almenys el 70 % dels seus ingressos, segons l\'<a href="{BOE_RIRPF}#a109">article 109 del Reglament de l\'IRPF</a>. Si comences l\'activitat, compta el percentatge del mateix trimestre.'),
        ("Com es calcula el model 130?",
         "S'aplica el 20 % al rendiment net acumulat des de l'1 de gener i es resten els pagaments dels trimestres anteriors i les retencions de l'any. Per això cada trimestre es calcula amb l'acumulat i no només amb el d'aquell trimestre."),
        ("Què és la minoració per rendiments baixos?",
         f'Si el rendiment net de les teves activitats de l\'any anterior va ser de 12.000 € o menys, restes entre 25 € i 100 € cada trimestre, segons l\'<a href="{BOE_RIRPF}#a110">article 110.3.c del Reglament de l\'IRPF</a>. El que no puguis restar passa als trimestres següents del mateix any.'),
        ("Què passa si em surt negatiu?",
         "Aquell trimestre no pagues res. Si el negatiu ve de la minoració, el restes als trimestres següents de l'any. Al quart trimestre es presenta com a negativa i ja no es trasllada."),
        ("Quan es presenta?",
         "De l'1 al 20 d'abril, juliol i octubre, i de l'1 al 30 de gener de l'any següent per al quart trimestre."),
        ("S'hi inclouen les despeses de difícil justificació?",
         "Sí. En estimació directa simplificada se sumen a les despeses de la casella 02, com indiquen les instruccions de l'AEAT: un 5 % del rendiment, amb un màxim de 2.000 € l'any."),
    ],
    "aviso": "és una estimació orientativa i no substitueix el consell d'un assessor fiscal. No inclou l'estimació objectiva (mòduls, model 131), les activitats agrícoles, la deducció per habitatge ni les declaracions complementàries. Fonts, en castellà:",
    "fuentes": M130_ES["fuentes"],
}

PAGINAS = [FACTURA_ES, FACTURA_CA, SUELDO_ES, SUELDO_CA, M130_ES, M130_CA]
