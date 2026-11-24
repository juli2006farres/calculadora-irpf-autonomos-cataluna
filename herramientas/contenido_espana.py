"""IRPF para todas las comunidades, calendario fiscal 2027 y adaptación de sueldo neto y cuánto facturar."""
import copy
import datetime
import unicodedata

from contenido import BOE_LIRPF, campo, casilla, seleccion
from contenido_303 import PAGINAS as PAGINAS_ANTERIORES
from contenido_extra import CLIENTE, INICIO

AEAT_ESCALAS = "https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025/c15-calculo-impuesto-determinacion-cuotas-integras/gravamen-base-liquidable-general/gravamen-autonomico.html"
AEAT_MINIMOS = "https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025/c14-adecuacion-impuesto-circunstancias-personales/minimo-autonomico-personal-familiar/cuadro-minimos-personales-familiares-estatal-autonomicos.html"
HACIENDA_2026 = "https://www.hacienda.gob.es/sgfal/financiacionterritorial/autonomica/capitulo-i-tributacion-autonomica-2026.pdf"
BOE_VALENCIA = "https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-19331"
AEAT_PLAZO_303 = "https://sede.agenciatributaria.gob.es/Sede/iva/presentar-declaracion-iva-modelo-303/plazo-presentacion-modelo-303.html"
AEAT_CALENDARIO = "https://sede.agenciatributaria.gob.es/Sede/presentacion-declaraciones-calendario-contribuyente.html"
BOE_LGT = "https://www.boe.es/buscar/act.php?id=BOE-A-2003-23186#a27"

COMUNIDADES = {
    "es": {"andalucia": "Andalucía", "aragon": "Aragón", "asturias": "Principado de Asturias", "baleares": "Illes Balears",
           "canarias": "Canarias", "cantabria": "Cantabria", "castilla_la_mancha": "Castilla-La Mancha",
           "castilla_y_leon": "Castilla y León", "cataluna": "Cataluña", "extremadura": "Extremadura", "galicia": "Galicia",
           "la_rioja": "La Rioja", "madrid": "Comunidad de Madrid", "murcia": "Región de Murcia", "valenciana": "Comunitat Valenciana"},
    "ca": {"andalucia": "Andalusia", "aragon": "Aragó", "asturias": "Principat d'Astúries", "baleares": "Illes Balears",
           "canarias": "Canàries", "cantabria": "Cantàbria", "castilla_la_mancha": "Castella-la Manxa",
           "castilla_y_leon": "Castella i Lleó", "cataluna": "Catalunya", "extremadura": "Extremadura", "galicia": "Galícia",
           "la_rioja": "La Rioja", "madrid": "Comunitat de Madrid", "murcia": "Regió de Múrcia", "valenciana": "Comunitat Valenciana"},
}


def orden_alfabetico(nombre):
    """Clave para ordenar nombres sin que cuenten los acentos ni las mayúsculas."""
    sin_acentos = "".join(ch for ch in unicodedata.normalize("NFD", nombre) if not unicodedata.combining(ch))
    return sin_acentos.casefold()


def selector_comunidad(lang, inicial):
    etiqueta, ayuda = {
        "es": ("Comunidad autónoma", "Donde vives. No incluye País Vasco, Navarra, Ceuta ni Melilla."),
        "ca": ("Comunitat autònoma", "On vius. No inclou el País Basc, Navarra, Ceuta ni Melilla."),
    }[lang]
    nombres = COMUNIDADES[lang]
    ops = "\n".join(
        f'          <option value="{c}"{" selected" if c == inicial else ""}>{n}</option>'
        for c, n in sorted(nombres.items(), key=lambda x: orden_alfabetico(x[1]))
    )
    return f"""      <div>
        <label for="comunidad">{etiqueta}<span class="ayuda">{ayuda}</span></label>
        <select id="comunidad" name="comunidad">
{ops}
        </select>
      </div>"""


