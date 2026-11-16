"""Genera las páginas de la web de calculadoras y actualiza las partes comunes de las existentes.

Uso, desde la carpeta de la web: python -I herramientas/generar.py .
"""
import html
import json
import posixpath
import re
import sys
from pathlib import Path

WEB = Path(sys.argv[1])
BASE = "https://juli2006farres.github.io/calculadora-irpf-autonomos-cataluna/"
MCPIZE = "https://mcpize.com/mcp/irpf-pymes-cat-mcp"
HOY = "2026-11-17"

RUTAS = {
    "irpf": {"es": "", "ca": "ca/"},
    "cuota": {"es": "cuota-autonomos-2026/", "ca": "ca/quota-autonoms-2026/"},
    "factura": {"es": "factura-autonomos/", "ca": "ca/factura-autonoms/"},
    "iva": {"es": "calculadora-iva/", "ca": "ca/calculadora-iva/"},
    "sueldo": {"es": "sueldo-neto-autonomo/", "ca": "ca/sou-net-autonom/"},
    "objetivo": {"es": "cuanto-facturar-autonomo/", "ca": "ca/quant-facturar-autonom/"},
    "m130": {"es": "modelo-130/", "ca": "ca/model-130/"},
}
ORDEN = ["irpf", "cuota", "factura", "iva", "sueldo", "objetivo", "m130"]
MENU = {
    "es": {"irpf": "IRPF", "cuota": "Cuota", "factura": "Factura", "iva": "IVA", "sueldo": "Sueldo neto",
           "objetivo": "Cuánto facturar", "m130": "Modelo 130"},
    "ca": {"irpf": "IRPF", "cuota": "Quota", "factura": "Factura", "iva": "IVA", "sueldo": "Sou net",
           "objetivo": "Quant facturar", "m130": "Model 130"},
}
TARJETAS = {
    "es": {
        "irpf": ("IRPF de autónomos en Cataluña", "Cuánto pagarás en la renta, con la escala catalana."),
        "cuota": ("Cuota de autónomos 2026", "Tu tramo y tu cuota mensual según lo que ganas."),
        "factura": ("Factura con IVA e IRPF", "El total de la factura, o cuánto facturar para cobrar una cantidad."),
        "iva": ("Calculadora de IVA", "Añade o quita el IVA del 21 %, 10 % o 4 % a cualquier precio."),
        "sueldo": ("Sueldo neto de autónomo", "Lo que te queda al mes tras gastos, cuota e IRPF."),
        "objetivo": ("Cuánto facturar", "La facturación y el precio por hora para ganar el neto que quieres."),
        "m130": ("Modelo 130", "Tus pagos trimestrales del IRPF, trimestre a trimestre."),
    },
    "ca": {
        "irpf": ("IRPF d'autònoms a Catalunya", "Quant pagaràs a la renda, amb l'escala catalana."),
        "cuota": ("Quota d'autònoms 2026", "El teu tram i la teva quota mensual segons el que guanyes."),
        "factura": ("Factura amb IVA i IRPF", "El total de la factura, o quant facturar per cobrar una quantitat."),
        "iva": ("Calculadora d'IVA", "Afegeix o treu l'IVA del 21 %, 10 % o 4 % a qualsevol preu."),
        "sueldo": ("Sou net d'autònom", "El que et queda al mes després de despeses, quota i IRPF."),
        "objetivo": ("Quant facturar", "La facturació i el preu per hora per guanyar el net que vols."),
        "m130": ("Model 130", "Els teus pagaments trimestrals de l'IRPF, trimestre a trimestre."),
    },
}
# Fecha de la última revisión de los datos de cada calculadora y a qué año se refieren.
REVISION = {
    "irpf": ("2026-11-04", {"es": "datos de 2025 y 2026", "ca": "dades del 2025 i el 2026"}),
    "cuota": ("2026-11-16", {"es": "tablas oficiales de 2026", "ca": "taules oficials del 2026"}),
    "factura": (HOY, {"es": "tipos vigentes en 2026", "ca": "tipus vigents el 2026"}),
    "iva": (HOY, {"es": "tipos vigentes en 2026", "ca": "tipus vigents el 2026"}),
    "sueldo": (HOY, {"es": "datos de 2026", "ca": "dades del 2026"}),
    "objetivo": (HOY, {"es": "datos de 2026", "ca": "dades del 2026"}),
    "m130": (HOY, {"es": "normativa vigente en 2026", "ca": "normativa vigent el 2026"}),
}
MESES = {
    "es": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"],
    "ca": ["gener", "febrer", "març", "abril", "maig", "juny", "juliol", "agost", "setembre", "octubre", "novembre", "desembre"],
}
T = {
    "es": {
        "marca": "Calculadoras para autónomos",
        "otro_idioma": "Català",
        "chips": ["Gratis", "Sin registro", "Sin cookies", "Datos oficiales"],
        "revisado": "Revisado el {fecha} · {datos}",
        "mas": "Más calculadoras para autónomos",
        "pie": "Calculadoras independientes, sin relación con la Agencia Tributaria, la Seguridad Social ni la Generalitat de Catalunya. Los cálculos se hacen en tu navegador y no se guarda nada.",
        "mcp": "¿Usas un asistente de IA? Estos cálculos también están en un <a href=\"" + MCPIZE + "\">servidor MCP con plan gratuito</a>.",
        "ia_titulo": "¿Usas Claude, ChatGPT o Cursor?",
        "ia_texto": "Estos cálculos están disponibles como servidor MCP, para que tu asistente de IA los haga dentro de la conversación. Tiene un plan gratuito de 50 consultas al mes.",
        "ia_boton": "Probarlo gratis en MCPize",
        "faq": "Preguntas frecuentes",
        "resultado": "Resultado",
        "rellena": "Rellena tus datos para ver el cálculo.",
        "aviso": "Aviso:",
        "os": "Cualquiera",
        "locale": "es_ES",
    },
    "ca": {
        "marca": "Calculadores per a autònoms",
        "otro_idioma": "Castellano",
        "chips": ["Gratuït", "Sense registre", "Sense galetes", "Dades oficials"],
        "revisado": "Revisat el {fecha} · {datos}",
        "mas": "Més calculadores per a autònoms",
        "pie": "Calculadores independents, sense relació amb l'Agència Tributària, la Seguretat Social ni la Generalitat de Catalunya. Els càlculs es fan al teu navegador i no es desa res.",
        "mcp": "Fas servir un assistent d'IA? Aquests càlculs també són en un <a href=\"" + MCPIZE + "\">servidor MCP amb pla gratuït</a>.",
        "ia_titulo": "Fas servir Claude, ChatGPT o Cursor?",
        "ia_texto": "Aquests càlculs estan disponibles com a servidor MCP, perquè el teu assistent d'IA els faci dins de la conversa. Té un pla gratuït de 50 consultes al mes. La pàgina del servei està en anglès i el servei respon en castellà.",
        "ia_boton": "Prova'l gratis a MCPize",
        "faq": "Preguntes freqüents",
        "resultado": "Resultat",
        "rellena": "Omple les teves dades per veure el càlcul.",
        "aviso": "Avís:",
        "os": "Qualsevol",
        "locale": "ca_ES",
    },
}
# Descripciones de las páginas que no se generan desde contenido.py (máximo 155 caracteres).
DESCRIPCIONES = {
    ("es", "irpf"): "Calcula gratis el IRPF de un autónomo en Cataluña en 2025 y 2026, con la escala catalana, la reducción por inicio de actividad y el mínimo por hijos.",
    ("ca", "irpf"): "Calcula gratis l'IRPF d'un autònom a Catalunya el 2025 i el 2026, amb l'escala catalana, la reducció per inici d'activitat i el mínim per fills.",
    ("es", "cuota"): "Calcula gratis tu cuota de autónomos 2026: tramo, base mínima y cuota mensual según tus rendimientos, con las tablas oficiales del BOE. Toda España.",
    ("ca", "cuota"): "Calcula gratis la teva quota d'autònoms 2026: tram, base mínima i quota mensual segons els teus rendiments, amb les taules oficials del BOE.",
}
ICONO = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%231f5f8b'/%3E%3Ctext x='16' y='22' font-size='16' text-anchor='middle' fill='white' font-family='Arial'%3E%E2%82%AC%3C/text%3E%3C/svg%3E"


