"""Genera las plantillas de factura de autónomo en Excel y Word, en castellano y en catalán.

Uso, desde la carpeta de la web: python -I herramientas/plantillas.py .

Contenido según el art. 6 del Reglamento de facturación (Real Decreto 1619/2012). Las plantillas no
llevan macros ni generan libros registro: según la AEAT, usar una hoja de cálculo o un procesador de
texto solo para introducir datos, expedir, imprimir y conservar facturas no está sujeto a Verifactu.
"""
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

WEB = Path(sys.argv[1])
DESTINO = WEB / "plantillas"
AZUL = "1B64A0"
WEB_URL = "https://calculadorasautonomos.es/"

TEXTOS = {
    "es": {
        "archivo": "factura-autonomo",
        "hoja": "Factura",
        "titulo": "FACTURA",
        "numero": "Número de factura",
        "numero_ej": "2026-001",
        "fecha": "Fecha de expedición",
        "fecha_op": "Fecha de la operación (si es distinta)",
        "emisor": "DATOS DEL AUTÓNOMO (EMISOR)",
        "cliente": "DATOS DEL CLIENTE",
        "nombre": "Nombre y apellidos o razón social",
        "nif": "NIF",
        "domicilio": "Domicilio",
        "nombre_ej_emisor": "Tu nombre y apellidos",
        "nombre_ej_cliente": "Nombre o razón social del cliente",
        "nif_ej": "00000000T",
        "dom_ej": "Calle, número, código postal y población",
        "conceptos": ["Descripción", "Cantidad", "Precio unitario sin IVA (€)", "Importe (€)"],
        "linea_ej": "Descripción del servicio o producto",
        "base": "Base imponible",
        "tipo_iva": "Tipo de IVA (%)",
        "cuota_iva": "Cuota de IVA",
        "tipo_ret": "Retención de IRPF (%)",
        "cuota_ret": "Retención de IRPF",
        "total": "TOTAL A PAGAR",
        "pago": "Forma de pago",
        "pago_ej": "Transferencia bancaria a la cuenta ES00 0000 0000 0000 0000 0000",
        "notas": [
            "Cómo usarla: cambia los textos en gris por tus datos y escribe los conceptos. El IVA, la retención y el total se calculan solos.",
            "IVA: 21 % general, 10 % reducido, 4 % superreducido o 0 % si la operación está exenta (indica entonces el motivo de la exención).",
            "Retención: 15 % para profesionales, 7 % el año de inicio y los dos siguientes, 0 % si el cliente es un particular o tu actividad es empresarial.",
            "Numera las facturas de forma correlativa, sin saltos. Esta plantilla no sustituye el consejo de un asesor.",
        ],
        "word_calculo": "Calcula la base, el IVA, la retención y el total con la calculadora gratuita: " + WEB_URL + "factura-autonomos/",
        "pie": "Plantilla gratuita de " + WEB_URL,
    },
    "ca": {
        "archivo": "factura-autonom",
        "hoja": "Factura",
        "titulo": "FACTURA",
        "numero": "Número de factura",
        "numero_ej": "2026-001",
        "fecha": "Data d'expedició",
        "fecha_op": "Data de l'operació (si és diferent)",
        "emisor": "DADES DE L'AUTÒNOM (EMISSOR)",
        "cliente": "DADES DEL CLIENT",
        "nombre": "Nom i cognoms o raó social",
        "nif": "NIF",
        "domicilio": "Domicili",
        "nombre_ej_emisor": "El teu nom i cognoms",
        "nombre_ej_cliente": "Nom o raó social del client",
        "nif_ej": "00000000T",
        "dom_ej": "Carrer, número, codi postal i població",
        "conceptos": ["Descripció", "Quantitat", "Preu unitari sense IVA (€)", "Import (€)"],
        "linea_ej": "Descripció del servei o producte",
        "base": "Base imposable",
        "tipo_iva": "Tipus d'IVA (%)",
        "cuota_iva": "Quota d'IVA",
        "tipo_ret": "Retenció d'IRPF (%)",
        "cuota_ret": "Retenció d'IRPF",
        "total": "TOTAL A PAGAR",
        "pago": "Forma de pagament",
        "pago_ej": "Transferència bancària al compte ES00 0000 0000 0000 0000 0000",
        "notas": [
            "Com fer-la servir: canvia els textos en gris per les teves dades i escriu els conceptes. L'IVA, la retenció i el total es calculen sols.",
            "IVA: 21 % general, 10 % reduït, 4 % superreduït o 0 % si l'operació està exempta (indica llavors el motiu de l'exempció).",
            "Retenció: 15 % per a professionals, 7 % l'any d'inici i els dos següents, 0 % si el client és un particular o la teva activitat és empresarial.",
            "Numera les factures de manera correlativa, sense salts. Aquesta plantilla no substitueix el consell d'un assessor.",
        ],
        "word_calculo": "Calcula la base, l'IVA, la retenció i el total amb la calculadora gratuïta: " + WEB_URL + "ca/factura-autonoms/",
        "pie": "Plantilla gratuïta de " + WEB_URL,
    },
}