# ---------------------------------------------------------------- IRPF para toda España
def formulario_irpf(lang):
    t = {
        "es": ("Tus datos del año", "Ejercicio", "El año que quieres calcular.", "Ingresos anuales (€)", "Lo facturado en el año, sin IVA.",
               "Gastos deducibles (€)", "Sin contar las cuotas de autónomo.", "Cuotas de autónomo pagadas (€)", "Total del año a la Seguridad Social.",
               "Retenciones y pagos a cuenta (€)", "Lo ya adelantado a Hacienda en el año.", "Estimación", "La que usas en el IRPF. La más habitual es la simplificada.",
               "Hijos y otros descendientes", "Descendientes que dan derecho al mínimo", "En general, menores de 25 años que viven contigo.",
               "De ellos, menores de 3 años", "Cuéntalos también en la casilla anterior.", "El otro progenitor también aplica el mínimo", "En ese caso se reparte a partes iguales."),
        "ca": ("Les teves dades de l'any", "Exercici", "L'any que vols calcular.", "Ingressos anuals (€)", "El que has facturat durant l'any, sense IVA.",
               "Despeses deduïbles (€)", "Sense comptar les quotes d'autònom.", "Quotes d'autònom pagades (€)", "Total de l'any a la Seguretat Social.",
               "Retencions i pagaments a compte (€)", "El que ja has avançat a Hisenda durant l'any.", "Estimació", "La que fas servir a l'IRPF. La més habitual és la simplificada.",
               "Fills i altres descendents", "Descendents que donen dret al mínim", "En general, menors de 25 anys que conviuen amb tu.",
               "D'aquests, menors de 3 anys", "Compta'ls també a la casella anterior.", "L'altre progenitor també aplica el mínim", "En aquest cas es reparteix a parts iguals."),
    }[lang]
    (cab, anio, anio_a, ing, ing_a, gas, gas_a, cuo, cuo_a, pag, pag_a, mod, mod_a, hijos_t, hijos, hijos_a, men, men_a, comp, comp_a) = t
    modalidades = [("directa_simplificada", "Directa simplificada"), ("directa_normal", "Directa normal")]
    return f"""    <h2>{cab}</h2>
    <div class="rejilla">
{selector_comunidad(lang, "madrid")}
{seleccion("anio", anio, [("2026", "2026"), ("2025", "2025")], anio_a)}
{campo("ingresos", ing, ing_a, "40000")}
{campo("gastos", gas, gas_a, "5000")}
{campo("cuotas", cuo, cuo_a, "4000")}
{campo("pagos", pag, pag_a, "0")}
{seleccion("modalidad", mod, modalidades, mod_a)}
    </div>
{casilla("inicio", *INICIO[lang])}
{casilla("cliente", *CLIENTE[lang])}
    <details>
      <summary>{hijos_t}</summary>
      <div class="rejilla" style="margin-top:12px">
{campo("hijos", hijos, hijos_a, "0", ' step="1" max="20"')}
{campo("menores3", men, men_a, "0", ' step="1" max="20"')}
      </div>
      <div class="casilla">
        <input id="compartido" name="compartido" type="checkbox">
        <label for="compartido">{comp}<span class="ayuda">{comp_a}</span></label>
      </div>
    </details>"""


FUENTES_IRPF = [
    ("Ley del IRPF, artículos 57, 58 y 63 (BOE)", BOE_LIRPF),
    ("Escalas autonómicas, Manual de Renta 2025 (Agencia Tributaria)", AEAT_ESCALAS),
    ("Mínimos autonómicos, Manual de Renta 2025 (Agencia Tributaria)", AEAT_MINIMOS),
    ("Tributación autonómica. Medidas 2026 (Ministerio de Hacienda)", HACIENDA_2026),
    ("Comunitat Valenciana: Ley 5/2026, artículo 18 (BOE)", BOE_VALENCIA),
]

IRPF_ES = {
    "lang": "es",
    "clave": "irpf_es",
    "script": "irpf-espana-app.js",
    "titulo": "Calculadora IRPF autónomos 2026 por comunidad autónoma · Gratis",
    "descripcion": "Calcula gratis el IRPF de un autónomo en 2025 y 2026 en cualquier comunidad autónoma, con su escala y sus mínimos, y compáralo con las demás.",
    "og_titulo": "Calculadora de IRPF de autónomos por comunidad autónoma",
    "og_descripcion": "El IRPF de tu actividad en tu comunidad, y cuánto pagarías en las demás.",
    "h1": "Calculadora de IRPF para autónomos en cada comunidad autónoma",
    "entradilla": "Calcula cuánto IRPF te corresponde como autónomo con la escala estatal y la de tu comunidad, en 2025 o 2026, y mira cuánto pagarías con los mismos datos en las otras 14 comunidades.",
    "formulario": formulario_irpf("es"),
    "faq": [
        ("¿Por qué el IRPF cambia según la comunidad autónoma?",
         "El IRPF tiene dos partes: la estatal, igual para todos, y la autonómica, que fija cada comunidad con su propia escala y, en algunos casos, sus propios mínimos personales. Por eso con los mismos ingresos se paga distinto en cada comunidad."),
        ("¿En qué comunidad paga menos IRPF un autónomo?",
         "Depende de lo que ganes. Con 40.000 € de ingresos, 5.000 € de gastos y 4.000 € de cuotas en 2026, la más baja es Madrid y la más alta, Cataluña, con unos 470 € de diferencia. Pero el orden cambia: Extremadura es la más barata con ingresos bajos y de las más caras con ingresos altos. La tabla del resultado ordena las 15 comunidades con tus datos."),
        ("¿Qué cambia en 2026?",
         f'Según el <a href="{HACIENDA_2026}">informe de Hacienda sobre las medidas autonómicas de 2026</a>, solo cambian las escalas de Extremadura, que baja los dos primeros tipos, y de la Comunitat Valenciana, que baja todos según la <a href="{BOE_VALENCIA}">Ley 5/2026</a>. El resto aplica la misma escala que en 2025.'),
        ("¿Incluye las deducciones autonómicas?",
         "No. Cada comunidad tiene muchas deducciones propias, por alquiler, hijos o donativos, que dependen de tu situación. La calculadora aplica la escala y los mínimos, así que el resultado real puede ser algo menor."),
        ("¿Por qué no están el País Vasco ni Navarra?",
         "Porque tienen su propio IRPF foral, con normas distintas. Ceuta y Melilla tampoco están, porque no tienen escala autonómica y aplican una deducción especial."),
    ],
    "aviso": "es una estimación orientativa y no sustituye la declaración ni el consejo de un asesor fiscal. Las escalas de 2025 son las del Manual de Renta de la Agencia Tributaria y los mínimos autonómicos de 2026 se suponen iguales a los de 2025, porque el informe de Hacienda no recoge cambios. Fuentes:",
    "fuentes": FUENTES_IRPF,
}