def fecha_texto(iso, lang):
    anio, mes, dia = (int(x) for x in iso.split("-"))
    nombre = MESES[lang][mes - 1]
    de = "d'" if lang == "ca" and nombre[0] in "aeiou" else "de "
    return f"{dia} {de}{nombre} de {anio}"


def relativa(desde, hasta):
    """Enlace relativo de la página `desde` a la página `hasta` (carpetas con barra final)."""
    r = posixpath.relpath(hasta.rstrip("/") or ".", desde.rstrip("/") or ".")
    return "./" if r == "." else r + "/"


def otro(lang):
    return "ca" if lang == "es" else "es"


def cabecera(lang, clave):
    ruta = RUTAS[clave][lang]
    enlaces = []
    for k in ORDEN:
        actual = ' aria-current="page"' if k == clave else ""
        enlaces.append(f'<a href="{relativa(ruta, RUTAS[k][lang])}"{actual}>{MENU[lang][k]}</a>')
    o = otro(lang)
    enlaces.append(
        f'<a class="idioma" href="{relativa(ruta, RUTAS[clave][o])}" hreflang="{o}" lang="{o}">{T[lang]["otro_idioma"]}</a>'
    )
    menu = "\n      ".join(enlaces)
    return f"""<header class="cabecera">
  <div class="contenedor">
    <a class="marca" href="{relativa(ruta, RUTAS["irpf"][lang])}"><span class="logo" aria-hidden="true">€</span>{T[lang]["marca"]}</a>
    <nav class="menu" aria-label="{T[lang]["marca"]}">
      {menu}
    </nav>
  </div>
</header>"""


