"""Genera las páginas de la web de calculadoras y actualiza las partes comunes de las existentes.

Uso, desde la carpeta de la web: python -I herramientas/generar.py .
"""
import hashlib
import html
import json
import posixpath
import re
import sys
from pathlib import Path

WEB = Path(sys.argv[1])
BASE = "https://calculadorasautonomos.es/"
MCPIZE = "https://mcpize.com/mcp/irpf-pymes-cat-mcp"
HOY = "2026-11-17"
# Fecha de la última modificación de las páginas, para el sitemap.
MODIFICADO = "2026-11-27"

RUTAS = {
    "irpf": {"es": "", "ca": "ca/"},
    "cuota": {"es": "cuota-autonomos-2026/", "ca": "ca/quota-autonoms-2026/"},
    "tarifa": {"es": "tarifa-plana-autonomos-2026/", "ca": "ca/tarifa-plana-autonoms-2026/"},
    "regularizacion": {"es": "regularizacion-cuota-autonomos-2026/", "ca": "ca/regularitzacio-quota-autonoms-2026/"},
    "insertar": {"es": "insertar/", "ca": "ca/inserir/"},
    "factura": {"es": "factura-autonomos/", "ca": "ca/factura-autonoms/"},
    "iva": {"es": "calculadora-iva/", "ca": "ca/calculadora-iva/"},
    "sueldo": {"es": "sueldo-neto-autonomo/", "ca": "ca/sou-net-autonom/"},
    "objetivo": {"es": "cuanto-facturar-autonomo/", "ca": "ca/quant-facturar-autonom/"},
    "m130": {"es": "modelo-130/", "ca": "ca/model-130/"},
    "m303": {"es": "modelo-303/", "ca": "ca/model-303/"},
    "m130_2027": {"es": "modelo-130-2027/", "ca": "ca/model-130-2027/"},
    "iva_anual": {"es": "iva-anual-autonomos-2027/", "ca": "ca/iva-anual-autonoms-2027/"},
    "plantilla": {"es": "plantilla-factura-autonomo/", "ca": "ca/plantilla-factura-autonom/"},
    "transparencia": {"es": "transparencia/", "ca": "ca/transparencia/"},
    "irpf_es": {"es": "calculadora-irpf-autonomos/", "ca": "ca/calculadora-irpf-autonoms/"},
    "calendario": {"es": "calendario-fiscal-autonomos-2027/", "ca": "ca/calendari-fiscal-autonoms-2027/"},
}
# ORDEN: tarjetas y sitemap. MENU_ORDEN: menú de arriba (el IRPF de Cataluña se enlaza desde las tarjetas).
ORDEN = ["irpf_es", "irpf", "cuota", "tarifa", "regularizacion", "factura", "plantilla", "iva", "m303", "iva_anual", "m130", "m130_2027", "sueldo", "objetivo", "calendario"]
MENU_ORDEN = ["irpf_es", "cuota", "factura", "plantilla", "iva", "m303", "m130", "sueldo", "objetivo", "calendario"]
MENU = {
    "es": {"irpf_es": "IRPF", "calendario": "Calendario", "irpf": "IRPF Cataluña", "cuota": "Cuota", "tarifa": "Tarifa plana", "regularizacion": "Regularización", "factura": "Factura", "iva": "IVA", "sueldo": "Sueldo neto",
           "objetivo": "Cuánto facturar", "m130": "Modelo 130", "m303": "Modelo 303", "plantilla": "Plantilla",
           "m130_2027": "Modelo 130 en 2027", "iva_anual": "IVA anual"},
    "ca": {"irpf_es": "IRPF", "calendario": "Calendari", "irpf": "IRPF Catalunya", "cuota": "Quota", "tarifa": "Tarifa plana", "regularizacion": "Regularització", "factura": "Factura", "iva": "IVA", "sueldo": "Sou net",
           "objetivo": "Quant facturar", "m130": "Model 130", "m303": "Model 303", "plantilla": "Plantilla",
           "m130_2027": "Model 130 el 2027", "iva_anual": "IVA anual"},
}
TARJETAS = {
    "es": {
        "irpf_es": ("IRPF por comunidad autónoma", "Tu IRPF en tu comunidad y cuánto pagarías en las demás."),
        "calendario": ("Calendario fiscal 2027", "Todos los plazos del año: modelos 303, 130, 390 y renta."),
        "irpf": ("IRPF de autónomos en Cataluña", "Cuánto pagarás en la renta, con la escala catalana."),
        "cuota": ("Cuota de autónomos 2026", "Tu tramo y tu cuota mensual según lo que ganas."),
        "tarifa": ("Tarifa plana 2026", "Cuánto te ahorras el primer año y si puedes alargarla."),
        "regularizacion": ("Regularización de la cuota", "Si la Seguridad Social te devolverá o te cobrará la diferencia de 2026."),
        "factura": ("Factura con IVA e IRPF", "El total de la factura, o cuánto facturar para cobrar una cantidad."),
        "iva": ("Calculadora de IVA", "Añade o quita el IVA del 21 %, 10 % o 4 % a cualquier precio."),
        "sueldo": ("Sueldo neto de autónomo", "Lo que te queda al mes tras gastos, cuota e IRPF."),
        "objetivo": ("Cuánto facturar", "La facturación y el precio por hora para ganar el neto que quieres."),
        "m130": ("Modelo 130", "Tus pagos trimestrales del IRPF, trimestre a trimestre."),
        "m303": ("Modelo 303", "El IVA de cada trimestre: lo que cobras menos lo que pagas."),
        "m130_2027": ("Modelo 130 en 2027", "Si te libras del 130, si pagas el 19 % y el pago domiciliado."),
        "iva_anual": ("IVA anual en 2027", "Si puedes cambiar los cuatro 303 por una declaración al año."),
        "plantilla": ("Plantilla de factura", "Excel y Word gratis, con el IVA y la retención calculados."),
    },
    "ca": {
        "irpf_es": ("IRPF per comunitat autònoma", "El teu IRPF a la teva comunitat i quant pagaries a les altres."),
        "calendario": ("Calendari fiscal 2027", "Tots els terminis de l'any: models 303, 130, 390 i renda."),
        "irpf": ("IRPF d'autònoms a Catalunya", "Quant pagaràs a la renda, amb l'escala catalana."),
        "cuota": ("Quota d'autònoms 2026", "El teu tram i la teva quota mensual segons el que guanyes."),
        "tarifa": ("Tarifa plana 2026", "Quant t'estalvies el primer any i si la pots allargar."),
        "regularizacion": ("Regularització de la quota", "Si la Seguretat Social et retornarà o et cobrarà la diferència del 2026."),
        "factura": ("Factura amb IVA i IRPF", "El total de la factura, o quant facturar per cobrar una quantitat."),
        "iva": ("Calculadora d'IVA", "Afegeix o treu l'IVA del 21 %, 10 % o 4 % a qualsevol preu."),
        "sueldo": ("Sou net d'autònom", "El que et queda al mes després de despeses, quota i IRPF."),
        "objetivo": ("Quant facturar", "La facturació i el preu per hora per guanyar el net que vols."),
        "m130": ("Model 130", "Els teus pagaments trimestrals de l'IRPF, trimestre a trimestre."),
        "m303": ("Model 303", "L'IVA de cada trimestre: el que cobres menys el que pagues."),
        "m130_2027": ("Model 130 el 2027", "Si et lliures del 130, si pagues el 19 % i el pagament domiciliat."),
        "iva_anual": ("IVA anual el 2027", "Si pots canviar els quatre 303 per una declaració a l'any."),
        "plantilla": ("Plantilla de factura", "Excel i Word gratis, amb l'IVA i la retenció calculats."),
    },
}
TRAZOS = {
    "irpf_es": '<path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2-6-2z"/><path d="M9 4v14M15 6v14"/>',
    "irpf": '<path d="M4 20V11M10 20V5M16 20v-6M2 20h20"/>',
    "cuota": '<path d="M3 10h18L12 4 3 10z"/><path d="M5.5 10v8M10 10v8M14 10v8M18.5 10v8M3 20h18"/>',
    "tarifa": '<path d="M12 21v-9"/><path d="M12 12C12 7.5 8.5 5 4 5c0 4.5 3.5 7 8 7z"/><path d="M12 14.5c0-4 3-6.5 8-6.5 0 4-3 6.5-8 6.5z"/>',
    "insertar": '<path d="m8 8-4 4 4 4M16 8l4 4-4 4M14 5l-4 14"/>',
    "regularizacion": '<path d="M20 11a8 8 0 0 0-14.3-4.9L4 8"/><path d="M4 3v5h5"/><path d="M4 13a8 8 0 0 0 14.3 4.9L20 16"/><path d="M20 21v-5h-5"/>',
    "factura": '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2V3z"/><path d="M9 8h6M9 12h6M9 16h3"/>',
    "plantilla": '<path d="M7 3h7l5 5v13H7V3z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>',
    "iva": '<path d="M19 5 5 19"/><circle cx="7" cy="7" r="2.5"/><circle cx="17" cy="17" r="2.5"/>',
    "m303": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 11h.01M12 11h.01M16 11h.01M8 15h.01M12 15h.01M8 18h.01M12 18h.01M16 15v3"/>',
    "m130": '<rect x="4" y="5" width="16" height="16" rx="2"/><path d="M4 10h16M8 3v4M16 3v4M9 15.5l2 2 4-4"/>',
    "sueldo": '<path d="M4 7h14a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a1 1 0 0 1-1-1V7z"/><path d="M4 7l11-3v3M16 13.5h.01"/>',
    "objetivo": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><path d="M12 12h.01"/>',
    "calendario": '<rect x="4" y="5" width="16" height="16" rx="2"/><path d="M4 10h16M8 3v4M16 3v4M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01"/>',
    "m130_2027": '<rect x="4" y="5" width="16" height="16" rx="2"/><path d="M4 10h16M8 3v4M16 3v4M9 17l6-5M9.5 13h.01M14.5 16.5h.01"/>',
    "iva_anual": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7v5l3.5 2"/>',
}
ICONOS = {
    k: f'<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">{v}</svg>'
    for k, v in TRAZOS.items()
}
# Fecha de la última revisión de los datos de cada calculadora y a qué año se refieren.
REVISION = {
    "irpf": ("2026-11-25", {"es": "datos de 2025 y 2026", "ca": "dades del 2025 i el 2026"}),
    "cuota": ("2026-11-25", {"es": "tablas oficiales de 2026", "ca": "taules oficials del 2026"}),
    "tarifa": ("2026-11-25", {"es": "datos de 2026", "ca": "dades del 2026"}),
    "regularizacion": ("2026-11-25", {"es": "normativa y tablas de 2026", "ca": "normativa i taules del 2026"}),
    "insertar": ("2026-11-25", {"es": "datos de 2026", "ca": "dades del 2026"}),
    "factura": (HOY, {"es": "tipos vigentes en 2026", "ca": "tipus vigents el 2026"}),
    "iva": (HOY, {"es": "tipos vigentes en 2026", "ca": "tipus vigents el 2026"}),
    "sueldo": ("2026-11-25", {"es": "datos de 2026", "ca": "dades del 2026"}),
    "objetivo": ("2026-11-25", {"es": "datos de 2026", "ca": "dades del 2026"}),
    "m130": ("2026-11-25", {"es": "normativa vigente en 2026", "ca": "normativa vigent el 2026"}),
    "m303": ("2026-11-18", {"es": "normativa vigente en 2026", "ca": "normativa vigent el 2026"}),
    "plantilla": ("2026-11-25", {"es": "requisitos vigentes en 2026", "ca": "requisits vigents el 2026"}),
    "irpf_es": ("2026-11-25", {"es": "datos de 2025 y 2026", "ca": "dades del 2025 i el 2026"}),
    "calendario": ("2026-11-25", {"es": "plazos de 2027", "ca": "terminis del 2027"}),
    "m130_2027": ("2026-11-27", {"es": "Real Decreto-ley 43/2026", "ca": "Reial decret llei 43/2026"}),
    "iva_anual": ("2026-11-27", {"es": "Real Decreto-ley 43/2026", "ca": "Reial decret llei 43/2026"}),
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
        "mcp": "¿Usas un asistente de IA? Las principales calculadoras también están en un <a href=\"" + MCPIZE + "\">servidor MCP con plan gratuito</a>.",
        "ia_titulo": "¿Usas Claude, ChatGPT o Cursor?",
        "ia_texto": "Las calculadoras de IRPF, cuota de autónomos, factura y modelos 130 y 303 están disponibles como servidor MCP, para que tu asistente de IA haga esos cálculos dentro de la conversación. Tiene un plan gratuito de 50 consultas al mes.",
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
        "mcp": "Fas servir un assistent d'IA? Les principals calculadores també són en un <a href=\"" + MCPIZE + "\">servidor MCP amb pla gratuït</a>.",
        "ia_titulo": "Fas servir Claude, ChatGPT o Cursor?",
        "ia_texto": "Les calculadores d'IRPF, quota d'autònoms, factura i models 130 i 303 estan disponibles com a servidor MCP, perquè el teu assistent d'IA faci aquests càlculs dins de la conversa. Té un pla gratuït de 50 consultes al mes. La pàgina del servei està en anglès i el servei respon en castellà.",
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
# Versión de la hoja de estilos: cambia sola cuando cambia estilos.css, para que los navegadores
# no sigan usando una copia antigua guardada en caché.
VERSION_CSS = hashlib.sha256((WEB / "estilos.css").read_bytes()).hexdigest()[:10]
# Contador de visitas sin cookies (GoatCounter). Versión fija con su huella (SRI): el navegador solo
# ejecuta exactamente este archivo. No cuenta en las calculadoras para otras webs ni en localhost, y
# solo envía la dirección sin la parte de «#», así que los datos de las calculadoras no salen del navegador.
CONTADOR = ('<script data-goatcounter="https://calculadoras-autonomos.goatcounter.com/count" async '
            'src="https://gc.zgo.at/count.v5.js" crossorigin="anonymous" '
            'integrity="sha384-atnOLvQb9t+jTSipvd75X2yginT4PjVbqDdlJAmxMm+wYElFmeR6EmLP5bYeoRVQ"></script>')
# Página de la que cuelga cada página de comunidad, para marcarla en el menú.
PADRE = {}
ICONO = "/favicon.svg"  # también /favicon.ico en la raíz, para Google y navegadores antiguos


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
    for k in MENU_ORDEN:
        actual = ' aria-current="page"' if k == PADRE.get(clave, clave) else ""
        enlaces.append(f'<a href="{relativa(ruta, RUTAS[k][lang])}"{actual}>{MENU[lang][k]}</a>')
    o = otro(lang)
    enlaces.append(
        f'<a class="idioma" href="{relativa(ruta, RUTAS[clave][o])}" hreflang="{o}" lang="{o}">{T[lang]["otro_idioma"]}</a>'
    )
    menu = "\n      ".join(enlaces)
    return f"""<header class="cabecera">
  <div class="contenedor">
    <a class="marca" href="{relativa(ruta, RUTAS["irpf"][lang])}" aria-label="{T[lang]["marca"]}"><span class="logo" aria-hidden="true">€</span><span class="marca-texto">{T[lang]["marca"]}</span></a>
    <nav class="menu" aria-label="{T[lang]["marca"]}">
      {menu}
    </nav>
  </div>
</header>"""


def linea_revision(lang, clave):
    iso, datos = REVISION[clave]
    texto = T[lang]["revisado"].format(fecha=fecha_texto(iso, lang), datos=datos[lang])
    return f'<p class="actualizado"><time datetime="{iso}">{texto}</time></p>'


INICIO = {"es": "Inicio", "ca": "Inici"}
ESTAS_AQUI = {"es": "Estás aquí", "ca": "Ets aquí"}
# Nombre de cada página de comunidad en las migas de pan («Madrid», «Galicia»...).
MIGA = {}


def pasos_migas(lang, clave):
    """Pasos de las migas de pan: [(nombre, ruta)]. La portada no lleva migas."""
    if clave == "irpf":
        return []
    pasos = [(INICIO[lang], RUTAS["irpf"][lang])]
    if clave in PADRE:
        padre = PADRE[clave]
        pasos.append((TARJETAS[lang][padre][0], RUTAS[padre][lang]))
        pasos.append((MIGA[(lang, clave)], RUTAS[clave][lang]))
    elif clave == "transparencia":
        pasos.append((TRANSPARENCIA[lang], RUTAS[clave][lang]))
    elif clave == "insertar":
        pasos.append((INSERTAR[lang]["titulo"], RUTAS[clave][lang]))
    else:
        pasos.append((TARJETAS[lang][clave][0], RUTAS[clave][lang]))
    return pasos


def migas(lang, clave):
    pasos = pasos_migas(lang, clave)
    if not pasos:
        return ""
    ruta = RUTAS[clave][lang]
    items = [f'<li><a href="{relativa(ruta, r)}">{html.escape(n, quote=False)}</a></li>' for n, r in pasos[:-1]]
    items.append(f'<li aria-current="page">{html.escape(pasos[-1][0], quote=False)}</li>')
    return f'<nav class="migas" aria-label="{ESTAS_AQUI[lang]}"><ol>{"".join(items)}</ol></nav>\n    '


def migas_ld(lang, clave):
    """Las mismas migas en datos estructurados (BreadcrumbList) para Google."""
    pasos = pasos_migas(lang, clave)
    if not pasos:
        return ""
    datos = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": n, "item": BASE + r} for i, (n, r) in enumerate(pasos, 1)
        ],
    }
    texto = json.dumps(datos, ensure_ascii=False, indent=2).replace("\n", "\n  ")
    return f'<script type="application/ld+json">\n  {texto}\n  </script>\n  '