IRPF_CA = {
    "lang": "ca",
    "clave": "irpf_es",
    "script": "irpf-espana-app.js",
    "titulo": "Calculadora IRPF autònoms 2026 per comunitat autònoma · Gratuïta",
    "descripcion": "Calcula gratis l'IRPF d'un autònom el 2025 i el 2026 a qualsevol comunitat autònoma, amb la seva escala i els seus mínims, i compara'l amb les altres.",
    "og_titulo": "Calculadora d'IRPF d'autònoms per comunitat autònoma",
    "og_descripcion": "L'IRPF de la teva activitat a la teva comunitat, i quant pagaries a les altres.",
    "h1": "Calculadora d'IRPF per a autònoms a cada comunitat autònoma",
    "entradilla": "Calcula quant IRPF et correspon com a autònom amb l'escala estatal i la de la teva comunitat, el 2025 o el 2026, i mira quant pagaries amb les mateixes dades a les altres 14 comunitats.",
    "formulario": formulario_irpf("ca"),
    "faq": [
        ("Per què l'IRPF canvia segons la comunitat autònoma?",
         "L'IRPF té dues parts: l'estatal, igual per a tothom, i l'autonòmica, que fixa cada comunitat amb la seva pròpia escala i, en alguns casos, els seus propis mínims personals. Per això amb els mateixos ingressos es paga diferent a cada comunitat."),
        ("A quina comunitat paga menys IRPF un autònom?",
         "Depèn del que guanyis. Amb 40.000 € d'ingressos, 5.000 € de despeses i 4.000 € de quotes el 2026, la més baixa és Madrid i la més alta, Catalunya, amb uns 470 € de diferència. Però l'ordre canvia: Extremadura és la més barata amb ingressos baixos i de les més cares amb ingressos alts. La taula del resultat ordena les 15 comunitats amb les teves dades."),
        ("Què canvia el 2026?",
         f'Segons l\'<a href="{HACIENDA_2026}">informe d\'Hisenda sobre les mesures autonòmiques del 2026</a>, només canvien les escales d\'Extremadura, que baixa els dos primers tipus, i de la Comunitat Valenciana, que els baixa tots segons la <a href="{BOE_VALENCIA}">Llei 5/2026</a>. La resta aplica la mateixa escala que el 2025.'),
        ("Inclou les deduccions autonòmiques?",
         "No. Cada comunitat té moltes deduccions pròpies, per lloguer, fills o donatius, que depenen de la teva situació. La calculadora aplica l'escala i els mínims, així que el resultat real pot ser una mica menor."),
        ("Per què no hi són el País Basc ni Navarra?",
         "Perquè tenen el seu propi IRPF foral, amb normes diferents. Ceuta i Melilla tampoc no hi són, perquè no tenen escala autonòmica i apliquen una deducció especial."),
    ],
    "aviso": "és una estimació orientativa i no substitueix la declaració ni el consell d'un assessor fiscal. Les escales del 2025 són les del Manual de Renda de l'Agència Tributària i els mínims autonòmics del 2026 se suposen iguals als del 2025, perquè l'informe d'Hisenda no en recull canvis. Fonts, en castellà:",
    "fuentes": FUENTES_IRPF,
}

