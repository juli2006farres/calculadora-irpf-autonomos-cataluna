"""Páginas de IRPF y de sueldo neto de cada comunidad autónoma.

Los datos (escalas, mínimos y ejemplos) salen de datos_comunidades.json, que calcula
datos_comunidades.mjs con los mismos módulos que usan las calculadoras.
"""
import copy
import json
import posixpath
import re
from pathlib import Path

from contenido import BOE_CUOTA, BOE_LIRPF
from contenido_espana import (AEAT_ESCALAS, AEAT_MINIMOS, BOE_VALENCIA, FUENTES_IRPF, HACIENDA_2026,
                              IRPF_CA, IRPF_ES, SUELDO_CA, SUELDO_ES, orden_alfabetico, reemplazar_faq)
from contenido_tarifa import PAGINAS as PAGINAS_ANTERIORES

DATOS = json.loads((Path(__file__).parent / "datos_comunidades.json").read_text(encoding="utf-8"))
ORDEN_COMUNIDADES = list(DATOS["comunidades"])

# Nombre corto (títulos), forma con preposición y forma con «de».
NOMBRES = {
    "es": {
        "andalucia": ("Andalucía", "en Andalucía", "de Andalucía"),
        "aragon": ("Aragón", "en Aragón", "de Aragón"),
        "asturias": ("Asturias", "en Asturias", "de Asturias"),
        "baleares": ("Baleares", "en las Illes Balears", "de las Illes Balears"),
        "canarias": ("Canarias", "en Canarias", "de Canarias"),
        "cantabria": ("Cantabria", "en Cantabria", "de Cantabria"),
        "castilla_la_mancha": ("Castilla-La Mancha", "en Castilla-La Mancha", "de Castilla-La Mancha"),
        "castilla_y_leon": ("Castilla y León", "en Castilla y León", "de Castilla y León"),
        "cataluna": ("Cataluña", "en Cataluña", "de Cataluña"),
        "extremadura": ("Extremadura", "en Extremadura", "de Extremadura"),
        "galicia": ("Galicia", "en Galicia", "de Galicia"),
        "la_rioja": ("La Rioja", "en La Rioja", "de La Rioja"),
        "madrid": ("Madrid", "en la Comunidad de Madrid", "de la Comunidad de Madrid"),
        "murcia": ("Murcia", "en la Región de Murcia", "de la Región de Murcia"),
        "valenciana": ("Comunidad Valenciana", "en la Comunitat Valenciana", "de la Comunitat Valenciana"),
    },
    "ca": {
        "andalucia": ("Andalusia", "a Andalusia", "d'Andalusia"),
        "aragon": ("Aragó", "a l'Aragó", "de l'Aragó"),
        "asturias": ("Astúries", "a Astúries", "d'Astúries"),
        "baleares": ("Balears", "a les Illes Balears", "de les Illes Balears"),
        "canarias": ("Canàries", "a les Canàries", "de les Canàries"),
        "cantabria": ("Cantàbria", "a Cantàbria", "de Cantàbria"),
        "castilla_la_mancha": ("Castella-la Manxa", "a Castella-la Manxa", "de Castella-la Manxa"),
        "castilla_y_leon": ("Castella i Lleó", "a Castella i Lleó", "de Castella i Lleó"),
        "cataluna": ("Catalunya", "a Catalunya", "de Catalunya"),
        "extremadura": ("Extremadura", "a Extremadura", "d'Extremadura"),
        "galicia": ("Galícia", "a Galícia", "de Galícia"),
        "la_rioja": ("La Rioja", "a La Rioja", "de La Rioja"),
        "madrid": ("Madrid", "a la Comunitat de Madrid", "de la Comunitat de Madrid"),
        "murcia": ("Múrcia", "a la Regió de Múrcia", "de la Regió de Múrcia"),
        "valenciana": ("Comunitat Valenciana", "a la Comunitat Valenciana", "de la Comunitat Valenciana"),
    },
}
SLUGS = {
    "es": {"andalucia": "andalucia", "aragon": "aragon", "asturias": "asturias", "baleares": "baleares", "canarias": "canarias",
           "cantabria": "cantabria", "castilla_la_mancha": "castilla-la-mancha", "castilla_y_leon": "castilla-y-leon",
           "cataluna": "cataluna", "extremadura": "extremadura", "galicia": "galicia", "la_rioja": "la-rioja",
           "madrid": "madrid", "murcia": "murcia", "valenciana": "comunidad-valenciana"},
    "ca": {"andalucia": "andalusia", "aragon": "arago", "asturias": "asturies", "baleares": "illes-balears", "canarias": "canaries",
           "cantabria": "cantabria", "castilla_la_mancha": "castella-la-manxa", "castilla_y_leon": "castella-i-lleo",
           "cataluna": "catalunya", "extremadura": "extremadura", "galicia": "galicia", "la_rioja": "la-rioja",
           "madrid": "madrid", "murcia": "murcia", "valenciana": "comunitat-valenciana"},
}
BASES = {
    "irpf": {"es": "calculadora-irpf-autonomos/", "ca": "ca/calculadora-irpf-autonoms/"},
    "sueldo": {"es": "sueldo-neto-autonomo/", "ca": "ca/sou-net-autonom/"},
}
OTRAS = {
    "cuota": {"es": "cuota-autonomos-2026/", "ca": "ca/quota-autonoms-2026/"},
    "tarifa": {"es": "tarifa-plana-autonomos-2026/", "ca": "ca/tarifa-plana-autonoms-2026/"},
    "irpf_cat": {"es": "", "ca": "ca/"},
}


def clave(tipo, c):
    return f"{tipo}_{c}"


# La página de IRPF de Cataluña ya existe: es la portada de la web.
RUTAS_COMUNIDADES = {}
for c in ORDEN_COMUNIDADES:
    if c != "cataluna":
        RUTAS_COMUNIDADES[clave("irpf", c)] = {l: BASES["irpf"][l] + SLUGS[l][c] + "/" for l in ("es", "ca")}
    RUTAS_COMUNIDADES[clave("sueldo", c)] = {l: BASES["sueldo"][l] + SLUGS[l][c] + "/" for l in ("es", "ca")}