def heroe(lang, clave, h1, entradilla):
    chips = "".join(f"<li>{c}</li>" for c in T[lang]["chips"])
    return f"""<section class="heroe">
  <div class="contenedor">
    {migas(lang, clave)}{h1}
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
        items.append(
            f'<li><a href="{relativa(ruta, RUTAS[k][lang])}"><span class="icono" aria-hidden="true">{ICONOS[k]}</span>'
            f'<div><strong>{titulo}</strong><span>{texto}</span></div></a></li>'
        )
    lista = "\n      ".join(items)
    return f"""<section class="tarjeta">
    <h2>{T[lang]["mas"]}</h2>
    <ul class="otras">
      {lista}
    </ul>
  </section>"""


TRANSPARENCIA = {"es": "Cómo se financia esta web", "ca": "Com es finança aquest web"}


GRUPOS_PIE = {
    "es": [("Impuestos", ["irpf_es", "irpf", "m303", "iva_anual", "m130", "m130_2027", "calendario"]),
           ("Cuota y sueldo", ["cuota", "tarifa", "regularizacion", "sueldo", "objetivo"]),
           ("Facturas", ["factura", "plantilla", "iva"])],
    "ca": [("Impostos", ["irpf_es", "irpf", "m303", "iva_anual", "m130", "m130_2027", "calendario"]),
           ("Quota i sou", ["cuota", "tarifa", "regularizacion", "sueldo", "objetivo"]),
           ("Factures", ["factura", "plantilla", "iva"])],
}
LEMA = {
    "es": "Calculadoras gratuitas para autónomos con datos oficiales del BOE, la Agencia Tributaria y la Seguridad Social. Sin registro y sin cookies.",
    "ca": "Calculadores gratuïtes per a autònoms amb dades oficials del BOE, l'Agència Tributària i la Seguretat Social. Sense registre i sense galetes.",
}


def pie(lang, clave):
    ruta = RUTAS[clave][lang]
    enlace = relativa(ruta, RUTAS["transparencia"][lang])
    columnas = []
    for titulo, claves in GRUPOS_PIE[lang]:
        enlaces = "".join(f'<li><a href="{relativa(ruta, RUTAS[k][lang])}">{TARJETAS[lang][k][0]}</a></li>' for k in claves)
        columnas.append(f'<div><h2>{titulo}</h2><ul>{enlaces}</ul></div>')
    return f"""<footer class="pie">
  <div class="contenedor">
    <div class="pie-columnas">
      <div class="pie-marca"><a class="marca" href="{relativa(ruta, RUTAS["irpf"][lang])}"><span class="logo" aria-hidden="true">€</span><span>{T[lang]["marca"]}</span></a><p>{LEMA[lang]}</p></div>
      {"".join(columnas)}
    </div>
    <div class="pie-legal">
      <p>{T[lang]["pie"]}</p>
      <p>{T[lang]["mcp"]}</p>
      <p><a href="{enlace}">{TRANSPARENCIA[lang]}</a> · <a href="{relativa(ruta, RUTAS["insertar"][lang])}">{INSERTAR[lang]["titulo"]}</a></p>
    </div>
  </div>