def excel(lang):
    t = TEXTOS[lang]
    wb = Workbook()
    ws = wb.active
    ws.title = t["hoja"]
    ws.sheet_view.showGridLines = False
    for col, ancho in zip("ABCD", (46, 12, 24, 18)):
        ws.column_dimensions[col].width = ancho
    gris = Font(color="7A8694", italic=True)
    negrita = Font(bold=True)
    cabecera = Font(bold=True, color="FFFFFF")
    relleno = PatternFill("solid", fgColor=AZUL)
    claro = PatternFill("solid", fgColor="E9F2FA")
    fino = Side(style="thin", color="C9D3DD")
    borde = Border(top=fino, bottom=fino, left=fino, right=fino)
    euros = '#,##0.00 "€"'

    ws["A1"] = t["titulo"]
    ws["A1"].font = Font(bold=True, size=20, color=AZUL)
    filas = [(t["numero"], t["numero_ej"]), (t["fecha"], "01/01/2026"), (t["fecha_op"], "")]
    for i, (etiqueta, valor) in enumerate(filas, start=3):
        ws.cell(i, 1, etiqueta).font = negrita
        ws.cell(i, 3, valor).font = gris

    def bloque(fila, titulo, nombre_ej):
        ws.cell(fila, 1, titulo).font = Font(bold=True, color=AZUL)
        for j, (etiqueta, valor) in enumerate(((t["nombre"], nombre_ej), (t["nif"], t["nif_ej"]), (t["domicilio"], t["dom_ej"])), start=1):
            ws.cell(fila + j, 1, etiqueta)
            ws.cell(fila + j, 3, valor).font = gris

    bloque(7, t["emisor"], t["nombre_ej_emisor"])
    bloque(12, t["cliente"], t["nombre_ej_cliente"])

    primera = 18
    for c, texto in enumerate(t["conceptos"], start=1):
        celda = ws.cell(primera - 1, c, texto)
        celda.font, celda.fill, celda.border = cabecera, relleno, borde
        celda.alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[primera - 1].height = 32
    lineas = 8
    for f in range(primera, primera + lineas):
        for c in range(1, 5):
            ws.cell(f, c).border = borde
        ws.cell(f, 3).number_format = euros
        ws.cell(f, 4, f'=IF(OR(B{f}="",C{f}=""),"",B{f}*C{f})').number_format = euros
    ws.cell(primera, 1, t["linea_ej"]).font = gris
    ws.cell(primera, 2, 1)
    ws.cell(primera, 3, 1000)
    ultima = primera + lineas - 1

    r = ultima + 2
    resumen = [
        (t["base"], f"=SUM(D{primera}:D{ultima})", None),
        (t["tipo_iva"], 21, "iva"),
        (t["cuota_iva"], f"=ROUND(D{r}*C{r + 1}/100,2)", None),
        (t["tipo_ret"], 15, "ret"),
        (t["cuota_ret"], f"=-ROUND(D{r}*C{r + 3}/100,2)", None),
        (t["total"], f"=D{r}+D{r + 2}+D{r + 4}", None),
    ]
    validacion_iva = DataValidation(type="list", formula1='"21,10,4,0"', allow_blank=False)
    validacion_ret = DataValidation(type="list", formula1='"15,7,0"', allow_blank=False)
    ws.add_data_validation(validacion_iva)
    ws.add_data_validation(validacion_ret)
    for i, (etiqueta, valor, tipo) in enumerate(resumen):
        fila = r + i
        ws.cell(fila, 1, etiqueta).font = negrita
        if tipo:
            celda = ws.cell(fila, 3, valor)
            celda.fill, celda.border = claro, borde
            (validacion_iva if tipo == "iva" else validacion_ret).add(celda)
        else:
            ws.cell(fila, 4, valor).number_format = euros
    total = r + len(resumen) - 1
    for c in (1, 4):
        celda = ws.cell(total, c)
        celda.font, celda.fill = Font(bold=True, color="FFFFFF", size=12), relleno
    ws.cell(total, 2).fill = relleno
    ws.cell(total, 3).fill = relleno

    p = total + 2
    ws.cell(p, 1, t["pago"]).font = negrita
    ws.cell(p, 3, t["pago_ej"]).font = gris
    for i, nota in enumerate(t["notas"], start=p + 2):
        ws.cell(i, 1, nota).font = Font(size=9, color="5A6675")
    ws.cell(p + 2 + len(t["notas"]) + 1, 1, t["pie"]).font = Font(size=9, color=AZUL)

    ws.print_area = f"A1:D{p + 2 + len(t['notas']) + 1}"
    ws.page_setup.fitToWidth = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    # El archivo no guarda resultados precalculados: así cualquier programa recalcula al abrirlo.
    wb.calculation.fullCalcOnLoad = True
    wb.properties.title = t["titulo"].title()
    wb.properties.creator = "Calculadoras para autónomos"
    destino = DESTINO / f"{t['archivo']}.xlsx"
    wb.save(destino)
    return destino