# ---------------------------------------------------------------- Calendario fiscal 2027
FILAS_CALENDARIO = {
    "es": [
        ("Hasta el 20 de enero", "Modelos 111 y 115 del 4T de 2026", "Solo si tienes trabajadores, pagas a profesionales con retención o alquilas un local.", None),
        ("Hasta el 1 de febrero", "Modelo 303 del 4T de 2026 (IVA)", "Plazo del 1 al 30 de enero, que en 2027 acaba en sábado.", "m303"),
        ("Hasta el 1 de febrero", "Modelo 130 del 4T de 2026 (IRPF)", "Salvo profesionales con retención en al menos el 70 % de sus ingresos del año anterior.", "m130"),
        ("Hasta el 1 de febrero", "Modelo 390: resumen anual del IVA de 2026", "", None),
        ("Hasta el 1 de febrero", "Modelos 190 y 180: resúmenes anuales de retenciones", "Si presentas los modelos 111 o 115.", None),
        ("Hasta el 1 de marzo", "Modelo 347: operaciones con terceros", "Si superas 3.005,06 € con un mismo cliente o proveedor en 2026. Plazo de febrero, que acaba en domingo.", None),
        ("Del 1 al 20 de abril", "Modelos 303, 130, 111 y 115 del 1T de 2027", "", "m303"),
        ("De abril a junio", "Renta 2026 (modelo 100)", "Hacienda publica las fechas exactas cada año. Normalmente acaba el 30 de junio.", "irpf_es"),
        ("Del 1 al 20 de julio", "Modelos 303, 130, 111 y 115 del 2T de 2027", "", "m130"),
        ("Del 1 al 20 de octubre", "Modelos 303, 130, 111 y 115 del 3T de 2027", "", "m303"),
        ("Hasta el 20 de enero de 2028", "Modelos 111 y 115 del 4T de 2027", "Solo si tienes trabajadores, pagas a profesionales con retención o alquilas un local.", None),
        ("Hasta el 31 de enero de 2028", "Modelos 303, 130 y 390 del 4T y del año 2027", "Plazo del 1 al 30 de enero, que en 2028 acaba en domingo.", "m130"),
    ],
    "ca": [
        ("Fins al 20 de gener", "Models 111 i 115 del 4T del 2026", "Només si tens treballadors, pagues professionals amb retenció o lloges un local.", None),
        ("Fins a l'1 de febrer", "Model 303 del 4T del 2026 (IVA)", "Termini de l'1 al 30 de gener, que el 2027 acaba en dissabte.", "m303"),
        ("Fins a l'1 de febrer", "Model 130 del 4T del 2026 (IRPF)", "Excepte professionals amb retenció en almenys el 70 % dels ingressos de l'any anterior.", "m130"),
        ("Fins a l'1 de febrer", "Model 390: resum anual de l'IVA del 2026", "", None),
        ("Fins a l'1 de febrer", "Models 190 i 180: resums anuals de retencions", "Si presentes els models 111 o 115.", None),
        ("Fins a l'1 de març", "Model 347: operacions amb tercers", "Si superes 3.005,06 € amb un mateix client o proveïdor el 2026. Termini de febrer, que acaba en diumenge.", None),
        ("De l'1 al 20 d'abril", "Models 303, 130, 111 i 115 del 1T del 2027", "", "m303"),
        ("D'abril a juny", "Renda 2026 (model 100)", "Hisenda publica les dates exactes cada any. Normalment acaba el 30 de juny.", "irpf_es"),
        ("De l'1 al 20 de juliol", "Models 303, 130, 111 i 115 del 2T del 2027", "", "m130"),
        ("De l'1 al 20 d'octubre", "Models 303, 130, 111 i 115 del 3T del 2027", "", "m303"),
        ("Fins al 20 de gener del 2028", "Models 111 i 115 del 4T del 2027", "Només si tens treballadors, pagues professionals amb retenció o lloges un local.", None),
        ("Fins al 31 de gener del 2028", "Models 303, 130 i 390 del 4T i de l'any 2027", "Termini de l'1 al 30 de gener, que el 2028 acaba en diumenge.", "m130"),
    ],
}
# Último día de cada fila de la tabla, en el mismo orden (lo comprueba la verificación del calendario).
# La renta no tiene fecha fija: se pone el 30 de junio, su final habitual, y el aviso lo dice.
FECHAS_CALENDARIO = [
    "2027-01-20", "2027-02-01", "2027-02-01", "2027-02-01", "2027-02-01", "2027-03-01",
    "2027-04-20", "2027-06-30", "2027-07-20", "2027-10-20", "2028-01-20", "2028-01-31",
]
assert all(len(FECHAS_CALENDARIO) == len(f) for f in FILAS_CALENDARIO.values())
ARCHIVO_ICS = {"es": "plazos-fiscales-2027.ics", "ca": "terminis-fiscals-2027.ics"}
# El 24-11-2026 el Consejo de Ministros aprobó un real decreto-ley que cambia los pagos trimestrales
# del IVA y del IRPF de muchos autónomos. Hasta leer su texto en el BOE y revisar los plazos de 2027,
# no se ofrece el archivo de calendario: una vez importado en el móvil ya no se puede corregir.
OFRECER_ICS = False
TEXTOS_ICS = {
    "es": {
        "nombre": "Plazos fiscales del autónomo 2027",
        "ultimo": "Último día: {que}",
        "renta": "Renta 2026 (modelo 100): final habitual del plazo",
        "confirma": "Confirma la fecha en el calendario del contribuyente de la Agencia Tributaria.",
        "mas": "Calendario y calculadoras gratis: {url}",
        "aviso": "Dentro de 5 días acaba un plazo fiscal: {que}",
    },
    "ca": {
        "nombre": "Terminis fiscals de l'autònom 2027",
        "ultimo": "Últim dia: {que}",
        "renta": "Renda 2026 (model 100): final habitual del termini",
        "confirma": "Confirma la data al calendari del contribuent de l'Agència Tributària.",
        "mas": "Calendari i calculadores gratuïtes: {url}",
        "aviso": "D'aquí a 5 dies acaba un termini fiscal: {que}",
    },
}