PADRE_COMUNIDADES = {k: ("irpf_es" if k.startswith("irpf_") else "sueldo") for k in RUTAS_COMUNIDADES}


def ruta(tipo, c, lang):
    if tipo == "irpf" and c == "cataluna":
        return OTRAS["irpf_cat"][lang]
    return RUTAS_COMUNIDADES[clave(tipo, c)][lang]


def relativa(desde, hasta):
    r = posixpath.relpath(hasta.rstrip("/") or ".", desde.rstrip("/") or ".")
    return "./" if r == "." else r + "/"


# ---------------------------------------------------------------- Formatos
def numero(valor, decimales=None):
    if decimales is None:
        decimales = 0 if float(valor).is_integer() else 2
    texto = f"{valor:,.{decimales}f}"
    return texto.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def eur(valor, decimales=None):
    return numero(valor, decimales) + " €"


def pct(valor):
    return numero(valor, 0 if float(valor).is_integer() else (1 if round(valor, 1) == valor else 2)) + " %"


def tramo_texto(desde, hasta, lang):
    if lang == "es":
        if hasta is None:
            return f"Más de {eur(desde)}"
        return f"Hasta {eur(hasta)}" if desde == 0 else f"De {eur(desde)} a {eur(hasta)}"
    if hasta is None:
        return f"Més de {eur(desde)}"
    return f"Fins a {eur(hasta)}" if desde == 0 else f"De {eur(desde)} a {eur(hasta)}"


def preseleccionar(formulario, c):
    """Marca la comunidad `c` en el desplegable de comunidades del formulario."""
    m = re.search(r'<select id="comunidad".*?</select>', formulario, flags=re.S)
    if not m:
        raise SystemExit("No hay desplegable de comunidades en el formulario")
    bloque = m.group(0).replace(" selected", "")
    nuevo = bloque.replace(f'<option value="{c}">', f'<option value="{c}" selected>', 1)
    if nuevo == bloque:
        raise SystemExit(f"No se encontró la comunidad {c} en el desplegable")
    return formulario.replace(m.group(0), nuevo, 1)


EJEMPLO_REF = 2  # índice del ejemplo de 40.000 € en DATOS["ejemplos"]
assert DATOS["ejemplos"][EJEMPLO_REF]["ingresos"] == 40_000


def ref(c):
    return DATOS["comunidades"][c]["ejemplos"][EJEMPLO_REF]


def marginal_maximo(c):
    ultima = DATOS["comunidades"][c]["marginal_conjunto"][-1]
    return ultima["total"], ultima["desde"]


# ---------------------------------------------------------------- Bloques comunes
def lista_comunidades(lang, tipo, desde, actual=None):
    """Enlaces a la página de cada comunidad, con una cifra del ejemplo de 40.000 €."""
    items = []
    for c in sorted(ORDEN_COMUNIDADES, key=lambda x: orden_alfabetico(NOMBRES[lang][x][0])):
        if c == actual:
            continue
        e = ref(c)
        if tipo == "irpf":
            dato = {"es": f"{eur(round(e['irpf']))} de IRPF con 40.000 €", "ca": f"{eur(round(e['irpf']))} d'IRPF amb 40.000 €"}[lang]
        else:
            dato = {"es": f"{eur(round(e['neto_mensual']))} al mes con 40.000 €", "ca": f"{eur(round(e['neto_mensual']))} al mes amb 40.000 €"}[lang]
        items.append(f'<li><a href="{relativa(desde, ruta(tipo, c, lang))}">{NOMBRES[lang][c][0]}<span>{dato}</span></a></li>')
    cuota = eur(ref(ORDEN_COMUNIDADES[0])["cuota_mensual"])
    nota = {
        "es": f"Cifras de un autónomo con 40.000 € de facturación, 5.000 € de gastos y la cuota mínima de su tramo ({cuota} al mes), en 2026.",
        "ca": f"Xifres d'un autònom amb 40.000 € de facturació, 5.000 € de despeses i la quota mínima del seu tram ({cuota} al mes), el 2026.",
    }[lang]
    return '<ul class="comunidades">\n      ' + "\n      ".join(items) + f'\n    </ul>\n    <p class="nota">{nota}</p>'


def tabla_ejemplos(lang, c, tipo):
    filas = []
    for e in DATOS["comunidades"][c]["ejemplos"]:
        celdas = [eur(e["ingresos"]), eur(e["gastos"])]
        if tipo == "sueldo":
            celdas.append(eur(e["cuota_mensual"]))
        celdas += [eur(e["irpf"])]
        if tipo == "irpf":
            celdas.append(pct(e["tipo_medio"]))
        celdas += [eur(e["neto_mensual"]), f"{e['puesto']} / 15"]
        filas.append("        <tr>" + "".join(f"<td>{x}</td>" for x in celdas) + "</tr>")
    if tipo == "irpf":
        cab = {"es": ["Facturación", "Gastos", "IRPF del año", "Tipo medio", "Te queda al mes", "Puesto"],
               "ca": ["Facturació", "Despeses", "IRPF de l'any", "Tipus mitjà", "Et queda al mes", "Posició"]}[lang]
    else:
        cab = {"es": ["Facturación", "Gastos", "Cuota al mes", "IRPF del año", "Te queda al mes", "Puesto"],
               "ca": ["Facturació", "Despeses", "Quota al mes", "IRPF de l'any", "Et queda al mes", "Posició"]}[lang]
    cabecera = "".join(f"<th>{x}</th>" for x in cab)
    cuerpo = "\n".join(filas)
    return f"""<div class="tabla-ancha">
    <table>
      <thead><tr>{cabecera}</tr></thead>
      <tbody>
{cuerpo}
      </tbody>
    </table>
    </div>"""


SUPUESTO = {
    "es": "Autónomo en estimación directa simplificada, sin hijos, sin la reducción por inicio de actividad y pagando la cuota mínima de su tramo de 2026. El puesto ordena las 15 comunidades de menos a más IRPF.",
    "ca": "Autònom en estimació directa simplificada, sense fills, sense la reducció per inici d'activitat i pagant la quota mínima del seu tram del 2026. La posició ordena les 15 comunitats de menys a més IRPF.",
}