</footer>"""


# Enlace de afiliado de Quipu (programa de afiliados de Quipu, panel en quipu.getrewardful.com).
# Solo aparece en las calculadoras relacionadas con facturar e impuestos trimestrales.
AFILIADO_URL = {"es": "https://getquipu.com/es/autonomos?via=juli", "ca": "https://getquipu.com/ca/autonoms?via=juli"}
PAGINAS_CON_AFILIADO = {"factura", "iva", "m130", "m303", "plantilla", "calendario", "tarifa", "irpf", "irpf_es", "sueldo", "m130_2027", "iva_anual"}
# En las calculadoras de impuestos y sueldo el título habla de impuestos, no solo de facturas.
PAGINAS_IMPUESTOS = {"irpf", "irpf_es", "sueldo", "m130_2027", "iva_anual"}
TITULO_IMPUESTOS = {"es": "¿Quieres llevar las facturas y los impuestos al día?", "ca": "Vols portar les factures i els impostos al dia?"}
AFILIADO = {
    "es": {
        "titulo": "¿Todavía haces las facturas a mano?",
        "texto": "Quipu es un programa de facturación para autónomos: crea facturas adaptadas a Verifactu, guarda los gastos con una foto del ticket y prepara tus impuestos. Se puede empezar gratis.",
        "boton": "Ver Quipu",
        "nota": "Enlace de afiliado: si contratas Quipu desde aquí, esta web recibe una comisión y a ti no te cuesta más. Así estas calculadoras siguen siendo gratis.",
        "mas": "Más información",
    },
    "ca": {
        "titulo": "Encara fas les factures a mà?",
        "texto": "Quipu és un programa de facturació per a autònoms: crea factures adaptades a Verifactu, desa les despeses amb una foto del tiquet i prepara els teus impostos. Es pot començar gratis.",
        "boton": "Veure Quipu",
        "nota": "Enllaç d'afiliat: si contractes Quipu des d'aquí, aquest web rep una comissió i a tu no et costa més. Així aquestes calculadores continuen sent gratuïtes.",
        "mas": "Més informació",
    },
}


def recomendacion(lang, clave):
    tipo = PADRE.get(clave, clave)
    if tipo not in PAGINAS_CON_AFILIADO:
        return ""
    a = AFILIADO[lang]
    titulo = TITULO_IMPUESTOS[lang] if tipo in PAGINAS_IMPUESTOS else a["titulo"]
    enlace = relativa(RUTAS[clave][lang], RUTAS["transparencia"][lang])
    return f"""<section class="tarjeta patrocinio">
    <h2>{titulo}</h2>
    <p>{a["texto"]}</p>
    <a class="boton" href="{AFILIADO_URL[lang]}" rel="sponsored noopener" target="_blank">{a["boton"]}</a>
    <p class="nota">{a["nota"]} <a href="{enlace}">{a["mas"]}</a></p>
  </section>

  """


def pagina_transparencia(lang):
    ruta = RUTAS["transparencia"][lang]
    raiz = "../" * ruta.count("/")
    if lang == "es":
        titulo, h1 = "Cómo se financia esta web · Calculadoras para autónomos", "Cómo se financia esta web"
        entradilla = "Las calculadoras son gratuitas y seguirán siéndolo. Esto es lo que hay detrás."
        cuerpo = f"""    <h2>Sin cookies ni datos personales</h2>
    <p>Las calculadoras no tienen registro ni cookies. Los cálculos se hacen en tu navegador y no se guarda nada de lo que escribes.</p>
    <p>Para saber qué páginas se usan, contamos las visitas con <a href="https://www.goatcounter.com/help/privacy">GoatCounter</a>, un contador que no usa cookies y no guarda tu IP ni otros datos personales. Solo recoge la página que visitas, la web de la que vienes y, de forma agregada, el país, el navegador y el tamaño de la pantalla. Los datos que escribes en las calculadoras no se envían.</p>
    <h2>Enlaces de afiliado</h2>
    <p>Algunas calculadoras muestran un enlace a <strong>Quipu</strong>, un programa de facturación para autónomos. Es un enlace de afiliado: si te registras y contratas una suscripción desde él, esta web recibe una comisión de Quipu. A ti no te cuesta más.</p>
    <p>Esos enlaces llevan siempre la etiqueta «Enlace de afiliado». Las comisiones no cambian los cálculos ni los resultados, y esta web no tiene relación con Quipu más allá de su programa de afiliados.</p>
    <p>Al pulsar el enlace sales de esta web. Quipu y su plataforma de afiliados, Rewardful, usan sus propias cookies para saber que llegaste desde aquí. Consulta la <a href="https://getquipu.com/es/politica-de-privacidad">política de privacidad de Quipu</a>.</p>
    <h2>Servidor MCP</h2>
    <p>Los mismos cálculos están disponibles como <a href="{MCPIZE}">servidor MCP en MCPize</a> para asistentes de IA, con un plan gratuito y otro de pago.</p>"""
    else:
        titulo, h1 = "Com es finança aquest web · Calculadores per a autònoms", "Com es finança aquest web"
        entradilla = "Les calculadores són gratuïtes i ho continuaran sent. Això és el que hi ha al darrere."
        cuerpo = f"""    <h2>Sense galetes ni dades personals</h2>
    <p>Les calculadores no tenen registre ni galetes. Els càlculs es fan al teu navegador i no es desa res del que escrius.</p>
    <p>Per saber quines pàgines es fan servir, comptem les visites amb <a href="https://www.goatcounter.com/help/privacy">GoatCounter</a>, un comptador que no fa servir galetes i no desa la teva IP ni altres dades personals. Només recull la pàgina que visites, el web d'on vens i, de manera agregada, el país, el navegador i la mida de la pantalla. Les dades que escrius a les calculadores no s'envien.</p>
    <h2>Enllaços d'afiliat</h2>
    <p>Algunes calculadores mostren un enllaç a <strong>Quipu</strong>, un programa de facturació per a autònoms. És un enllaç d'afiliat: si et registres i contractes una subscripció des d'aquí, aquest web rep una comissió de Quipu. A tu no et costa més.</p>
    <p>Aquests enllaços porten sempre l'etiqueta «Enllaç d'afiliat». Les comissions no canvien els càlculs ni els resultats, i aquest web no té relació amb Quipu més enllà del seu programa d'afiliats.</p>
    <p>En prémer l'enllaç surts d'aquest web. Quipu i la seva plataforma d'afiliats, Rewardful, fan servir les seves pròpies galetes per saber que hi has arribat des d'aquí. Consulta la <a href="https://getquipu.com/es/politica-de-privacidad">política de privacitat de Quipu</a>.</p>
    <h2>Servidor MCP</h2>
    <p>Els mateixos càlculs estan disponibles com a <a href="{MCPIZE}">servidor MCP a MCPize</a> per a assistents d'IA, amb un pla gratuït i un altre de pagament.</p>"""
    es, ca = BASE + RUTAS["transparencia"]["es"], BASE + RUTAS["transparencia"]["ca"]
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{titulo}</title>
  <meta name="description" content="{html.escape(entradilla)}">
  <link rel="canonical" href="{BASE + ruta}">
  <link rel="alternate" hreflang="es" href="{es}">
  <link rel="alternate" hreflang="ca" href="{ca}">
  <link rel="alternate" hreflang="x-default" href="{es}">
  <link rel="icon" href="{ICONO}">
  {migas_ld(lang, "transparencia")}{CONTADOR}
  <link rel="stylesheet" href="{raiz}estilos.css?v={VERSION_CSS}">