def linea_revision(lang, clave):
    iso, datos = REVISION[clave]
    texto = T[lang]["revisado"].format(fecha=fecha_texto(iso, lang), datos=datos[lang])
    return f'<p class="actualizado"><time datetime="{iso}">{texto}</time></p>'


def heroe(lang, clave, h1, entradilla):
    chips = "".join(f"<li>{c}</li>" for c in T[lang]["chips"])
    return f"""<section class="heroe">
  <div class="contenedor">
    {h1}
    {entradilla}
    <ul class="chips">{chips}</ul>
    {linea_revision(lang, clave)}
  </div>
</section>"""


def mas_calculadoras(lang, clave):
    ruta = RUTAS[clave][lang]
    items = []
    for k in ORDEN:
        if k == clave:
            continue
        titulo, texto = TARJETAS[lang][k]
        items.append(f'<li><a href="{relativa(ruta, RUTAS[k][lang])}"><strong>{titulo}</strong><span>{texto}</span></a></li>')
    lista = "\n      ".join(items)
    return f"""<section class="tarjeta">
    <h2>{T[lang]["mas"]}</h2>
    <ul class="otras">
      {lista}
    </ul>
  </section>"""


def pie(lang):
    return f"""<footer class="pie">
  <div class="contenedor">
    <p>{T[lang]["pie"]}</p>
    <p>{T[lang]["mcp"]}</p>
  </div>
</footer>"""


def hreflang(clave):
    es, ca = BASE + RUTAS[clave]["es"], BASE + RUTAS[clave]["ca"]
    return (
        f'<link rel="alternate" hreflang="es" href="{es}">\n'
        f'  <link rel="alternate" hreflang="ca" href="{ca}">\n'
        f'  <link rel="alternate" hreflang="x-default" href="{es}">'
    )


def texto_plano(fragmento):
    return html.unescape(re.sub(r"<[^>]+>", "", fragmento))


def pagina(p):
    lang, clave = p["lang"], p["clave"]
    if len(p["descripcion"]) > 155:
        raise SystemExit(f"Descripción demasiado larga ({len(p['descripcion'])}) en {lang}/{clave}")
    ruta = RUTAS[clave][lang]
    url = BASE + ruta
    raiz = "../" * ruta.count("/")
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebApplication",
                "name": p["og_titulo"],
                "url": url,
                "applicationCategory": "FinanceApplication",
                "operatingSystem": T[lang]["os"],
                "inLanguage": lang,
                "dateModified": REVISION[clave][0],
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": texto_plano(a)}}
                    for q, a in p["faq"]
                ],
            },
        ],
    }
    faq = "\n".join(f"    <h3>{q}</h3>\n    <p>{a}</p>" for q, a in p["faq"])
    fuentes = "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in p["fuentes"])
    ld_texto = json.dumps(ld, ensure_ascii=False, indent=2).replace("\n", "\n  ")
    clase = "calculadora apilada" if p.get("apilada") else "calculadora"
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{p["titulo"]}</title>
  <meta name="description" content="{html.escape(p["descripcion"])}">
  <link rel="canonical" href="{url}">
  {hreflang(clave)}
  <meta property="og:type" content="website">
  <meta property="og:title" content="{html.escape(p["og_titulo"])}">
  <meta property="og:description" content="{html.escape(p["og_descripcion"])}">
  <meta property="og:url" content="{url}">
  <meta property="og:locale" content="{T[lang]["locale"]}">
  <link rel="icon" href="{ICONO}">
  <script type="application/ld+json">
  {ld_texto}
  </script>
  <link rel="stylesheet" href="{raiz}estilos.css">