def comparacion(lang, c):
    e = ref(c)
    en = NOMBRES[lang][c][1]
    barata, cara = e["mas_barata"], e["mas_cara"]
    if lang == "es":
        if c == barata:
            return f"Con 40.000 € de facturación, {en} es donde menos IRPF paga un autónomo: {eur(e['irpf'])}, frente a {eur(e['irpf_mas_cara'])} {NOMBRES[lang][cara][1]}, la que más."
        if c == cara:
            return f"Con 40.000 € de facturación, {en} es donde más IRPF paga un autónomo: {eur(e['irpf'])}, frente a {eur(e['irpf_mas_barata'])} {NOMBRES[lang][barata][1]}, la que menos."
        return (f"Con 40.000 € de facturación, un autónomo paga {eur(e['irpf'])} de IRPF {en}, el puesto {e['puesto']} de 15. "
                f"La que menos cobra es {NOMBRES[lang][barata][0]}, con {eur(e['irpf_mas_barata'])}, y la que más, {NOMBRES[lang][cara][0]}, con {eur(e['irpf_mas_cara'])}.")
    if c == barata:
        return f"Amb 40.000 € de facturació, {en} és on menys IRPF paga un autònom: {eur(e['irpf'])}, davant {eur(e['irpf_mas_cara'])} {NOMBRES[lang][cara][1]}, la que més."
    if c == cara:
        return f"Amb 40.000 € de facturació, {en} és on més IRPF paga un autònom: {eur(e['irpf'])}, davant {eur(e['irpf_mas_barata'])} {NOMBRES[lang][barata][1]}, la que menys."
    return (f"Amb 40.000 € de facturació, un autònom paga {eur(e['irpf'])} d'IRPF {en}, la posició {e['puesto']} de 15. "
            f"La que menys cobra és {NOMBRES[lang][barata][0]}, amb {eur(e['irpf_mas_barata'])}, i la que més, {NOMBRES[lang][cara][0]}, amb {eur(e['irpf_mas_cara'])}.")


def sujeto(lang, c, mayuscula=False):
    """Nombre de la comunidad con su artículo, para usarlo como sujeto: «la Comunitat Valenciana», «l'Aragó»."""
    forma = NOMBRES[lang][c][1].split(" ", 1)[1]
    return forma[0].upper() + forma[1:] if mayuscula else forma


def plural(lang, c):
    return sujeto(lang, c).startswith(("las ", "les "))


def ejemplo_minimo(c):
    """Primer mínimo en que la comunidad se aparta del estatal: (concepto, autonómico, estatal)."""
    m, est = DATOS["comunidades"][c]["minimos"], DATOS["minimos_estatales"]
    pares = [("contribuyente", m["contribuyente"], est["contribuyente"])]
    pares += [(f"hijo{i}", a, b) for i, (a, b) in enumerate(zip(m["descendientes"], est["descendientes"]), 1)]
    pares += [("menor3", m["menor3"], est["menor3"])]
    return next(p for p in pares if p[1] != p[2])


CONCEPTO_MINIMO = {
    "es": {"contribuyente": "el mínimo del contribuyente", "hijo1": "el mínimo por el primer hijo", "hijo2": "el mínimo por el segundo hijo",
           "hijo3": "el mínimo por el tercer hijo", "hijo4": "el mínimo por el cuarto hijo", "menor3": "el aumento por cada hijo menor de 3 años"},
    "ca": {"contribuyente": "el mínim del contribuent", "hijo1": "el mínim pel primer fill", "hijo2": "el mínim pel segon fill",
           "hijo3": "el mínim pel tercer fill", "hijo4": "el mínim pel quart fill", "menor3": "l'augment per cada fill menor de 3 anys"},
}


def cifras(items):
    lis = "".join(f"<li><strong>{a}</strong><span>{b}</span></li>" for a, b in items)
    return f'<ul class="cifras">{lis}</ul>'


# ---------------------------------------------------------------- IRPF de cada comunidad
def tabla_marginal(lang, c):
    corto = NOMBRES[lang][c][0]
    filas = []
    for f in DATOS["comunidades"][c]["marginal_conjunto"]:
        filas.append(f"        <tr><td>{tramo_texto(f['desde'], f['hasta'], lang)}</td><td>{pct(f['estatal'])}</td>"
                     f"<td>{pct(f['autonomico'])}</td><td>{pct(f['total'])}</td></tr>")
    cab = {"es": ["Base liquidable", "Estatal", corto, "Total"], "ca": ["Base liquidable", "Estatal", corto, "Total"]}[lang]
    cabecera = "".join(f"<th>{x}</th>" for x in cab)
    cuerpo = "\n".join(filas)
    return f"""<div class="tabla-ancha">
    <table>
      <thead><tr>{cabecera}</tr></thead>
      <tbody>
{cuerpo}
      </tbody>
    </table>
    </div>"""