</head>
<body>
{cabecera(lang, "transparencia")}
<section class="heroe">
  <div class="contenedor">
    {migas(lang, "transparencia")}<h1>{h1}</h1>
    <p class="entradilla">{entradilla}</p>
  </div>
</section>
<main>
<div class="contenedor">
  <section class="tarjeta faq">
{cuerpo}
  </section>

  {mas_calculadoras(lang, "transparencia")}
</div>
</main>
{pie(lang, "transparencia")}
</body>
</html>
"""


def meta_imagen(lang, clave, titulo):
    """Etiquetas de la imagen que se ve al compartir el enlace (la crea herramientas/imagenes.py)."""
    ruta = RUTAS[clave][lang]
    nombre = (ruta.strip("/").replace("/", "-") or "inicio") + ".jpg"
    if not (WEB / "compartir" / nombre).exists():
        return ""
    return (
        f'\n  <meta property="og:site_name" content="{T[lang]["marca"]}">'
        f'\n  <meta property="og:image" content="{BASE}compartir/{nombre}">'
        f'\n  <meta property="og:image:width" content="1200">'
        f'\n  <meta property="og:image:height" content="630">'
        f'\n  <meta property="og:image:alt" content="{html.escape(titulo)}">'
        f'\n  <meta name="twitter:card" content="summary_large_image">'
    )


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
    if p.get("cuerpo"):
        bloque = p["cuerpo"]
    else:
        bloque = f"""<div class="{clase}">
  <form id="formulario" class="tarjeta" novalidate>
{p["formulario"]}
  </form>

  <section class="tarjeta resultado" aria-live="polite">
    <h2>{T[lang]["resultado"]}</h2>
    <div id="resultado"><p>{T[lang]["rellena"]}</p></div>
  </section>
  </div>"""
    script = f'<script type="module" src="{raiz}{p["script"]}"></script>\n' if p.get("script") else ""
    # Botones de compartir e imprimir en las calculadoras (las páginas con «cuerpo» no tienen formulario).
    if p.get("script") and not p.get("cuerpo"):
        script += f'<script type="module" src="{raiz}compartir.js"></script>\n'
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
  <meta property="og:locale" content="{T[lang]["locale"]}">{meta_imagen(lang, clave, p["og_titulo"])}
  <link rel="icon" href="{ICONO}">
  <script type="application/ld+json">
  {ld_texto}
  </script>
  {migas_ld(lang, clave)}{CONTADOR}
  <link rel="stylesheet" href="{raiz}estilos.css?v={VERSION_CSS}">
</head>
<body>
{cabecera(lang, clave)}
{heroe(lang, clave, "<h1>" + p["h1"] + "</h1>", '<p class="entradilla">' + p["entradilla"] + "</p>")}
<main>
<div class="contenedor">
  {bloque}

  {recomendacion(lang, clave)}{p.get("extra", "")}<section class="tarjeta faq">
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
{pie(lang, clave)}
{script}</body>
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
    t = sustituir(t, r'<footer class="pie">.*?</footer>', pie(lang, clave), archivo)
    t = re.sub(r'\n  <meta (?:property="og:(?:site_name|image[^"]*)"|name="twitter:card") content="[^"]*">', "", t)
    titulo = re.search(r'<meta property="og:title" content="(.*?)">', t).group(1)
    t = sustituir(t, r'<meta property="og:locale" content="[^"]*">', re.search(r'<meta property="og:locale" content="[^"]*">', t).group(0) + meta_imagen(lang, clave, html.unescape(titulo)), archivo)
    t = re.sub(
        r'href="((?:\.\./)*)estilos\.css(?:\?v=\w+)?"',
        lambda m: f'href="{m.group(1)}estilos.css?v={VERSION_CSS}"',
        t,
    )
    # Contador de visitas: se quita el anterior y se pone el actual antes de la hoja de estilos.
    t = re.sub(r'<script data-goatcounter="[^"]*"[^>]*></script>\n  ', "", t)
    t, n = re.subn(r'(\n  )(<link rel="stylesheet")', lambda m: m.group(1) + CONTADOR + m.group(1) + m.group(2), t, count=1)
    if n != 1:
        raise SystemExit(f"No se pudo poner el contador en {archivo}")
    # Migas de pan (la portada no lleva): se quitan las anteriores y se vuelven a poner.
    t = re.sub(r'<nav class="migas".*?</nav>\n    ', "", t, flags=re.S)
    t = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema\.org",\s*"@type": "BreadcrumbList".*?</script>\n  ', "", t, flags=re.S)
    if pasos_migas(lang, clave):
        t, n = re.subn(r'(<section class="heroe">\s*<div class="contenedor">\s*)(<h1)', lambda m: m.group(1) + migas(lang, clave) + m.group(2), t, count=1)
        t, n2 = re.subn(r'(\n  )(<link rel="stylesheet")', lambda m: m.group(1) + migas_ld(lang, clave) + m.group(2), t, count=1)
        if n != 1 or n2 != 1:
            raise SystemExit(f"No se pudieron poner las migas en {archivo}")
    # Botones de compartir e imprimir, después del script de la calculadora.
    t = re.sub(r'<script type="module" src="(?:\.\./)*compartir\.js"></script>\n', "", t)
    t, n = re.subn(r'(<script type="module" src="((?:\.\./)*)(?:app|cuota-app)\.js"></script>\n)',
                   lambda m: m.group(1) + f'<script type="module" src="{m.group(2)}compartir.js"></script>\n', t, count=1)
    if n != 1:
        raise SystemExit(f"No se encontró el script de la calculadora en {archivo}")
    # Recuadro de Quipu justo debajo de la calculadora (solo en las páginas que lo llevan).
    t = re.sub(r'<section class="tarjeta patrocinio">.*?</section>\n\n  ', "", t, flags=re.S)
    if recomendacion(lang, clave):
        t = sustituir(t, r'<section class="tarjeta ia">', recomendacion(lang, clave) + '<section class="tarjeta ia">', archivo)
    archivo.write_text(t, encoding="utf-8")


# ---------------------------------------------------------------- Calculadoras para insertar en otras webs
# Cada una es una página mínima (sin menú ni pie) que se pone en un iframe. No se indexan: la página
# que se posiciona es la normal. /insertar/ explica cómo ponerlas y da el código para copiar.
WIDGETS = {
    "irpf": {"destino": "irpf_es", "ruta": {"es": "insertar/irpf/", "ca": "ca/inserir/irpf/"}, "altura": 1100},
    "sueldo": {"destino": "sueldo", "ruta": {"es": "insertar/sueldo/", "ca": "ca/inserir/sou/"}, "altura": 980},
}
INSERTAR = {
    "es": {
        "titulo": "Pon nuestras calculadoras en tu web",
        "pie": "Calculadora:",
        "fuente": "Datos oficiales de 2026. Estimación orientativa.",
    },
    "ca": {
        "titulo": "Posa les nostres calculadores al teu web",
        "pie": "Calculadora:",
        "fuente": "Dades oficials del 2026. Estimació orientativa.",
    },
}


def pagina_widget(lang, tipo, p):
    w = WIDGETS[tipo]
    ruta = w["ruta"][lang]
    raiz = "../" * ruta.count("/")
    destino = BASE + RUTAS[w["destino"]][lang]
    i = INSERTAR[lang]
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{p["og_titulo"]}</title>
  <meta name="robots" content="noindex, follow">
  <link rel="icon" href="{ICONO}">
  <link rel="stylesheet" href="{raiz}estilos.css?v={VERSION_CSS}">
</head>
<body class="widget">
<main>
<div class="contenedor">
  <div class="calculadora apilada">
  <form id="formulario" class="tarjeta" novalidate>
{p["formulario"]}
  </form>

  <section class="tarjeta resultado" aria-live="polite">
    <h2>{T[lang]["resultado"]}</h2>
    <div id="resultado"><p>{T[lang]["rellena"]}</p></div>
  </section>
  </div>
  <p class="widget-pie">{i["pie"]} <a href="{destino}" target="_blank" rel="noopener">{TARJETAS[lang][w["destino"]][0]} · {T[lang]["marca"]}</a>. {i["fuente"]}</p>
</div>
</main>
<script type="module" src="{raiz}{p["script"]}"></script>
<script type="module" src="{raiz}widget.js"></script>
</body>
</html>
"""