def _escapar_ics(texto):
    return texto.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def _plegar_ics(linea):
    """Corta las líneas de más de 75 bytes como pide el estándar iCalendar (RFC 5545), sin partir letras."""
    partes, actual = [], ""
    for letra in linea:
        limite = 75 if not partes else 74
        if len((actual + letra).encode("utf-8")) > limite:
            partes.append(actual)
            actual = letra
        else:
            actual += letra
    partes.append(actual)
    return "\r\n ".join(partes)


def calendario_ics(lang, url):
    """Archivo .ics con un evento de día completo por cada plazo y un aviso 5 días antes a las 9:00."""
    t = TEXTOS_ICS[lang]
    lineas = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Calculadoras para autonomos//Calendario fiscal 2027//" + lang.upper(),
              "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "X-WR-CALNAME:" + _escapar_ics(t["nombre"]), "X-WR-TIMEZONE:Europe/Madrid"]
    for n, ((plazo, que, detalle, _), fecha) in enumerate(zip(FILAS_CALENDARIO[lang], FECHAS_CALENDARIO), 1):
        dia = fecha.replace("-", "")
        siguiente = (datetime.date.fromisoformat(fecha) + datetime.timedelta(days=1)).strftime("%Y%m%d")
        que_minuscula = que[0].lower() + que[1:] if que.startswith("Model") else que
        resumen = t["renta"] if que.startswith(("Renta", "Renda")) else t["ultimo"].format(que=que_minuscula)
        descripcion = " ".join(x for x in (f"{plazo}.", detalle, t["confirma"]) if x) + "\n" + t["mas"].format(url=url)
        lineas += [
            "BEGIN:VEVENT",
            f"UID:plazo-{dia}-{n:02d}-{lang}@juli2006farres.github.io",
            "DTSTAMP:20261124T000000Z",
            f"DTSTART;VALUE=DATE:{dia}",
            f"DTEND;VALUE=DATE:{siguiente}",
            "SUMMARY:" + _escapar_ics(resumen),
            "DESCRIPTION:" + _escapar_ics(descripcion),
            "URL:" + url,
            "TRANSP:TRANSPARENT",
            "BEGIN:VALARM",
            "ACTION:DISPLAY",
            "DESCRIPTION:" + _escapar_ics(t["aviso"].format(que=que)),
            "TRIGGER:-P4DT15H",
            "END:VALARM",
            "END:VEVENT",
        ]
    lineas.append("END:VCALENDAR")
    return "\r\n".join(_plegar_ics(l) for l in lineas) + "\r\n"


RUTAS_CALC = {
    "es": {"m303": "modelo-303/", "m130": "modelo-130/", "irpf_es": "calculadora-irpf-autonomos/"},
    "ca": {"m303": "ca/model-303/", "m130": "ca/model-130/", "irpf_es": "ca/calculadora-irpf-autonoms/"},
}


def cuerpo_calendario(lang):
    raiz = "../" * (2 if lang == "ca" else 1)
    cab = {"es": ("Plazo en 2027", "Qué se presenta", "Calculadora"), "ca": ("Termini el 2027", "Què es presenta", "Calculadora")}[lang]
    enlace_txt = {"es": "Calcular", "ca": "Calcular"}[lang]
    titulo, intro, nota = {
        "es": ("Plazos de 2027 para autónomos",
               "Estos son los plazos habituales de un autónomo en estimación directa que presenta el IVA y el IRPF cada trimestre.",
               "Si domicilias el pago, el plazo para hacerlo acaba unos días antes. Si un plazo termina en sábado, domingo o festivo nacional, pasa al siguiente día hábil."),
        "ca": ("Terminis del 2027 per a autònoms",
               "Aquests són els terminis habituals d'un autònom en estimació directa que presenta l'IVA i l'IRPF cada trimestre.",
               "Si domicilies el pagament, el termini per fer-ho acaba uns dies abans. Si un termini acaba en dissabte, diumenge o festiu nacional, passa al dia hàbil següent."),
    }[lang]
    filas = []
    for plazo, que, detalle, calc in FILAS_CALENDARIO[lang]:
        enlace = f'<a href="{raiz}{RUTAS_CALC[lang][calc]}">{enlace_txt}</a>' if calc else ""
        det = f'<span class="ayuda">{detalle}</span>' if detalle else ""
        filas.append(f"        <tr><td><strong>{plazo}</strong></td><td>{que}{det}</td><td>{enlace}</td></tr>")
    cuerpo = "\n".join(filas)
    boton, ayuda = {
        "es": ("Añadir los plazos a mi calendario",
               f"Descarga un archivo con los {len(FECHAS_CALENDARIO)} plazos de la tabla, cada uno con un aviso 5 días antes si tu calendario lo admite. "
               "En iPhone, Mac y Outlook se abre con tu calendario; en Google Calendar, impórtalo desde el ordenador en Configuración › Importar y exportar."),
        "ca": ("Afegeix els terminis al meu calendari",
               f"Descarrega un fitxer amb els {len(FECHAS_CALENDARIO)} terminis de la taula, cadascun amb un avís 5 dies abans si el teu calendari ho admet. "
               "A l'iPhone, al Mac i a l'Outlook s'obre amb el teu calendari; a Google Calendar, importa'l des de l'ordinador a Configuració › Importa i exporta."),
    }[lang]
    icono = ('<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
             'stroke-linejoin="round" aria-hidden="true"><rect x="4" y="5" width="16" height="16" rx="2"/><path d="M4 10h16M8 3v4M16 3v4M12 13v5M9.5 15.5h5"/></svg>')
    bloque_ics = f"""<div class="anadir-calendario">
      <a class="boton" href="{ARCHIVO_ICS[lang]}" download="{ARCHIVO_ICS[lang]}" type="text/calendar">{icono}{boton}</a>
      <p class="nota">{ayuda}</p>
    </div>
    """ if OFRECER_ICS else ""
    return f"""<section class="tarjeta">
    <h2>{titulo}</h2>
    <p>{intro}</p>
    {bloque_ics}<div class="tabla-ancha calendario">
    <table>
      <thead><tr><th>{cab[0]}</th><th>{cab[1]}</th><th>{cab[2]}</th></tr></thead>
      <tbody>
{cuerpo}
      </tbody>
    </table>
    </div>
    <p class="nota">{nota}</p>
  </section>"""