def bloque_minimos(lang, c):
    d = DATOS["comunidades"][c]
    m, est = d["minimos"], DATOS["minimos_estatales"]
    de = NOMBRES[lang][c][2]
    if not d["minimos_propios"]:
        if lang == "es":
            return (f"<p>Para la parte autonómica del IRPF, la escala {de} se aplica con los mismos mínimos que la estatal: "
                    f"{eur(est['contribuyente'])} por contribuyente, {eur(est['descendientes'][0])} por el primer hijo, "
                    f"{eur(est['descendientes'][1])} por el segundo, {eur(est['descendientes'][2])} por el tercero, "
                    f"{eur(est['descendientes'][3])} por el cuarto y siguientes, y {eur(est['menor3'])} más por cada hijo menor de 3 años.</p>")
        return (f"<p>Per a la part autonòmica de l'IRPF, l'escala {de} s'aplica amb els mateixos mínims que l'estatal: "
                f"{eur(est['contribuyente'])} per contribuent, {eur(est['descendientes'][0])} pel primer fill, "
                f"{eur(est['descendientes'][1])} pel segon, {eur(est['descendientes'][2])} pel tercer, "
                f"{eur(est['descendientes'][3])} pel quart i següents, i {eur(est['menor3'])} més per cada fill menor de 3 anys.</p>")
    conceptos = {
        "es": ["Contribuyente", "Primer hijo", "Segundo hijo", "Tercer hijo", "Cuarto hijo y siguientes", "Por cada hijo menor de 3 años"],
        "ca": ["Contribuent", "Primer fill", "Segon fill", "Tercer fill", "Quart fill i següents", "Per cada fill menor de 3 anys"],
    }[lang]
    valores = [(m["contribuyente"], est["contribuyente"])] + list(zip(m["descendientes"], est["descendientes"])) + [(m["menor3"], est["menor3"])]
    # La comunidad va en la última columna, que es la que se destaca en negrita.
    filas = "\n".join(f"        <tr><td>{t}</td><td>{eur(b)}</td><td>{eur(a)}</td></tr>" for t, (a, b) in zip(conceptos, valores))
    corto = NOMBRES[lang][c][0]
    cab = {"es": ("Mínimo", "Estatal", corto), "ca": ("Mínim", "Estatal", corto)}[lang]
    todos = all(a > b for a, b in valores)
    intro = {
        "es": f"<p>La comunidad tiene mínimos propios, {'más altos que los estatales' if todos else 'algunos más altos que los estatales'}, que solo se usan para calcular la parte autonómica del impuesto.</p>",
        "ca": f"<p>La comunitat té mínims propis, {'més alts que els estatals' if todos else 'alguns més alts que els estatals'}, que només es fan servir per calcular la part autonòmica de l'impost.</p>",
    }[lang]
    return f"""{intro}
    <div class="tabla-ancha">
    <table>
      <thead><tr><th>{cab[0]}</th><th>{cab[1]}</th><th>{cab[2]}</th></tr></thead>
      <tbody>
{filas}
      </tbody>
    </table>
    </div>"""


def cambio_2026(lang, c):
    d = DATOS["comunidades"][c]
    if not d["escala_2025"]:
        return ""
    antes, ahora = d["escala_2025"], d["escala_2026"]
    if [t["hasta"] for t in antes] != [t["hasta"] for t in ahora]:
        raise SystemExit(f"Los tramos de {c} cambian en 2026: hay que redactar el cambio a mano")
    cambios = [(a["tipo"], b["tipo"]) for a, b in zip(antes, ahora) if a["tipo"] != b["tipo"]]
    # El texto dice «los N primeros tramos»: solo vale si los que cambian son los primeros.
    if [a["tipo"] != b["tipo"] for a, b in zip(antes, ahora)] != [i < len(cambios) for i in range(len(antes))]:
        raise SystemExit(f"En {c} no cambian solo los primeros tramos: hay que redactar el cambio a mano")
    if c == "valenciana":
        fuente = {"es": f'la <a href="{BOE_VALENCIA}">Ley 5/2026</a>', "ca": f'la <a href="{BOE_VALENCIA}">Llei 5/2026</a>'}[lang]
    else:
        fuente = {"es": f'el <a href="{HACIENDA_2026}">informe de Hacienda de 2026</a>', "ca": f"l'<a href=\"{HACIENDA_2026}\">informe d'Hisenda del 2026</a>"}[lang]
    if lang == "es":
        if len(cambios) == len(antes):
            que = (f"bajan los tipos de todos los tramos: el primero pasa del {pct(cambios[0][0])} al {pct(cambios[0][1])} "
                   f"y el último, del {pct(cambios[-1][0])} al {pct(cambios[-1][1])}")
        else:
            pares = [f"del {pct(x)} al {pct(y)}" for x, y in cambios]
            lista = pares[0] if len(pares) == 1 else ", ".join(pares[:-1]) + " y " + pares[-1]
            que = f"bajan los tipos de los {len(cambios)} primeros tramos, {lista}; el resto no cambia"
        return f"<p><strong>Cambia en 2026.</strong> Según {fuente}, {que}. La calculadora usa la escala del año que elijas.</p>"
    if len(cambios) == len(antes):
        que = (f"baixen els tipus de tots els trams: el primer passa del {pct(cambios[0][0])} al {pct(cambios[0][1])} "
               f"i l'últim, del {pct(cambios[-1][0])} al {pct(cambios[-1][1])}")
    else:
        pares = [f"del {pct(x)} al {pct(y)}" for x, y in cambios]
        lista = pares[0] if len(pares) == 1 else ", ".join(pares[:-1]) + " i " + pares[-1]
        que = f"baixen els tipus dels {len(cambios)} primers trams, {lista}; la resta no canvia"
    return f"<p><strong>Canvia el 2026.</strong> Segons {fuente}, {que}. La calculadora fa servir l'escala de l'any que triïs.</p>"