def cuerpo_insertar(lang):
    """Instrucciones y código para copiar. insertar.js cambia la vista previa y el código según la elección."""
    t = {
        "es": ("Elige la calculadora", "Vista previa", "Código para pegar en tu web", "Copiar el código",
               "Pégalo en tu página donde quieras que aparezca la calculadora (en WordPress, en un bloque «HTML personalizado»). "
               "Se adapta al ancho de tu web y funciona en el móvil.",
               "Condiciones: es gratis, no hace falta registrarse y no pone cookies ni publicidad en tu web. Solo te pedimos que dejes el enlace de debajo de la calculadora."),
        "ca": ("Tria la calculadora", "Vista prèvia", "Codi per enganxar al teu web", "Copia el codi",
               "Enganxa'l a la teva pàgina on vulguis que aparegui la calculadora (al WordPress, en un bloc «HTML personalitzat»). "
               "S'adapta a l'amplada del teu web i funciona al mòbil.",
               "Condicions: és gratuït, no cal registrar-se i no posa galetes ni publicitat al teu web. Només et demanem que deixis l'enllaç de sota de la calculadora."),
    }[lang]
    eleccion, vista, codigo, copiar, como, condiciones = t
    opciones = []
    for n, (tipo, w) in enumerate(WIDGETS.items()):
        titulo, texto = TARJETAS[lang][w["destino"]]
        src = BASE + w["ruta"][lang]
        enlace = BASE + RUTAS[w["destino"]][lang]
        marcado = " checked" if n == 0 else ""
        vista_rel = relativa(RUTAS["insertar"][lang], w["ruta"][lang])
        opciones.append(
            f'      <label class="opcion-widget"><input type="radio" name="widget" value="{tipo}"{marcado} '
            f'data-src="{src}" data-vista="{vista_rel}" data-enlace="{enlace}" data-titulo="{html.escape(titulo)}" data-altura="{w["altura"]}">'
            f'<span><strong>{titulo}</strong>{texto}</span></label>'
        )
    primera = next(iter(WIDGETS.values()))
    return f"""<section class="tarjeta">
    <h2>{eleccion}</h2>
    <div class="opciones-widget">
{chr(10).join(opciones)}
    </div>
    <h3 class="subtitulo">{codigo}</h3>
    <textarea id="codigo" class="codigo" rows="6" readonly aria-label="{codigo}"></textarea>
    <div class="acciones-fila"><button type="button" class="accion" id="copiar">{copiar}</button></div>
    <p class="acciones-aviso" id="copiado" role="status"></p>
    <p class="nota">{como}</p>
    <p class="nota">{condiciones}</p>
  </section>

  <section class="tarjeta">
    <h2>{vista}</h2>
    <iframe id="vista" class="vista-widget" src="{relativa(RUTAS["insertar"][lang], primera["ruta"][lang])}" title="{vista}" height="{primera["altura"]}" loading="lazy"></iframe>
  </section>"""


