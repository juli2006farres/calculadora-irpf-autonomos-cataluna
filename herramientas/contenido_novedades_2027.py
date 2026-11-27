"""Novedades de 2027 del Real Decreto-ley 43/2026: modelo 130 (dispensa, 19 % y pago domiciliado) e IVA anual."""
from contenido import BOE_LIRPF, BOE_RDL_43_2026, BOE_RIRPF, campo, casilla, seleccion
from contenido_regularizacion import PAGINAS as PAGINAS_ANTERIORES

BOE_LIVA = "https://www.boe.es/buscar/act.php?id=BOE-A-1992-28740"
BOE_RIVA = "https://www.boe.es/buscar/act.php?id=BOE-A-1992-28925"
RDL = ("Real Decreto-ley 43/2026, artículos 2 y 3 (BOE)", BOE_RDL_43_2026)


def fecha(id_, etiqueta, ayuda, valor, minimo, maximo):
    return f"""      <div id="bloque-{id_}">
        <label for="{id_}">{etiqueta}<span class="ayuda">{ayuda}</span></label>
        <input id="{id_}" name="{id_}" type="date" value="{valor}" min="{minimo}" max="{maximo}">
      </div>"""


# ---------------------------------------------------------------- Modelo 130 en 2027
def formulario_130(lang):
    if lang == "es":
        metodo = seleccion("metodo", "Cómo calculas tu rendimiento", [
            ("directa", "Estimación directa (normal o simplificada)"),
            ("objetiva", "Estimación objetiva (módulos)"),
            ("agraria", "Actividad agrícola, ganadera, forestal o pesquera"),
        ], "La mayoría de autónomos está en directa simplificada.")
        inicio = seleccion("inicio", "Cuándo empezaste la actividad", [
            ("antes", "Antes de 2025"), ("2025", "Durante 2025"), ("despues", "En 2026 o después"),
        ])
        fecha_html = fecha("fecha", "Día en que empezaste", "Para elevar al año lo que facturaste en 2025.", "2025-03-01", "2025-01-01", "2025-12-31")
        cifra = campo("cifra", "Ingresos de la actividad en 2025 (€)", "Tu cifra de negocios: lo que facturaste en 2025, sin IVA.", "30000")
        signo = seleccion("signo", "Resultado de tu renta de 2025", [("devolver", "A devolver"), ("pagar", "A pagar"), ("cero", "Cero")])
        cuota = campo("cuota", "Cuota diferencial (€)", "En la declaración aparece como «Cuota diferencial». Suele coincidir con el resultado, salvo si cobras deducciones por maternidad, familia numerosa o discapacidad.", "600")
        pagos = campo("pagos", "Pagos del modelo 130 de 2025 (€)", "La suma de lo que ingresaste en los cuatro trimestres de 2025.", "400")
        prof = casilla("profesional", "Soy profesional y en 2026 al menos el 70 % de mis ingresos tuvo retención", "En ese caso ya no tenías que presentar el modelo 130, y sigue igual.")
        opcional = ("Para el pago domiciliado (opcional)", "Rendimiento neto de la actividad en 2025 (€)", "Lo que te quedó en 2025 tras los gastos, según tu declaración.",
                    "Tipo medio estatal de 2025 (%)", "Aparece en tu declaración de la renta.", "Tipo medio autonómico de 2025 (%)", "Aparece en tu declaración de la renta.")
        titulo = "Tus datos de la renta de 2025"
    else:
        metodo = seleccion("metodo", "Com calcules el teu rendiment", [
            ("directa", "Estimació directa (normal o simplificada)"),
            ("objetiva", "Estimació objectiva (mòduls)"),
            ("agraria", "Activitat agrícola, ramadera, forestal o pesquera"),
        ], "La majoria d'autònoms és en directa simplificada.")
        inicio = seleccion("inicio", "Quan vas començar l'activitat", [
            ("antes", "Abans del 2025"), ("2025", "Durant el 2025"), ("despues", "El 2026 o després"),
        ])
        fecha_html = fecha("fecha", "Dia que vas començar", "Per elevar a l'any el que vas facturar el 2025.", "2025-03-01", "2025-01-01", "2025-12-31")
        cifra = campo("cifra", "Ingressos de l'activitat el 2025 (€)", "La teva xifra de negocis: el que vas facturar el 2025, sense IVA.", "30000")
        signo = seleccion("signo", "Resultat de la teva renda del 2025", [("devolver", "A retornar"), ("pagar", "A pagar"), ("cero", "Zero")])
        cuota = campo("cuota", "Quota diferencial (€)", "A la declaració apareix com a «Quota diferencial». Sol coincidir amb el resultat, llevat que cobris deduccions per maternitat, família nombrosa o discapacitat.", "600")
        pagos = campo("pagos", "Pagaments del model 130 del 2025 (€)", "La suma del que vas ingressar els quatre trimestres del 2025.", "400")
        prof = casilla("profesional", "Soc professional i el 2026 almenys el 70 % dels meus ingressos va tenir retenció", "En aquest cas ja no havies de presentar el model 130, i continua igual.")
        opcional = ("Per al pagament domiciliat (opcional)", "Rendiment net de l'activitat el 2025 (€)", "El que et va quedar el 2025 després de les despeses, segons la teva declaració.",
                    "Tipus mitjà estatal del 2025 (%)", "Apareix a la teva declaració de la renda.", "Tipus mitjà autonòmic del 2025 (%)", "Apareix a la teva declaració de la renda.")
        titulo = "Les teves dades de la renda del 2025"
    sub, rend, rend_a, est, est_a, aut, aut_a = opcional
    return f"""    <h2>{titulo}</h2>
    <div class="rejilla">
{metodo}
    </div>
    <div class="solo-directa">
    <div class="rejilla">
{inicio}
{fecha_html}
{cifra}
{signo}
{cuota}
{pagos}
    </div>
{prof}
    <h3>{sub}</h3>
    <div class="rejilla">
{campo("rendimiento", rend, rend_a)}
{campo("tipo_estatal", est, est_a, "", ' max="100"')}
{campo("tipo_autonomico", aut, aut_a, "", ' max="100"')}
    </div>
    </div>"""