def extra_irpf(lang, c):
    d = DATOS["comunidades"][c]
    corto, en, de = NOMBRES[lang][c]
    desde = ruta("irpf", c, lang)
    e = ref(c)
    maximo, umbral = marginal_maximo(c)
    if lang == "es":
        cif = cifras([
            (f"{pct(d['tipo_minimo'])} – {pct(d['tipo_maximo'])}", "Tipos de la escala autonómica en 2026"),
            (pct(maximo), f"Tipo marginal máximo, estatal y autonómico, desde {eur(umbral)}"),
            (f"{e['puesto']} de 15", "Puesto con 40.000 € de facturación, de menos a más IRPF"),
        ])
        return f"""<section class="tarjeta">
    <h2>El IRPF {de} en 2026</h2>
    {cif}
    <p>El IRPF se calcula con dos escalas: la estatal, igual en toda España, y la autonómica {de}. Cada tipo se aplica solo a la parte de la base que cae en su tramo, así que pasar a un tramo superior no encarece lo que ya ganabas.</p>
    {cambio_2026(lang, c)}
    <h3 class="subtitulo">Tipos marginales: estatal + autonómico</h3>
    {tabla_marginal(lang, c)}
    <p class="nota">La base liquidable es tu rendimiento neto después de gastos, cuotas y reducciones.</p>
  </section>

  <section class="tarjeta">
    <h2>Mínimo personal y familiar {en}</h2>
    {bloque_minimos(lang, c)}
  </section>

  <section class="tarjeta">
    <h2>Ejemplos de IRPF de un autónomo {en}</h2>
    <p>{SUPUESTO[lang]}</p>
    {tabla_ejemplos(lang, c, "irpf")}
    <p class="nota">{comparacion(lang, c)}</p>
  </section>

  <section class="tarjeta">
    <h2>IRPF de autónomos en otras comunidades</h2>
    {lista_comunidades(lang, "irpf", desde, c)}
  </section>

  """
    cif = cifras([
        (f"{pct(d['tipo_minimo'])} – {pct(d['tipo_maximo'])}", "Tipus de l'escala autonòmica el 2026"),
        (pct(maximo), f"Tipus marginal màxim, estatal i autonòmic, des de {eur(umbral)}"),
        (f"{e['puesto']} de 15", "Posició amb 40.000 € de facturació, de menys a més IRPF"),
    ])
    return f"""<section class="tarjeta">
    <h2>L'IRPF {de} el 2026</h2>
    {cif}
    <p>L'IRPF es calcula amb dues escales: l'estatal, igual a tot Espanya, i l'autonòmica {de}. Cada tipus s'aplica només a la part de la base que cau al seu tram, així que passar a un tram superior no encareix el que ja guanyaves.</p>
    {cambio_2026(lang, c)}
    <h3 class="subtitulo">Tipus marginals: estatal + autonòmic</h3>
    {tabla_marginal(lang, c)}
    <p class="nota">La base liquidable és el teu rendiment net després de despeses, quotes i reduccions.</p>
  </section>

  <section class="tarjeta">
    <h2>Mínim personal i familiar {en}</h2>
    {bloque_minimos(lang, c)}
  </section>

  <section class="tarjeta">
    <h2>Exemples d'IRPF d'un autònom {en}</h2>
    <p>{SUPUESTO[lang]}</p>
    {tabla_ejemplos(lang, c, "irpf")}
    <p class="nota">{comparacion(lang, c)}</p>
  </section>

  <section class="tarjeta">
    <h2>IRPF d'autònoms a altres comunitats</h2>
    {lista_comunidades(lang, "irpf", desde, c)}
  </section>

  """


def faq_irpf(lang, c):
    d = DATOS["comunidades"][c]
    corto, en, de = NOMBRES[lang][c]
    e = ref(c)
    maximo, umbral = marginal_maximo(c)
    primero = d["marginal_conjunto"][0]["total"]
    cuota = relativa(ruta("irpf", c, lang), OTRAS["cuota"][lang])
    if d["minimos_propios"]:
        concepto, autonomico, estatal = ejemplo_minimo(c)
    if e["puesto"] == 1:
        puesto = {"es": "Es la comunidad que menos IRPF cobra de las 15.", "ca": "És la comunitat que menys IRPF cobra de les 15."}[lang]
    elif e["puesto"] == 15:
        puesto = {"es": "Es la comunidad que más IRPF cobra de las 15.", "ca": "És la comunitat que més IRPF cobra de les 15."}[lang]
    else:
        puesto = {"es": f"Es el puesto {e['puesto']} de 15, de menos a más IRPF.", "ca": f"És la posició {e['puesto']} de 15, de menys a més IRPF."}[lang]
    if lang == "es":
        faq = [
            (f"¿Cuánto IRPF paga un autónomo {en}?",
             f"Depende de lo que gane. Con 40.000 € de facturación, 5.000 € de gastos y la cuota mínima de su tramo en 2026, unos {eur(round(e['irpf']))} al año, "
             f"un tipo medio del {pct(e['tipo_medio'])}, y le quedan unos {eur(round(e['neto_mensual']))} al mes. {puesto}"),
            (f"¿Cuáles son los tipos del IRPF {en} en 2026?",
             f"La escala autonómica va del {pct(d['tipo_minimo'])} al {pct(d['tipo_maximo'])}. Sumada a la estatal, el tipo marginal empieza en el {pct(primero)} "
             f"y llega al {pct(maximo)} a partir de {eur(umbral)} de base liquidable."),
            (f"¿{'Tienen' if plural(lang, c) else 'Tiene'} {sujeto(lang, c)} mínimos personales propios?",
             (f"Sí. Por ejemplo, {CONCEPTO_MINIMO[lang][concepto]} es de {eur(autonomico)} para la parte autonómica, frente a los {eur(estatal)} estatales. La calculadora los aplica."
              if d["minimos_propios"] else
              f"No. Para la parte autonómica usa los mismos mínimos que el Estado, como los {eur(DATOS['minimos_estatales']['contribuyente'])} del contribuyente.")),
        ]
        if d["escala_2025"]:
            faq.append(("¿Qué cambia en 2026?", re.sub(r"</?p>|<strong>.*?</strong> ", "", cambio_2026(lang, c))))
        faq += [
            (f"¿Incluye las deducciones autonómicas {de}?",
             "No. Las deducciones por alquiler, hijos, donativos y otras dependen de tu situación y no entran en el cálculo, así que el resultado real puede ser algo menor."),
            ("¿La cuota de autónomos también cambia según la comunidad?",
             f'No. La cuota de autónomos es igual en toda España y depende solo de tus rendimientos. Puedes calcularla en la <a href="{cuota}">calculadora de cuota de autónomos</a>.'),
        ]
        return faq
    faq = [
        (f"Quant IRPF paga un autònom {en}?",
         f"Depèn del que guanyi. Amb 40.000 € de facturació, 5.000 € de despeses i la quota mínima del seu tram el 2026, uns {eur(round(e['irpf']))} l'any, "
         f"un tipus mitjà del {pct(e['tipo_medio'])}, i li queden uns {eur(round(e['neto_mensual']))} al mes. {puesto}"),
        (f"Quins són els tipus de l'IRPF {en} el 2026?",
         f"L'escala autonòmica va del {pct(d['tipo_minimo'])} al {pct(d['tipo_maximo'])}. Sumada a l'estatal, el tipus marginal comença al {pct(primero)} "
         f"i arriba al {pct(maximo)} a partir de {eur(umbral)} de base liquidable."),
        (f"{sujeto(lang, c, True)} {'tenen' if plural(lang, c) else 'té'} mínims personals propis?",
         (f"Sí. Per exemple, {CONCEPTO_MINIMO[lang][concepto]} és de {eur(autonomico)} per a la part autonòmica, davant els {eur(estatal)} estatals. La calculadora els aplica."
          if d["minimos_propios"] else
          f"No. Per a la part autonòmica fa servir els mateixos mínims que l'Estat, com els {eur(DATOS['minimos_estatales']['contribuyente'])} del contribuent.")),
    ]
    if d["escala_2025"]:
        faq.append(("Què canvia el 2026?", re.sub(r"</?p>|<strong>.*?</strong> ", "", cambio_2026(lang, c))))
    faq += [
        (f"Inclou les deduccions autonòmiques {de}?",
         "No. Les deduccions per lloguer, fills, donatius i altres depenen de la teva situació i no entren al càlcul, així que el resultat real pot ser una mica menor."),
        ("La quota d'autònoms també canvia segons la comunitat?",
         f'No. La quota d\'autònoms és igual a tot Espanya i depèn només dels teus rendiments. La pots calcular a la <a href="{cuota}">calculadora de quota d\'autònoms</a>.'),
    ]
    return faq