CALENDARIO_ES = {
    "lang": "es",
    "clave": "calendario",
    "script": None,
    "cuerpo": cuerpo_calendario("es"),
    "titulo": "Calendario fiscal del autónomo 2027 · Todos los plazos del año",
    "descripcion": "Calendario fiscal 2027 para autónomos: plazos de los modelos 303, 130, 390, 111, 347 y de la renta, mes a mes, con enlaces a calculadoras gratis.",
    "og_titulo": "Calendario fiscal del autónomo 2027",
    "og_descripcion": "Todos los plazos de 2027 para autónomos: IVA, IRPF, resúmenes anuales y renta.",
    "h1": "Calendario fiscal del autónomo 2027",
    "entradilla": "Todos los plazos que tiene un autónomo en 2027, mes a mes: IVA, pagos del IRPF, resúmenes anuales y la renta, con un enlace a la calculadora de cada modelo.",
    "faq": [
        ("¿Cuándo se presentan los modelos 303 y 130 en 2027?",
         "Del 1 al 20 de abril, julio y octubre para el primer, segundo y tercer trimestre. El cuarto trimestre de 2026 se presenta en enero de 2027, y como el 30 de enero cae en sábado, el plazo pasa al lunes 1 de febrero."),
        ("¿Qué pasa si presento un modelo fuera de plazo?",
         f'Si lo presentas tarde por tu cuenta, sin que Hacienda te lo haya pedido, pagas un recargo del 1 % más un 1 % por cada mes completo de retraso, y a partir de los 12 meses un 15 % más intereses, según el <a href="{BOE_LGT}">artículo 27 de la Ley General Tributaria</a>. Si te lo reclama Hacienda, puede haber además una sanción.'),
        ("¿Qué es el modelo 390?",
         "Es el resumen anual del IVA. En general lo presentan en enero los autónomos que presentan el modelo 303 durante el año."),
        ("¿Qué es el modelo 347?",
         "Es la declaración de operaciones con terceros. Hay que presentarla en febrero si en el año has facturado o comprado más de 3.005,06 €, IVA incluido, a una misma persona o empresa, salvo que esas operaciones ya estén en otros modelos."),
        ("¿Estas fechas son oficiales?",
         f'Son los plazos habituales que fija la normativa, aplicados a 2027 con la regla de que un plazo que acaba en día inhábil pasa al siguiente día hábil. La Agencia Tributaria publica cada año su <a href="{AEAT_CALENDARIO}">calendario del contribuyente</a>: compruébalo cuando salga.'),
    ],
    "aviso": "es un resumen orientativo de los plazos más habituales y no incluye todos los modelos ni los plazos de las haciendas forales. Confirma las fechas en el calendario oficial de la Agencia Tributaria. Fuentes:",
    "fuentes": [
        ("Plazos de presentación del modelo 303 (Agencia Tributaria)", AEAT_PLAZO_303),
        ("Calendario del contribuyente (Agencia Tributaria)", AEAT_CALENDARIO),
        ("Ley General Tributaria, artículo 27 (BOE)", BOE_LGT),
    ],
}