FUENTES_130 = [
    RDL,
    ("Ley del IRPF, artículo 101.11: porcentajes de los pagos fraccionados (BOE)", BOE_LIRPF + "#a101"),
    ("Reglamento del IRPF, artículos 109 y 110: dispensa y cálculo de los pagos fraccionados (BOE)", BOE_RIRPF + "#a109"),
]

CONVALIDACION_ES = f'Es una norma del <a href="{BOE_RDL_43_2026}">Real Decreto-ley 43/2026</a>, en vigor desde el 26 de noviembre de 2026. El Congreso tiene que convalidarlo en los 30 días siguientes; si no lo hiciera, estas novedades decaerían. Actualizaremos esta página en cuanto se publique la decisión en el BOE.'
CONVALIDACION_CA = f'És una norma del <a href="{BOE_RDL_43_2026}">Reial decret llei 43/2026</a>, en vigor des del 26 de novembre de 2026. El Congrés l\'ha de convalidar en els 30 dies següents; si no ho fes, aquestes novetats decaurien. Actualitzarem aquesta pàgina tan aviat com es publiqui la decisió al BOE.'

M130_2027_ES = {
    "lang": "es",
    "clave": "m130_2027",
    "script": "modelo130-2027-app.js",
    "formulario": formulario_130("es"),
    "titulo": "Modelo 130 en 2027: ¿tienes que presentarlo? · Calculadora",
    "descripcion": "Comprueba gratis si en 2027 te libras del modelo 130, si pagarás el 19 % o el 20 % y si puedes pedir el pago domiciliado (Real Decreto-ley 43/2026).",
    "og_titulo": "Modelo 130 en 2027: dispensa, 19 % y pago domiciliado",
    "og_descripcion": "Si en 2027 tienes que presentar el modelo 130 y con qué porcentaje, según tu renta de 2025.",
    "h1": "Modelo 130 en 2027: ¿tienes que presentarlo y con qué porcentaje?",
    "entradilla": "Desde 2027 muchos autónomos en estimación directa pagan el 19 % en vez del 20 %, y algunos ya no tienen que presentar el modelo 130. Con los datos de tu renta de 2025 te digo qué te toca.",
    "faq": [
        ("¿Qué cambia en el modelo 130 en 2027?",
         f'Con el <a href="{BOE_RDL_43_2026}">Real Decreto-ley 43/2026</a>, desde 2027 el pago fraccionado de la estimación directa baja del 20 % al 19 % si tu cifra de negocios de 2025 fue inferior a 250.000 €; si en 2025 no tenías la actividad, también es el 19 %. Además, algunos autónomos dejan de estar obligados a presentarlo y otros pueden pedir que Hacienda les cargue una cantidad fija cada trimestre.'),
        ("¿Quién no tiene que presentar el modelo 130 en 2027?",
         f'Quien está en estimación directa y cumple dos condiciones, según el <a href="{BOE_RIRPF}#a109">artículo 109.2 del Reglamento del IRPF</a>: que su cifra de negocios de 2025 fuera inferior a 85.000 € (elevada al año si empezó en 2025) y que su renta de 2025 saliera con una cuota diferencial negativa, a devolver, igual o mayor que lo que pagó con el modelo 130 ese año. La idea es no adelantar dinero que luego Hacienda tendría que devolver. Además, los profesionales que en el año anterior tuvieron retención en al menos el 70 % de sus ingresos siguen sin tener que presentarlo.'),
        ("¿Por qué se mira la renta de 2025 y no la de 2026?",
         "Porque la norma usa la última declaración cuyo plazo terminó antes del primer pago fraccionado del año. Para 2027 es la renta de 2025, que se presentaba hasta el 30 de junio de 2026. La de 2026 se presenta a partir de abril de 2027, a la vez que el primer modelo 130."),
        ("¿Qué es el pago domiciliado del modelo 130?",
         f'Si tu cifra de negocios de 2025 fue inferior a 250.000 € y tu renta de 2025 salió a devolver después de haber pagado el modelo 130, puedes optar por un sistema nuevo (<a href="{BOE_RIRPF}#a110">artículo 110.5 del Reglamento del IRPF</a>): cada trimestre pagas el 25 % de tu rendimiento neto de 2025 multiplicado por la suma de tus tipos medios estatal y autonómico de 2025. No presentas el modelo: Hacienda te enseña el importe en su sede electrónica en los cinco primeros días de cada plazo y lo carga en tu cuenta el último día. Para 2027 se pide en marzo de 2027 con la declaración censal; en los años siguientes, en diciembre. Se mantiene cada año mientras cumplas los requisitos y no renuncies.'),
        ("¿Dónde veo la cuota diferencial y los tipos medios?",
         "En tu declaración de la renta de 2025. La cuota diferencial es lo que sale después de restar las retenciones y los pagos fraccionados: si es negativa, es a devolver. Los tipos medios de gravamen estatal y autonómico aparecen en el cálculo de la cuota de la declaración."),
        ("¿Esto ya es definitivo?", CONVALIDACION_ES),
    ],
    "aviso": "es una estimación orientativa y no sustituye a la Agencia Tributaria ni a un asesor. Vale para autónomos personas físicas en estimación directa; no tiene en cuenta la reducción del 60 % de Ceuta y Melilla. Fuentes:",
    "fuentes": FUENTES_130,
}