def fuentes_irpf(c):
    fuentes = [FUENTES_IRPF[0], FUENTES_IRPF[1], FUENTES_IRPF[2], FUENTES_IRPF[3]]
    if c == "valenciana":
        fuentes.append(FUENTES_IRPF[4])
    return fuentes


def ajustar(texto, maximo, alternativas):
    """Devuelve el primer texto que cabe en `maximo` caracteres."""
    for t in [texto, *alternativas]:
        if len(t) <= maximo:
            return t
    raise SystemExit(f"Ningún texto cabe en {maximo} caracteres: {texto}")


def pagina_irpf(lang, c):
    base = IRPF_ES if lang == "es" else IRPF_CA
    p = copy.deepcopy(base)
    corto, en, de = NOMBRES[lang][c]
    if lang == "es":
        titulo = ajustar(f"Calculadora IRPF autónomos {corto} 2026 · Gratis", 70, [f"IRPF autónomos {corto} 2026 · Calculadora"])
        descripcion = ajustar(
            f"Calcula gratis el IRPF de un autónomo {en} en 2026, con la escala autonómica, los tipos marginales, los mínimos y ejemplos.", 155,
            [f"IRPF de autónomos {en} en 2026: calculadora gratis con la escala autonómica, los tipos y ejemplos."])
        p.update({
            "titulo": titulo,
            "descripcion": descripcion,
            "og_titulo": f"Calculadora de IRPF de autónomos {en}",
            "og_descripcion": f"El IRPF de un autónomo {en}, con su escala, sus mínimos y ejemplos.",
            "h1": f"Calculadora de IRPF para autónomos {en}",
            "entradilla": f"Calcula el IRPF de tu actividad con la escala estatal y la {de}, en 2025 o 2026, y mira cuánto pagarías con los mismos datos en las otras 14 comunidades.",
            "aviso": "es una estimación orientativa y no sustituye la declaración ni el consejo de un asesor fiscal. No incluye las deducciones autonómicas. Los mínimos autonómicos de 2026 se suponen iguales a los de 2025, porque el informe de Hacienda no recoge cambios. Fuentes:",
        })
    else:
        titulo = ajustar(f"Calculadora IRPF autònoms {corto} 2026 · Gratuïta", 70, [f"IRPF autònoms {corto} 2026 · Calculadora"])
        descripcion = ajustar(
            f"Calcula gratis l'IRPF d'un autònom {en} el 2026, amb l'escala autonòmica, els tipus marginals, els mínims i exemples.", 155,
            [f"IRPF d'autònoms {en} el 2026: calculadora gratuïta amb l'escala autonòmica, els tipus i exemples."])
        p.update({
            "titulo": titulo,
            "descripcion": descripcion,
            "og_titulo": f"Calculadora d'IRPF d'autònoms {en}",
            "og_descripcion": f"L'IRPF d'un autònom {en}, amb la seva escala, els seus mínims i exemples.",
            "h1": f"Calculadora d'IRPF per a autònoms {en}",
            "entradilla": f"Calcula l'IRPF de la teva activitat amb l'escala estatal i la {de}, el 2025 o el 2026, i mira quant pagaries amb les mateixes dades a les altres 14 comunitats.",
            "aviso": "és una estimació orientativa i no substitueix la declaració ni el consell d'un assessor fiscal. No inclou les deduccions autonòmiques. Els mínims autonòmics del 2026 se suposen iguals als del 2025, perquè l'informe d'Hisenda no en recull canvis. Fonts, en castellà:",
        })
    p["clave"] = clave("irpf", c)
    p["formulario"] = preseleccionar(p["formulario"], c)
    p["extra"] = extra_irpf(lang, c)
    p["faq"] = faq_irpf(lang, c)
    p["fuentes"] = fuentes_irpf(c)
    return p