def word(lang):
    t = TEXTOS[lang]
    doc = Document()
    estilo = doc.styles["Normal"]
    estilo.font.name = "Calibri"
    estilo.font.size = Pt(10.5)
    titulo = doc.add_paragraph()
    run = titulo.add_run(t["titulo"])
    run.bold, run.font.size, run.font.color.rgb = True, Pt(22), RGBColor.from_string(AZUL)

    def tabla_datos(filas):
        tabla = doc.add_table(rows=0, cols=2)
        tabla.style = "Table Grid"
        for etiqueta, valor in filas:
            celdas = tabla.add_row().cells
            celdas[0].text = etiqueta
            celdas[0].paragraphs[0].runs[0].bold = True
            celdas[1].text = valor
        return tabla

    tabla_datos([(t["numero"], t["numero_ej"]), (t["fecha"], "01/01/2026"), (t["fecha_op"], "")])
    for titulo_bloque, nombre in ((t["emisor"], t["nombre_ej_emisor"]), (t["cliente"], t["nombre_ej_cliente"])):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        r = p.add_run(titulo_bloque)
        r.bold, r.font.color.rgb = True, RGBColor.from_string(AZUL)
        tabla_datos([(t["nombre"], nombre), (t["nif"], t["nif_ej"]), (t["domicilio"], t["dom_ej"])])

    doc.add_paragraph()
    conceptos = doc.add_table(rows=1, cols=4)
    conceptos.style = "Table Grid"
    for celda, texto in zip(conceptos.rows[0].cells, t["conceptos"]):
        celda.text = texto
        celda.paragraphs[0].runs[0].bold = True
    for valores in ((t["linea_ej"], "1", "1.000,00", "1.000,00"), *[("", "", "", "")] * 7):
        for celda, texto in zip(conceptos.add_row().cells, valores):
            celda.text = texto

    doc.add_paragraph()
    resumen = doc.add_table(rows=0, cols=2)
    resumen.style = "Table Grid"
    for etiqueta, valor in (
        (t["base"], "1.000,00 €"),
        (t["tipo_iva"] + ": 21", "210,00 €"),
        (t["tipo_ret"] + ": 15", "−150,00 €"),
        (t["total"], "1.060,00 €"),
    ):
        celdas = resumen.add_row().cells
        celdas[0].text, celdas[1].text = etiqueta, valor
        celdas[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for celda in resumen.rows[-1].cells:
        celda.paragraphs[0].runs[0].bold = True

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.add_run(t["pago"] + ": ").bold = True
    p.add_run(t["pago_ej"])
    for texto in [t["word_calculo"], *t["notas"][1:], t["pie"]]:
        nota = doc.add_paragraph()
        r = nota.add_run(texto)
        r.font.size, r.font.color.rgb = Pt(8.5), RGBColor.from_string("5A6675")
    doc.core_properties.title = t["titulo"].title()
    doc.core_properties.author = "Calculadoras para autónomos"
    destino = DESTINO / f"{t['archivo']}.docx"
    doc.save(destino)
    return destino


if __name__ == "__main__":
    DESTINO.mkdir(exist_ok=True)
    for lang in ("es", "ca"):
        print(excel(lang), word(lang))