M130_2027_CA = {
    "lang": "ca",
    "clave": "m130_2027",
    "script": "modelo130-2027-app.js",
    "formulario": formulario_130("ca"),
    "titulo": "Model 130 el 2027: l'has de presentar? · Calculadora",
    "descripcion": "Comprova gratis si el 2027 et lliures del model 130, si pagaràs el 19 % o el 20 % i si pots demanar el pagament domiciliat (RDL 43/2026).",
    "og_titulo": "Model 130 el 2027: dispensa, 19 % i pagament domiciliat",
    "og_descripcion": "Si el 2027 has de presentar el model 130 i amb quin percentatge, segons la teva renda del 2025.",
    "h1": "Model 130 el 2027: l'has de presentar i amb quin percentatge?",
    "entradilla": "Des del 2027 molts autònoms en estimació directa paguen el 19 % en lloc del 20 %, i alguns ja no han de presentar el model 130. Amb les dades de la teva renda del 2025 et dic què et toca.",
    "faq": [
        ("Què canvia en el model 130 el 2027?",
         f'Amb el <a href="{BOE_RDL_43_2026}">Reial decret llei 43/2026</a>, des del 2027 el pagament fraccionat de l\'estimació directa baixa del 20 % al 19 % si la teva xifra de negocis del 2025 va ser inferior a 250.000 €; si el 2025 no tenies l\'activitat, també és el 19 %. A més, alguns autònoms deixen d\'estar obligats a presentar-lo i d\'altres poden demanar que Hisenda els carregui una quantitat fixa cada trimestre.'),
        ("Qui no ha de presentar el model 130 el 2027?",
         f'Qui és en estimació directa i compleix dues condicions, segons l\'<a href="{BOE_RIRPF}#a109">article 109.2 del Reglament de l\'IRPF</a>: que la seva xifra de negocis del 2025 fos inferior a 85.000 € (elevada a l\'any si va començar el 2025) i que la seva renda del 2025 sortís amb una quota diferencial negativa, a retornar, igual o més gran que el que va pagar amb el model 130 aquell any. La idea és no avançar diners que després Hisenda hauria de retornar. A més, els professionals que l\'any anterior van tenir retenció en almenys el 70 % dels seus ingressos continuen sense haver-lo de presentar.'),
        ("Per què es mira la renda del 2025 i no la del 2026?",
         "Perquè la norma fa servir l'última declaració el termini de la qual va acabar abans del primer pagament fraccionat de l'any. Per al 2027 és la renda del 2025, que es presentava fins al 30 de juny de 2026. La del 2026 es presenta a partir d'abril del 2027, alhora que el primer model 130."),
        ("Què és el pagament domiciliat del model 130?",
         f'Si la teva xifra de negocis del 2025 va ser inferior a 250.000 € i la teva renda del 2025 va sortir a retornar després d\'haver pagat el model 130, pots optar per un sistema nou (<a href="{BOE_RIRPF}#a110">article 110.5 del Reglament de l\'IRPF</a>): cada trimestre pagues el 25 % del teu rendiment net del 2025 multiplicat per la suma dels teus tipus mitjans estatal i autonòmic del 2025. No presentes el model: Hisenda t\'ensenya l\'import a la seu electrònica els cinc primers dies de cada termini i el carrega al teu compte l\'últim dia. Per al 2027 es demana el març del 2027 amb la declaració censal; els anys següents, el desembre. Es manté cada any mentre compleixis els requisits i no hi renunciïs.'),
        ("On veig la quota diferencial i els tipus mitjans?",
         "A la teva declaració de la renda del 2025. La quota diferencial és el que surt després de restar les retencions i els pagaments fraccionats: si és negativa, és a retornar. Els tipus mitjans de gravamen estatal i autonòmic apareixen en el càlcul de la quota de la declaració."),
        ("Això ja és definitiu?", CONVALIDACION_CA),
    ],
    "aviso": "és una estimació orientativa i no substitueix l'Agència Tributària ni un assessor. Serveix per a autònoms persones físiques en estimació directa; no té en compte la reducció del 60 % de Ceuta i Melilla. Fonts, en castellà:",
    "fuentes": FUENTES_130,
}