# ---------------------------------------------------------------- Sueldo neto de cada comunidad
def extra_sueldo(lang, c):
    corto, en, de = NOMBRES[lang][c]
    desde = ruta("sueldo", c, lang)
    e = ref(c)
    irpf = relativa(desde, ruta("irpf", c, lang))
    diferencia = round(e["irpf"] - e["irpf_mas_barata"])
    if lang == "es":
        cif = cifras([
            (eur(round(e["neto_mensual"])), "Al mes con 40.000 € de facturación y 5.000 € de gastos"),
            (eur(round(e["irpf"])), f"De IRPF en el año {en}"),
            (f"{e['puesto']} de 15", "Puesto de la comunidad, de más a menos sueldo neto"),
        ])
        frase = (f"{NOMBRES[lang][c][1][0].upper() + NOMBRES[lang][c][1][1:]} es donde más le queda a un autónomo con 40.000 € de facturación."
                 if diferencia == 0 else
                 f"Con 40.000 € de facturación, el mismo autónomo tendría {eur(diferencia)} más al año {NOMBRES[lang][e['mas_barata']][1]}, donde menos IRPF se paga. La cuota de autónomos es la misma en toda España: la diferencia es solo el IRPF.")
        return f"""<section class="tarjeta">
    <h2>Cuánto le queda a un autónomo {en}</h2>
    {cif}
    <p>{SUPUESTO[lang].replace("de menos a más IRPF", "de más a menos sueldo neto")}</p>
    {tabla_ejemplos(lang, c, "sueldo")}
    <p class="nota">{frase} <a href="{irpf}">Ver la escala del IRPF {de}</a>.</p>
  </section>

  <section class="tarjeta">
    <h2>Sueldo neto de autónomo en otras comunidades</h2>
    {lista_comunidades(lang, "sueldo", desde, c)}
  </section>

  """
    cif = cifras([
        (eur(round(e["neto_mensual"])), "Al mes amb 40.000 € de facturació i 5.000 € de despeses"),
        (eur(round(e["irpf"])), f"D'IRPF a l'any {en}"),
        (f"{e['puesto']} de 15", "Posició de la comunitat, de més a menys sou net"),
    ])
    frase = (f"{NOMBRES[lang][c][1][0].upper() + NOMBRES[lang][c][1][1:]} és on més li queda a un autònom amb 40.000 € de facturació."
             if diferencia == 0 else
             f"Amb 40.000 € de facturació, el mateix autònom tindria {eur(diferencia)} més l'any {NOMBRES[lang][e['mas_barata']][1]}, on menys IRPF es paga. La quota d'autònoms és la mateixa a tot Espanya: la diferència és només l'IRPF.")
    return f"""<section class="tarjeta">
    <h2>Quant li queda a un autònom {en}</h2>
    {cif}
    <p>{SUPUESTO[lang].replace("de menys a més IRPF", "de més a menys sou net")}</p>
    {tabla_ejemplos(lang, c, "sueldo")}
    <p class="nota">{frase} <a href="{irpf}">Veure l'escala de l'IRPF {de}</a>.</p>
  </section>

  <section class="tarjeta">
    <h2>Sou net d'autònom a altres comunitats</h2>
    {lista_comunidades(lang, "sueldo", desde, c)}
  </section>

  """


def posicion(lang, c):
    """Frase con el puesto de la comunidad, salvo si ya se ha nombrado como la primera o la última."""
    e = ref(c)
    if c in (e["mas_barata"], e["mas_cara"]):
        return ""
    s, pl = sujeto(lang, c, True), plural(lang, c)
    return {"es": f" {s} {'están' if pl else 'está'} en el puesto {e['puesto']} de 15.",
            "ca": f" {s} {'són' if pl else 'és'} a la posició {e['puesto']} de 15."}[lang]


def faq_sueldo(lang, c):
    corto, en, de = NOMBRES[lang][c]
    e = ref(c)
    desde = ruta("sueldo", c, lang)
    cuota = relativa(desde, OTRAS["cuota"][lang])
    tarifa = relativa(desde, OTRAS["tarifa"][lang])
    barata, cara = e["mas_barata"], e["mas_cara"]
    if lang == "es":
        return [
            (f"¿Cuánto le queda a un autónomo {en} que factura 40.000 € al año?",
             f"En 2026, con 5.000 € de gastos y la cuota mínima de su tramo ({eur(e['cuota_mensual'])} al mes), paga unos {eur(round(e['irpf']))} de IRPF y le quedan unos {eur(round(e['neto_mensual']))} al mes en 12 pagas."),
            ("¿En qué comunidad le queda más dinero a un autónomo?",
             f"Con 40.000 € de facturación, donde más le queda es {NOMBRES[lang][barata][1]}, y donde menos, {NOMBRES[lang][cara][1]}.{posicion(lang, c)} El orden cambia con los ingresos: la tabla de ejemplos lo muestra con otras cifras."),
            (f"¿La cuota de autónomos es distinta {en}?",
             f'No. La cuota es igual en toda España y depende solo de tus rendimientos. Puedes ver tu tramo en la <a href="{cuota}">calculadora de cuota de autónomos</a>.'),
            ("¿Y si tengo la tarifa plana?",
             f'Escribe 88,64 € en el campo de la cuota, que es lo que se paga en 2026 con la tarifa plana. En la <a href="{tarifa}">calculadora de la tarifa plana</a> puedes ver cuánto te ahorras y si puedes alargarla.'),
            ("¿Qué no incluye?",
             f"Las deducciones autonómicas {de}, otras rentas como un sueldo o alquileres, el mínimo por hijos y la tributación conjunta."),
        ]
    return [
        (f"Quant li queda a un autònom {en} que factura 40.000 € l'any?",
         f"El 2026, amb 5.000 € de despeses i la quota mínima del seu tram ({eur(e['cuota_mensual'])} al mes), paga uns {eur(round(e['irpf']))} d'IRPF i li queden uns {eur(round(e['neto_mensual']))} al mes en 12 pagues."),
        ("A quina comunitat li queden més diners a un autònom?",
         f"Amb 40.000 € de facturació, on més li queda és {NOMBRES[lang][barata][1]}, i on menys, {NOMBRES[lang][cara][1]}.{posicion(lang, c)} L'ordre canvia amb els ingressos: la taula d'exemples ho mostra amb altres xifres."),
        (f"La quota d'autònoms és diferent {en}?",
         f'No. La quota és igual a tot Espanya i depèn només dels teus rendiments. Pots veure el teu tram a la <a href="{cuota}">calculadora de quota d\'autònoms</a>.'),
        ("I si tinc la tarifa plana?",
         f'Escriu 88,64 € al camp de la quota, que és el que es paga el 2026 amb la tarifa plana. A la <a href="{tarifa}">calculadora de la tarifa plana</a> pots veure quant t\'estalvies i si la pots allargar.'),
        ("Què no inclou?",
         f"Les deduccions autonòmiques {de}, altres rendes com un sou o lloguers, el mínim per fills i la tributació conjunta."),
    ]