REPO = "https://github.com/juli2006farres/calculadora-irpf-autonomos-cataluna"


def paginas_insertar():
    es = {
        "lang": "es",
        "clave": "insertar",
        "script": "insertar.js",
        "cuerpo": cuerpo_insertar("es"),
        "titulo": "Calculadoras para autónomos gratis para tu web · Insertar",
        "descripcion": "Pon gratis en tu web la calculadora de IRPF por comunidad o la de sueldo neto de autónomo: copia el código y pégalo. Sin registro ni cookies.",
        "og_titulo": "Pon nuestras calculadoras para autónomos en tu web",
        "og_descripcion": "Calculadoras de IRPF y sueldo neto gratis para tu blog o tu web, con datos oficiales de 2026.",
        "h1": "Pon nuestras calculadoras para autónomos en tu web",
        "entradilla": "Si tienes un blog, una gestoría o una web para autónomos, puedes poner gratis nuestra calculadora de IRPF por comunidad o la de sueldo neto. Copia el código y pégalo en tu página.",
        "faq": [
            ("¿Cuánto cuesta?", "Nada. Es gratis y no hace falta registrarse."),
            ("¿Se actualiza sola?", "Sí. La calculadora se carga desde esta web, así que cuando cambian los datos, por ejemplo al pasar a 2027, se actualiza en tu web sin que tengas que hacer nada."),
            ("¿Recoge datos de mis visitantes?", "No. Los cálculos se hacen en el navegador de cada visitante y no se guarda nada. No hay cookies, analítica ni publicidad."),
            ("¿Se adapta al tamaño de mi web?", "Sí. El ancho se adapta a tu página y el alto crece o encoge con el resultado gracias a la última línea del código, la del «script». Si tu web no permite añadir scripts, quita esa línea: la calculadora funciona igual, con el alto fijo de «height» y una barra de desplazamiento si hace falta."),
        ],
        "aviso": "las calculadoras dan estimaciones orientativas y no sustituyen el consejo de un asesor fiscal. Cada calculadora enlaza sus fuentes oficiales en su página. Más información:",
        "fuentes": [("Código de las calculadoras, con licencia MIT (GitHub)", REPO)],
    }
    ca = {
        "lang": "ca",
        "clave": "insertar",
        "script": "insertar.js",
        "cuerpo": cuerpo_insertar("ca"),
        "titulo": "Calculadores per a autònoms gratuïtes per al teu web · Inserir",
        "descripcion": "Posa gratis al teu web la calculadora d'IRPF per comunitat o la de sou net d'autònom: copia el codi i enganxa'l. Sense registre ni galetes.",
        "og_titulo": "Posa les nostres calculadores per a autònoms al teu web",
        "og_descripcion": "Calculadores d'IRPF i sou net gratuïtes per al teu blog o el teu web, amb dades oficials del 2026.",
        "h1": "Posa les nostres calculadores per a autònoms al teu web",
        "entradilla": "Si tens un blog, una gestoria o un web per a autònoms, pots posar-hi gratis la nostra calculadora d'IRPF per comunitat o la de sou net. Copia el codi i enganxa'l a la teva pàgina.",
        "faq": [
            ("Quant costa?", "Res. És gratuït i no cal registrar-se."),
            ("S'actualitza sola?", "Sí. La calculadora es carrega des d'aquest web, així que quan canvien les dades, per exemple en passar al 2027, s'actualitza al teu web sense que hagis de fer res."),
            ("Recull dades dels meus visitants?", "No. Els càlculs es fan al navegador de cada visitant i no es desa res. No hi ha galetes, analítica ni publicitat."),
            ("S'adapta a la mida del meu web?", "Sí. L'amplada s'adapta a la teva pàgina i l'alçada creix o s'encongeix amb el resultat gràcies a l'última línia del codi, la de l'«script». Si el teu web no permet afegir scripts, treu aquesta línia: la calculadora funciona igual, amb l'alçada fixa de «height» i una barra de desplaçament si cal."),
        ],
        "aviso": "les calculadores donen estimacions orientatives i no substitueixen el consell d'un assessor fiscal. Cada calculadora enllaça les seves fonts oficials a la seva pàgina. Més informació:",
        "fuentes": [("Codi de les calculadores, amb llicència MIT (GitHub)", REPO)],
    }
    return [es, ca]