# ---------------------------------------------------------------- IVA anual en 2027
def formulario_iva(lang):
    if lang == "es":
        titular = seleccion("titular", "Quién factura", [
            ("persona", "Autónomo persona física"),
            ("atribucion_fisicas", "Comunidad de bienes o sociedad civil con todos los socios personas físicas"),
            ("sociedad", "Sociedad (S.L., S.A., cooperativa…)"),
        ])
        inicio = seleccion("inicio", "Cuándo empezaste la actividad", [("antes", "Antes de 2026"), ("2026", "Durante 2026"), ("2027", "En 2027")])
        regimen = seleccion("regimen", "Régimen de IVA en 2026", [
            ("general", "Régimen general"),
            ("criterio_caja", "Criterio de caja"),
            ("redeme_voluntario", "Devolución mensual (REDEME)"),
            ("simplificado", "Régimen simplificado (módulos)"),
            ("recargo", "Recargo de equivalencia (comercio minorista)"),
        ], "Casi todos los autónomos están en el régimen general.")
        fecha_html = fecha("fecha", "Día en que empezaste", "Para elevar al año lo que facturaste en 2026.", "2026-03-01", "2026-01-01", "2026-12-31")
        volumen = campo("volumen", "Lo que facturaste en 2026, sin IVA (€)", "Tu volumen de operaciones del año.", "40000")
        repercutido = campo("repercutido", "IVA cobrado en 2026 (€)", "El IVA de tus facturas, sumando los cuatro modelos 303.", "8400")
        soportado = campo("soportado", "IVA deducible de 2026 (€)", "El IVA de tus gastos que te dedujiste, sumando los cuatro modelos 303.", "2400")
        previsto = campo("previsto", "IVA que prevés pagar en 2027 (€), opcional", "Si lo dejas vacío, uso el de 2026.")
        titulo = "Tus datos"
    else:
        titular = seleccion("titular", "Qui factura", [
            ("persona", "Autònom persona física"),
            ("atribucion_fisicas", "Comunitat de béns o societat civil amb tots els socis persones físiques"),
            ("sociedad", "Societat (S.L., S.A., cooperativa…)"),
        ])
        inicio = seleccion("inicio", "Quan vas començar l'activitat", [("antes", "Abans del 2026"), ("2026", "Durant el 2026"), ("2027", "El 2027")])
        regimen = seleccion("regimen", "Règim d'IVA el 2026", [
            ("general", "Règim general"),
            ("criterio_caja", "Criteri de caixa"),
            ("redeme_voluntario", "Devolució mensual (REDEME)"),
            ("simplificado", "Règim simplificat (mòduls)"),
            ("recargo", "Recàrrec d'equivalència (comerç minorista)"),
        ], "Gairebé tots els autònoms són en el règim general.")
        fecha_html = fecha("fecha", "Dia que vas començar", "Per elevar a l'any el que vas facturar el 2026.", "2026-03-01", "2026-01-01", "2026-12-31")
        volumen = campo("volumen", "El que vas facturar el 2026, sense IVA (€)", "El teu volum d'operacions de l'any.", "40000")
        repercutido = campo("repercutido", "IVA cobrat el 2026 (€)", "L'IVA de les teves factures, sumant els quatre models 303.", "8400")
        soportado = campo("soportado", "IVA deduïble del 2026 (€)", "L'IVA de les teves despeses que et vas deduir, sumant els quatre models 303.", "2400")
        previsto = campo("previsto", "IVA que preveus pagar el 2027 (€), opcional", "Si el deixes buit, faig servir el del 2026.")
        titulo = "Les teves dades"
    return f"""    <h2>{titulo}</h2>
    <div class="rejilla">
{titular}
{inicio}
{regimen}
{fecha_html}
    </div>
    <div class="solo-con-2026">
    <div class="rejilla">
{volumen}
{repercutido}
{soportado}
    </div>
    </div>
    <div class="rejilla">
{previsto}
    </div>"""