CALENDARIO_CA = {
    "lang": "ca",
    "clave": "calendario",
    "script": None,
    "cuerpo": cuerpo_calendario("ca"),
    "titulo": "Calendari fiscal de l'autònom 2027 · Tots els terminis de l'any",
    "descripcion": "Calendari fiscal 2027 per a autònoms: terminis dels models 303, 130, 390, 111, 347 i de la renda, mes a mes, amb enllaços a calculadores gratuïtes.",
    "og_titulo": "Calendari fiscal de l'autònom 2027",
    "og_descripcion": "Tots els terminis del 2027 per a autònoms: IVA, IRPF, resums anuals i renda.",
    "h1": "Calendari fiscal de l'autònom 2027",
    "entradilla": "Tots els terminis que té un autònom el 2027, mes a mes: IVA, pagaments de l'IRPF, resums anuals i la renda, amb un enllaç a la calculadora de cada model.",
    "faq": [
        ("Quan es presenten els models 303 i 130 el 2027?",
         "De l'1 al 20 d'abril, juliol i octubre per al primer, segon i tercer trimestre. El quart trimestre del 2026 es presenta el gener del 2027, i com que el 30 de gener cau en dissabte, el termini passa al dilluns 1 de febrer."),
        ("Què passa si presento un model fora de termini?",
         f'Si el presentes tard pel teu compte, sense que Hisenda te l\'hagi demanat, pagues un recàrrec de l\'1 % més un 1 % per cada mes complet de retard, i a partir dels 12 mesos un 15 % més interessos, segons l\'<a href="{BOE_LGT}">article 27 de la Llei general tributària</a>. Si t\'ho reclama Hisenda, hi pot haver a més una sanció.'),
        ("Què és el model 390?",
         "És el resum anual de l'IVA. En general el presenten al gener els autònoms que presenten el model 303 durant l'any."),
        ("Què és el model 347?",
         "És la declaració d'operacions amb tercers. S'ha de presentar al febrer si durant l'any has facturat o comprat més de 3.005,06 €, IVA inclòs, a una mateixa persona o empresa, llevat que aquestes operacions ja figurin en altres models."),
        ("Aquestes dates són oficials?",
         f'Són els terminis habituals que fixa la normativa, aplicats al 2027 amb la regla que un termini que acaba en dia inhàbil passa al dia hàbil següent. L\'Agència Tributària publica cada any el seu <a href="{AEAT_CALENDARIO}">calendari del contribuent</a>: comprova-ho quan surti.'),
    ],
    "aviso": "és un resum orientatiu dels terminis més habituals i no inclou tots els models ni els terminis de les hisendes forals. Confirma les dates al calendari oficial de l'Agència Tributària. Fonts, en castellà:",
    "fuentes": CALENDARIO_ES["fuentes"],
}

# ---------------------------------------------------------------- Sueldo neto y cuánto facturar para toda España
FUENTES_SUELDO = [("Cuota de autónomos: Orden PJC/297/2026 (BOE)", "https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-7296"), *FUENTES_IRPF[:3]]


def a_toda_espana(p):
    p = copy.deepcopy(p)
    lang = p["lang"]
    p["formulario"] = p["formulario"].replace('    <div class="rejilla">\n', '    <div class="rejilla">\n' + selector_comunidad(lang, "madrid") + "\n", 1)
    p["fuentes"] = FUENTES_SUELDO
    return p


def reemplazar_faq(faq, reemplazos):
    return [reemplazos.get(q, (q, a)) for q, a in faq]