</head>
<body>
{cabecera(lang, clave)}
{heroe(lang, clave, "<h1>" + p["h1"] + "</h1>", '<p class="entradilla">' + p["entradilla"] + "</p>")}
<main>
<div class="contenedor">
  <div class="{clase}">
  <form id="formulario" class="tarjeta" novalidate>
{p["formulario"]}
  </form>

  <section class="tarjeta resultado" aria-live="polite">
    <h2>{T[lang]["resultado"]}</h2>
    <div id="resultado"><p>{T[lang]["rellena"]}</p></div>
  </section>
  </div>

  <section class="tarjeta faq">
    <h2>{T[lang]["faq"]}</h2>
{faq}
  </section>

  <section class="tarjeta ia">
    <h2>{T[lang]["ia_titulo"]}</h2>
    <p>{T[lang]["ia_texto"]}</p>
    <a class="boton" href="{MCPIZE}">{T[lang]["ia_boton"]}</a>
  </section>

  {mas_calculadoras(lang, clave)}

  <div class="aviso">
    <strong>{T[lang]["aviso"]}</strong> {p["aviso"]}
    <ul>{fuentes}</ul>
  </div>
</div>
</main>
{pie(lang)}
<script type="module" src="{raiz}{p["script"]}"></script>
</body>
</html>
"""


def sustituir(texto, patron, nuevo, archivo):
    resultado, n = re.subn(patron, lambda _: nuevo, texto, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f"No se encontró {patron!r} en {archivo}")
    return resultado


def actualizar_existente(lang, clave):
    """Actualiza menú, revisión, descripción y tarjetas de las páginas de IRPF y cuota, que no se generan."""
    archivo = WEB / RUTAS[clave][lang] / "index.html"
    t = archivo.read_text(encoding="utf-8")
    t = sustituir(t, r'<header class="cabecera">.*?</header>', cabecera(lang, clave), archivo)
    t = sustituir(t, r'<section class="tarjeta">\s*<h2>(?:Más|Més) calculador(?:as|es).*?</section>', mas_calculadoras(lang, clave), archivo)
    t = re.sub(r'\n    <p class="actualizado">.*?</p>', "", t)
    if '<ul class="chips">' not in t:
        raise SystemExit(f"No se encontraron las etiquetas de la portada en {archivo}")
    t = re.sub(r'(<ul class="chips">.*?</ul>)', lambda m: m.group(1) + "\n    " + linea_revision(lang, clave), t, count=1, flags=re.S)
    t = sustituir(t, r'<meta name="description" content=".*?">', f'<meta name="description" content="{html.escape(DESCRIPCIONES[(lang, clave)])}">', archivo)
    fecha = fecha_texto(REVISION[clave][0], lang)
    t = re.sub(r'<span id="fecha-revision">[^<]*</span>', f'<span id="fecha-revision">{fecha}</span>', t)
    t = t.replace(
        '"offers": { "@type": "Offer"',
        f'"dateModified": "{REVISION[clave][0]}",\n        "offers": {{ "@type": "Offer"',
        1,
    ) if '"dateModified"' not in t else t
    archivo.write_text(t, encoding="utf-8")


def sitemap():
    lineas = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for clave in ORDEN:
        es, ca = RUTAS[clave]["es"], RUTAS[clave]["ca"]
        for ruta in (es, ca):
            lineas += [
                "  <url>",
                f"    <loc>{BASE}{ruta}</loc>",
                f"    <lastmod>{HOY}</lastmod>",
                f'    <xhtml:link rel="alternate" hreflang="es" href="{BASE}{es}"/>',
                f'    <xhtml:link rel="alternate" hreflang="ca" href="{BASE}{ca}"/>',
                f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{es}"/>',
                "  </url>",
            ]
    lineas.append("</urlset>")
    (WEB / "sitemap.xml").write_text("\n".join(lineas) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))
    from contenido_extra import PAGINAS

    for (lang, clave), d in DESCRIPCIONES.items():
        if len(d) > 155:
            raise SystemExit(f"Descripción demasiado larga ({len(d)}) en {lang}/{clave}")
    for lang in ("es", "ca"):
        for clave in ("irpf", "cuota"):
            actualizar_existente(lang, clave)
    for p in PAGINAS:
        destino = WEB / RUTAS[p["clave"]][p["lang"]] / "index.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(pagina(p), encoding="utf-8")
        print("escrita", destino)
    sitemap()