FUENTES_IVA = [
    RDL,
    ("Ley del IVA: régimen especial de declaración anual, artículos 163 novovicies a 163 duotricies (BOE)", BOE_LIVA),
    ("Reglamento del IVA: artículos 33, 61 octodecies y 71, y disposición transitoria séptima (BOE)", BOE_RIVA),
]

IVA_ANUAL_ES = {
    "lang": "es",
    "clave": "iva_anual",
    "script": "iva-anual-app.js",
    "formulario": formulario_iva("es"),
    "titulo": "IVA anual para autónomos 2027 · ¿Puedes y cuánto pagarías?",
    "descripcion": "Comprueba gratis si puedes pasar al IVA anual en 2027 y calcula tus tres pagos a cuenta de abril, julio y octubre, según el Real Decreto-ley 43/2026.",
    "og_titulo": "Calculadora del IVA anual para autónomos 2027",
    "og_descripcion": "Si puedes acogerte al IVA anual en 2027 y cuánto pagarías en abril, julio, octubre y enero.",
    "h1": "IVA anual para autónomos en 2027: ¿puedes acogerte y cuánto pagarías?",
    "entradilla": "Desde 2027, los autónomos que facturan hasta 85.000 € pueden cambiar los cuatro modelos 303 por una declaración al año y tres pagos fijos. Comprueba si puedes y cuánto te cargarían.",
    "faq": [
        ("¿Qué es el IVA anual para autónomos?",
         f'Es un régimen especial voluntario que crea el <a href="{BOE_RDL_43_2026}">Real Decreto-ley 43/2026</a> desde 2027. En lugar de cuatro modelos 303, presentas una sola declaración del IVA del año, del 1 al 30 de enero del año siguiente, y pagas a cuenta tres cantidades fijas que Hacienda te carga en la cuenta el 20 de abril, el 20 de julio y el 20 de octubre. En la declaración anual se restan esos pagos y pagas lo que falte o te devuelven lo que sobre.'),
        ("¿Quién puede acogerse?",
         "Los autónomos personas físicas, y las comunidades de bienes o sociedades civiles cuyos socios sean todos personas físicas, si su volumen de operaciones del año anterior no pasó de 85.000 € (elevado al año si empezaron ese año). Quien empieza la actividad puede pedirlo desde el principio. No pueden quienes están en el régimen simplificado, el criterio de caja, el grupo de entidades, la cuenta corriente tributaria o la liquidación mensual, salvo si es solo por estar en la devolución mensual (REDEME), que se deja al optar. Para 2027, en la misma solicitud se puede renunciar a los regímenes incompatibles."),
        ("¿Cómo se calculan los pagos a cuenta?",
         "Cada pago es la cuarta parte del IVA a pagar del año anterior. El primer año se toma la suma de los modelos 303 del año anterior presentados antes de que acabe marzo. Si esa cantidad no es positiva, o si acabas de empezar la actividad, los pagos son cero. Con tres pagos adelantas tres cuartas partes y el resto se paga en enero. Hacienda te enseña cada importe en su sede electrónica en los cinco primeros días de abril, julio y octubre."),
        ("¿Cuándo y cómo se pide?",
         "Para 2027, durante el mes de marzo de 2027, con la declaración censal e indicando la cuenta bancaria para los cargos. Después, en diciembre para el año siguiente o al darte de alta. Se mantiene cada año hasta que renuncies; la renuncia se hace en diciembre y dura al menos tres años. Si un año pasas de 85.000 €, sales del régimen al año siguiente."),
        ("¿Me conviene?",
         "A favor: haces una declaración en vez de cuatro y los pagos son fijos y automáticos. En contra: los pagos se basan en el año anterior aunque este año factures menos (lo recuperas en enero), no se pueden aplazar ni fraccionar, la renuncia dura al menos tres años y, si estabas en el criterio de caja o en la devolución mensual, pierdes sus ventajas. Si tu IVA suele salir a devolver, tus pagos a cuenta serían cero."),
        ("¿Esto ya es definitivo?", CONVALIDACION_ES),
    ],
    "aviso": "es una estimación orientativa y no sustituye a la Agencia Tributaria ni a un asesor. Toma como IVA de 2026 lo cobrado menos lo deducible de tus modelos 303; Hacienda calculará el importe exacto. Fuentes:",
    "fuentes": FUENTES_IVA,
}