def llms_txt(paginas):
    """Resumen de la web para asistentes de IA (formato llms.txt: https://llmstxt.org/)."""
    por_clave = {(p["lang"], p["clave"]): p for p in paginas}

    def descripcion(lang, clave):
        p = por_clave.get((lang, clave))
        return p["descripcion"] if p else DESCRIPCIONES[(lang, clave)]

    lineas = [
        "# Calculadoras para autónomos",
        "",
        "> Calculadoras gratuitas para autónomos en España, en castellano y en catalán: IRPF en las 15 comunidades de régimen común, "
        "cuota de autónomos 2026, tarifa plana, regularización de la cuota, sueldo neto, cuánto facturar, IVA, facturas, modelos 130 y 303 "
        "y calendario fiscal 2027. Datos oficiales del BOE, la Agencia Tributaria y la Seguridad Social, sin registro, sin cookies y sin guardar datos.",
        "",
        f"- Datos revisados el {fecha_texto(MODIFICADO, 'es')}, incluido el Real Decreto-ley 43/2026: en 2026, los gastos de difícil "
        "justificación de la estimación directa simplificada son el 10 % del rendimiento, con un máximo de 3.000 €.",
        "- Cada página enlaza sus fuentes oficiales y explica qué incluye y qué no. Son estimaciones orientativas, no asesoramiento fiscal.",
        "- No cubre el País Vasco ni Navarra (IRPF foral), ni Ceuta y Melilla.",
        "- Los cálculos se hacen en el navegador del usuario. El código es público con licencia MIT: "
        "https://github.com/juli2006farres/calculadora-irpf-autonomos-cataluna",
        f"- Las mismas calculadoras están disponibles como servidor MCP para asistentes de IA, con plan gratuito: {MCPIZE}",
        "",
        "## Calculadoras",
        "",
    ]
    for clave in ORDEN:
        lineas.append(f"- [{TARJETAS['es'][clave][0]}]({BASE + RUTAS[clave]['es']}): {descripcion('es', clave)}")
    lineas += ["", "## Por comunidad autónoma", ""]
    for tipo, titulo in (("irpf_es", "IRPF de autónomos"), ("sueldo", "Sueldo neto de autónomo")):
        hijos = [k for k, padre in PADRE.items() if padre == tipo]
        enlaces = ", ".join(f"[{MIGA[('es', k)]}]({BASE + RUTAS[k]['es']})" for k in sorted(hijos, key=lambda k: MIGA[("es", k)]))
        lineas.append(f"- {titulo}: {enlaces}.")
    lineas += ["", "## En catalán", ""]
    for clave in ORDEN:
        lineas.append(f"- [{TARJETAS['ca'][clave][0]}]({BASE + RUTAS[clave]['ca']}): {descripcion('ca', clave)}")
    lineas += ["", "## Optional", "", f"- [Cómo se financia esta web]({BASE + RUTAS['transparencia']['es']}): enlaces de afiliado marcados y servidor MCP."]
    (WEB / "llms.txt").write_text("\n".join(lineas) + "\n", encoding="utf-8")