def pagina_sueldo(lang, c):
    base = SUELDO_ES if lang == "es" else SUELDO_CA
    p = copy.deepcopy(base)
    corto, en, de = NOMBRES[lang][c]
    if lang == "es":
        p.update({
            "titulo": ajustar(f"Sueldo neto autónomo {corto} 2026 · Calculadora gratis", 70, [f"Sueldo neto autónomo {corto} 2026 · Calculadora"]),
            "descripcion": ajustar(
                f"Calcula cuánto le queda al mes a un autónomo {en} en 2026, tras gastos, cuota de autónomos e IRPF, con ejemplos y comparado con otras comunidades.", 155,
                [f"Cuánto le queda al mes a un autónomo {en} en 2026 tras gastos, cuota e IRPF. Calculadora gratis con ejemplos."]),
            "og_titulo": f"Calculadora de sueldo neto de autónomo {en}",
            "og_descripcion": f"Lo que le queda al mes a un autónomo {en} tras gastos, cuota e IRPF.",
            "h1": f"Sueldo neto de un autónomo {en}: calculadora 2026",
            "entradilla": f"Calcula lo que te queda limpio cada mes {en} después de gastos, cuota de autónomos e IRPF, con las tablas oficiales de 2026, y compáralo con las demás comunidades.",
        })
    else:
        p.update({
            "titulo": ajustar(f"Sou net autònom {corto} 2026 · Calculadora gratuïta", 70, [f"Sou net autònom {corto} 2026 · Calculadora"]),
            "descripcion": ajustar(
                f"Calcula quant li queda al mes a un autònom {en} el 2026, després de despeses, quota d'autònoms i IRPF, amb exemples i comparat amb altres comunitats.", 155,
                [f"Quant li queda al mes a un autònom {en} el 2026 després de despeses, quota i IRPF. Calculadora gratuïta amb exemples."]),
            "og_titulo": f"Calculadora de sou net d'autònom {en}",
            "og_descripcion": f"El que li queda al mes a un autònom {en} després de despeses, quota i IRPF.",
            "h1": f"Sou net d'un autònom {en}: calculadora 2026",
            "entradilla": f"Calcula el que et queda net cada mes {en} després de despeses, quota d'autònoms i IRPF, amb les taules oficials del 2026, i compara-ho amb les altres comunitats.",
        })
    p["clave"] = clave("sueldo", c)
    p["formulario"] = preseleccionar(p["formulario"], c)
    p["extra"] = extra_sueldo(lang, c)
    p["faq"] = faq_sueldo(lang, c)
    return p


# ---------------------------------------------------------------- Enlaces desde las páginas generales
def hub(lang, tipo, desde):
    titulo = {
        ("es", "irpf"): ("IRPF de autónomos en cada comunidad", "Escala, tipos marginales, mínimos y ejemplos de cada comunidad, con la calculadora ya preparada."),
        ("ca", "irpf"): ("IRPF d'autònoms a cada comunitat", "Escala, tipus marginals, mínims i exemples de cada comunitat, amb la calculadora ja preparada."),
        ("es", "sueldo"): ("Sueldo neto de autónomo en cada comunidad", "Ejemplos de lo que le queda a un autónomo en cada comunidad, con la calculadora ya preparada."),
        ("ca", "sueldo"): ("Sou net d'autònom a cada comunitat", "Exemples del que li queda a un autònom a cada comunitat, amb la calculadora ja preparada."),
    }[(lang, tipo)]
    return f"""<section class="tarjeta">
    <h2>{titulo[0]}</h2>
    <p>{titulo[1]}</p>
    {lista_comunidades(lang, tipo, desde)}
  </section>

  """


def con_hub(p, tipo):
    p = copy.deepcopy(p)
    p["extra"] = hub(p["lang"], tipo, BASES[tipo][p["lang"]])
    return p


TARIFA_EN_SUELDO = {
    "es": ("¿Qué no incluye?",
           'Otras rentas como un sueldo o alquileres, el mínimo por hijos, las deducciones y la tributación conjunta. Si tienes la tarifa plana, escribe 88,64 € en el campo de la cuota: en la <a href="../tarifa-plana-autonomos-2026/">calculadora de la tarifa plana</a> verás cuánto te ahorras.'),
    "ca": ("Què no inclou?",
           'Altres rendes com un sou o lloguers, el mínim per fills, les deduccions i la tributació conjunta. Si tens la tarifa plana, escriu 88,64 € al camp de la quota: a la <a href="../tarifa-plana-autonoms-2026/">calculadora de la tarifa plana</a> veuràs quant t\'estalvies.'),
}


def sueldo_general(p):
    p = con_hub(p, "sueldo")
    pregunta = "¿Qué no incluye?" if p["lang"] == "es" else "Què no inclou?"
    if pregunta not in [q for q, _ in p["faq"]]:
        raise SystemExit(f"No se encontró la pregunta «{pregunta}» en el sueldo neto")
    p["faq"] = reemplazar_faq(p["faq"], {pregunta: TARIFA_EN_SUELDO[p["lang"]]})
    return p


sustitutos = {
    ("es", "irpf_es"): con_hub(IRPF_ES, "irpf"),
    ("ca", "irpf_es"): con_hub(IRPF_CA, "irpf"),
    ("es", "sueldo"): sueldo_general(SUELDO_ES),
    ("ca", "sueldo"): sueldo_general(SUELDO_CA),
}
PAGINAS_COMUNIDADES = []
for c in ORDEN_COMUNIDADES:
    for lang in ("es", "ca"):
        if c != "cataluna":
            PAGINAS_COMUNIDADES.append(pagina_irpf(lang, c))
        PAGINAS_COMUNIDADES.append(pagina_sueldo(lang, c))

PAGINAS = [sustitutos.get((p["lang"], p["clave"]), p) for p in PAGINAS_ANTERIORES] + PAGINAS_COMUNIDADES