IVA_ANUAL_CA = {
    "lang": "ca",
    "clave": "iva_anual",
    "script": "iva-anual-app.js",
    "formulario": formulario_iva("ca"),
    "titulo": "IVA anual per a autònoms 2027 · Hi pots optar i quant pagaries?",
    "descripcion": "Comprova gratis si pots passar a l'IVA anual el 2027 i calcula els teus tres pagaments a compte d'abril, juliol i octubre (Reial decret llei 43/2026).",
    "og_titulo": "Calculadora de l'IVA anual per a autònoms 2027",
    "og_descripcion": "Si et pots acollir a l'IVA anual el 2027 i quant pagaries a l'abril, el juliol, l'octubre i el gener.",
    "h1": "IVA anual per a autònoms el 2027: t'hi pots acollir i quant pagaries?",
    "entradilla": "Des del 2027, els autònoms que facturen fins a 85.000 € poden canviar els quatre models 303 per una declaració a l'any i tres pagaments fixos. Comprova si pots i quant et carregarien.",
    "faq": [
        ("Què és l'IVA anual per a autònoms?",
         f'És un règim especial voluntari que crea el <a href="{BOE_RDL_43_2026}">Reial decret llei 43/2026</a> des del 2027. En lloc de quatre models 303, presentes una sola declaració de l\'IVA de l\'any, de l\'1 al 30 de gener de l\'any següent, i pagues a compte tres quantitats fixes que Hisenda et carrega al compte el 20 d\'abril, el 20 de juliol i el 20 d\'octubre. A la declaració anual es resten aquests pagaments i pagues el que falti o et retornen el que sobri.'),
        ("Qui s'hi pot acollir?",
         "Els autònoms persones físiques, i les comunitats de béns o societats civils els socis de les quals siguin tots persones físiques, si el seu volum d'operacions de l'any anterior no va passar de 85.000 € (elevat a l'any si van començar aquell any). Qui comença l'activitat ho pot demanar des del principi. No poden els que són en el règim simplificat, el criteri de caixa, el grup d'entitats, el compte corrent tributari o la liquidació mensual, llevat que sigui només per ser en la devolució mensual (REDEME), que es deixa en optar. Per al 2027, a la mateixa sol·licitud es pot renunciar als règims incompatibles."),
        ("Com es calculen els pagaments a compte?",
         "Cada pagament és la quarta part de l'IVA a pagar de l'any anterior. El primer any es pren la suma dels models 303 de l'any anterior presentats abans que acabi el març. Si aquesta quantitat no és positiva, o si acabes de començar l'activitat, els pagaments són zero. Amb tres pagaments avances tres quartes parts i la resta es paga el gener. Hisenda t'ensenya cada import a la seu electrònica els cinc primers dies d'abril, juliol i octubre."),
        ("Quan i com es demana?",
         "Per al 2027, durant el mes de març del 2027, amb la declaració censal i indicant el compte bancari per als càrrecs. Després, el desembre per a l'any següent o quan et donis d'alta. Es manté cada any fins que hi renunciïs; la renúncia es fa el desembre i dura almenys tres anys. Si un any passes de 85.000 €, surts del règim l'any següent."),
        ("Em convé?",
         "A favor: fas una declaració en lloc de quatre i els pagaments són fixos i automàtics. En contra: els pagaments es basen en l'any anterior encara que aquest any facturis menys (ho recuperes el gener), no es poden ajornar ni fraccionar, la renúncia dura almenys tres anys i, si eres en el criteri de caixa o en la devolució mensual, en perds els avantatges. Si el teu IVA sol sortir a retornar, els teus pagaments a compte serien zero."),
        ("Això ja és definitiu?", CONVALIDACION_CA),
    ],
    "aviso": "és una estimació orientativa i no substitueix l'Agència Tributària ni un assessor. Pren com a IVA del 2026 el cobrat menys el deduïble dels teus models 303; Hisenda calcularà l'import exacte. Fonts, en castellà:",
    "fuentes": FUENTES_IVA,
}

PAGINAS = [*PAGINAS_ANTERIORES, M130_2027_ES, M130_2027_CA, IVA_ANUAL_ES, IVA_ANUAL_CA]