# Páginas que van al sitemap además de las de ORDEN (las de cada comunidad).
EXTRA_SITEMAP = []


def sitemap():
    lineas = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for clave in ORDEN + EXTRA_SITEMAP:
        es, ca = RUTAS[clave]["es"], RUTAS[clave]["ca"]
        for ruta in (es, ca):
            lineas += [
                "  <url>",
                f"    <loc>{BASE}{ruta}</loc>",
                f"    <lastmod>{MODIFICADO}</lastmod>",
                f'    <xhtml:link rel="alternate" hreflang="es" href="{BASE}{es}"/>',
                f'    <xhtml:link rel="alternate" hreflang="ca" href="{BASE}{ca}"/>',
                f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{es}"/>',
                "  </url>",
            ]
    lineas.append("</urlset>")
    (WEB / "sitemap.xml").write_text("\n".join(lineas) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))
    from contenido_comunidades import PADRE_COMUNIDADES, RUTAS_COMUNIDADES
    from contenido_novedades_2027 import PAGINAS

    RUTAS.update(RUTAS_COMUNIDADES)
    PADRE.update(PADRE_COMUNIDADES)
    EXTRA_SITEMAP.extend(RUTAS_COMUNIDADES)
    for k, padre in PADRE_COMUNIDADES.items():
        REVISION[k] = REVISION[padre]
    for p in PAGINAS:
        if "miga" in p:
            MIGA[(p["lang"], p["clave"])] = p["miga"]

    PAGINAS = [*PAGINAS, *paginas_insertar()]
    EXTRA_SITEMAP.append("insertar")
    por_clave = {(p["lang"], p["clave"]): p for p in PAGINAS}
    for tipo, w in WIDGETS.items():
        for lang in ("es", "ca"):
            destino = WEB / w["ruta"][lang] / "index.html"
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_text(pagina_widget(lang, tipo, por_clave[(lang, w["destino"])]), encoding="utf-8")

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
    for lang in ("es", "ca"):
        destino = WEB / RUTAS["transparencia"][lang] / "index.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(pagina_transparencia(lang), encoding="utf-8")
    # Plazos del calendario fiscal para añadirlos al calendario del móvil o del ordenador.
    from contenido_espana import ARCHIVO_ICS, OFRECER_ICS, calendario_ics

    for lang in ("es", "ca"):
        carpeta = RUTAS["calendario"][lang]
        archivo = WEB / carpeta / ARCHIVO_ICS[lang]
        if OFRECER_ICS:
            archivo.write_bytes(calendario_ics(lang, BASE + carpeta).encode("utf-8"))
        elif archivo.exists():
            archivo.unlink()
    sitemap()
    llms_txt(PAGINAS)