base = {p["lang"] + p["clave"]: p for p in PAGINAS_ANTERIORES}
SUELDO_ES = a_toda_espana(base["essueldo"])
SUELDO_ES.update({
    "titulo": "Calculadora sueldo neto autónomo 2026 · Por comunidad autónoma",
    "descripcion": "Calcula cuánto te queda al mes como autónomo en 2026 en tu comunidad, tras gastos, cuota de autónomos e IRPF. Gratis, sin registro y con datos oficiales.",
    "og_descripcion": "Lo que te queda al mes como autónomo tras gastos, cuota e IRPF, en tu comunidad.",
    "entradilla": "Calcula lo que te queda limpio cada mes después de gastos, cuota de autónomos e IRPF, en cualquier comunidad salvo País Vasco y Navarra. La cuota sigue las tablas oficiales de 2026.",
    "aviso": "es una estimación orientativa y no sustituye el consejo de un asesor fiscal o laboral. No incluye las deducciones autonómicas del IRPF. Fuentes:",
})
SUELDO_ES["faq"] = reemplazar_faq(SUELDO_ES["faq"], {
    "¿Cuánto le queda a un autónomo que factura 40.000 € al año?": (
        "¿Cuánto le queda a un autónomo que factura 40.000 € al año?",
        "En 2026, con 5.000 € de gastos y la cuota mínima de su tramo (427,21 € al mes), unos 2.016 € al mes en Cataluña. En otras comunidades cambia el IRPF: elige la tuya en la calculadora para verlo."),
    "¿Por qué solo vale para Cataluña?": (
        "¿Por qué cambia según la comunidad?",
        "El IRPF tiene una parte autonómica con escala propia en cada comunidad. La cuota de autónomos, en cambio, es igual en toda España."),
})
SUELDO_CA = a_toda_espana(base["casueldo"])
SUELDO_CA.update({
    "titulo": "Calculadora sou net autònom 2026 · Per comunitat autònoma",
    "descripcion": "Calcula quant et queda al mes com a autònom el 2026 a la teva comunitat, després de despeses, quota d'autònoms i IRPF. Gratuïta i amb dades oficials.",
    "og_descripcion": "El que et queda al mes com a autònom després de despeses, quota i IRPF, a la teva comunitat.",
    "entradilla": "Calcula el que et queda net cada mes després de despeses, quota d'autònoms i IRPF, a qualsevol comunitat excepte el País Basc i Navarra. La quota segueix les taules oficials del 2026.",
    "aviso": "és una estimació orientativa i no substitueix el consell d'un assessor fiscal o laboral. No inclou les deduccions autonòmiques de l'IRPF. Fonts, en castellà:",
})
SUELDO_CA["faq"] = reemplazar_faq(SUELDO_CA["faq"], {
    "Quant li queda a un autònom que factura 40.000 € l'any?": (
        "Quant li queda a un autònom que factura 40.000 € l'any?",
        "El 2026, amb 5.000 € de despeses i la quota mínima del seu tram (427,21 € al mes), uns 2.016 € al mes a Catalunya. A altres comunitats canvia l'IRPF: tria la teva a la calculadora per veure-ho."),
    "Per què només serveix per a Catalunya?": (
        "Per què canvia segons la comunitat?",
        "L'IRPF té una part autonòmica amb escala pròpia a cada comunitat. La quota d'autònoms, en canvi, és igual a tot Espanya."),
})
OBJETIVO_ES = a_toda_espana(base["esobjetivo"])
OBJETIVO_ES.update({
    "descripcion": "¿Cuánto tienes que facturar como autónomo para ganar 2.000 € netos al mes? Calcúlalo con la cuota de autónomos y el IRPF de tu comunidad en 2026.",
    "entradilla": "Escribe el sueldo neto que quieres al mes y calcula cuánto tienes que facturar al año, con la cuota de autónomos y el IRPF de tu comunidad en 2026. También te da el precio mínimo por hora.",
    "aviso": "es una estimación orientativa y no sustituye el consejo de un asesor fiscal o laboral. No incluye la tarifa plana, otras rentas, el mínimo por hijos ni las deducciones autonómicas. Fuentes:",
})
OBJETIVO_ES["faq"] = reemplazar_faq(OBJETIVO_ES["faq"], {
    "¿Cuánto tiene que facturar un autónomo para ganar 2.000 € netos al mes?": (
        "¿Cuánto tiene que facturar un autónomo para ganar 2.000 € netos al mes?",
        "En Cataluña en 2026, con 5.000 € de gastos al año y la cuota mínima de su tramo, unos 39.730 € al año sin IVA, unos 3.311 € al mes. En otras comunidades cambia por el IRPF: elige la tuya en la calculadora."),
    "¿Por qué solo vale para Cataluña?": (
        "¿Por qué cambia según la comunidad?",
        "El IRPF tiene una parte autonómica con escala propia en cada comunidad. La cuota de autónomos es igual en toda España."),
})
OBJETIVO_CA = a_toda_espana(base["caobjetivo"])
OBJETIVO_CA.update({
    "descripcion": "Quant has de facturar com a autònom per guanyar 2.000 € nets al mes? Calcula-ho amb la quota d'autònoms i l'IRPF de la teva comunitat el 2026.",
    "entradilla": "Escriu el sou net que vols al mes i calcula quant has de facturar a l'any, amb la quota d'autònoms i l'IRPF de la teva comunitat el 2026. També et dona el preu mínim per hora.",
    "aviso": "és una estimació orientativa i no substitueix el consell d'un assessor fiscal o laboral. No inclou la tarifa plana, altres rendes, el mínim per fills ni les deduccions autonòmiques. Fonts, en castellà:",
})
OBJETIVO_CA["faq"] = reemplazar_faq(OBJETIVO_CA["faq"], {
    "Quant ha de facturar un autònom per guanyar 2.000 € nets al mes?": (
        "Quant ha de facturar un autònom per guanyar 2.000 € nets al mes?",
        "A Catalunya el 2026, amb 5.000 € de despeses l'any i la quota mínima del seu tram, uns 39.730 € l'any sense IVA, uns 3.311 € al mes. A altres comunitats canvia per l'IRPF: tria la teva a la calculadora."),
    "Per què només serveix per a Catalunya?": (
        "Per què canvia segons la comunitat?",
        "L'IRPF té una part autonòmica amb escala pròpia a cada comunitat. La quota d'autònoms és igual a tot Espanya."),
})

sustitutos = {("es", "sueldo"): SUELDO_ES, ("ca", "sueldo"): SUELDO_CA, ("es", "objetivo"): OBJETIVO_ES, ("ca", "objetivo"): OBJETIVO_CA}
PAGINAS = [sustitutos.get((p["lang"], p["clave"]), p) for p in PAGINAS_ANTERIORES] + [IRPF_ES, IRPF_CA, CALENDARIO_ES, CALENDARIO_CA]
