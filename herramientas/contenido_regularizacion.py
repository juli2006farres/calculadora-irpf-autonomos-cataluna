"""Calculadora de la regularización de la cuota de autónomos de 2026 (art. 308.1.c de la LGSS)."""
from contenido import BOE_CUOTA, FUENTE_RDL_43, MODALIDAD, campo, casilla, seleccion
from contenido_comunidades import PAGINAS as PAGINAS_ANTERIORES
from contenido_extra import CLIENTE
from contenido_tarifa import BOE_LETA

BOE_LGSS_308 = "https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a308"

TARIFA = {
    "es": ("He tenido la tarifa plana en 2026", "Los meses con tarifa plana no se regularizan."),
    "ca": ("He tingut la tarifa plana el 2026", "Els mesos amb tarifa plana no es regularitzen."),
}


def formulario(lang):
    t = {
        "es": ("Tus datos de 2026", "Ingresos del año (€)", "Lo facturado en 2026, sin IVA.",
               "Gastos deducibles (€)", "Sin contar las cuotas de autónomo.",
               "Cuota que has pagado al mes (€)", "Por ejemplo, 299,56 € es la cuota mínima del tramo 1 de la tabla general.",
               "Meses de alta en 2026", "Los meses del año en que has estado de alta como autónomo.",
               "Estimación en el IRPF", "La que usas en el IRPF. La más habitual es la simplificada.", "mes", "meses"),
        "ca": ("Les teves dades del 2026", "Ingressos de l'any (€)", "El que has facturat el 2026, sense IVA.",
               "Despeses deduïbles (€)", "Sense comptar les quotes d'autònom.",
               "Quota que has pagat al mes (€)", "Per exemple, 299,56 € és la quota mínima del tram 1 de la taula general.",
               "Mesos d'alta el 2026", "Els mesos de l'any en què has estat d'alta com a autònom.",
               "Estimació a l'IRPF", "La que fas servir a l'IRPF. La més habitual és la simplificada.", "mes", "mesos"),
    }[lang]
    cab, ing, ing_a, gas, gas_a, cuo, cuo_a, mes, mes_a, mod, mod_a, uno, varios = t
    meses = [(str(n), f"{n} {uno if n == 1 else varios}") for n in range(12, 0, -1)]
    return f"""    <h2>{cab}</h2>
    <div class="rejilla">
{campo("ingresos", ing, ing_a, "30000")}
{campo("gastos", gas, gas_a, "3000")}
{campo("cuota", cuo, cuo_a, "299.56")}
{seleccion("meses", mes, meses, mes_a)}
{seleccion("modalidad", mod, MODALIDAD[lang], mod_a)}
    </div>
{casilla("cliente", *CLIENTE[lang])}
{casilla("tarifa", *TARIFA[lang])}"""


FUENTES = [
    ("Ley General de la Seguridad Social, artículo 308: cotización y regularización (BOE)", BOE_LGSS_308),
    ("Ley 20/2007 del Estatuto del trabajo autónomo, artículo 38 ter: tarifa plana (BOE)", BOE_LETA),
    ("Bases y tipos de cotización de 2026: Orden PJC/297/2026 (BOE)", BOE_CUOTA),
    FUENTE_RDL_43,
]

REGULARIZACION_ES = {
    "lang": "es",
    "clave": "regularizacion",
    "script": "regularizacion-app.js",
    "formulario": formulario("es"),
    "titulo": "Regularización cuota autónomos 2026 · ¿Te devuelven o pagas?",
    "descripcion": "Calcula gratis si la Seguridad Social te devolverá dinero o te cobrará más por tu cuota de autónomos de 2026, según tus rendimientos reales.",
    "og_titulo": "Calculadora de la regularización de la cuota de autónomos 2026",
    "og_descripcion": "Si la Seguridad Social te devolverá o te cobrará la diferencia de tu cuota de 2026.",
    "h1": "Regularización de la cuota de autónomos 2026: ¿te devolverán o tendrás que pagar?",
    "entradilla": "Durante el año pagas una cuota provisional. Cuando Hacienda comunica tus rendimientos reales, la Seguridad Social la compara con la de tu tramo: calcula si te devolverán dinero o tendrás que pagar la diferencia.",
    "faq": [
        ("¿Qué es la regularización de la cuota de autónomos?",
         f'Desde 2023, los autónomos cotizan según sus rendimientos reales. Durante el año pagas una cuota provisional según lo que prevés ganar, y cuando Hacienda comunica a la Seguridad Social tus rendimientos del año, se compara lo que pagaste con la cuota del tramo que te corresponde, según el <a href="{BOE_LGSS_308}">artículo 308.1.c de la Ley General de la Seguridad Social</a>.'),
        ("¿Cuándo me devuelven o tengo que pagar?",
         "Si pagaste menos que la cuota mínima de tu tramo real, pagas la diferencia hasta el último día del mes siguiente a la notificación, sin recargo ni intereses. Si pagaste más que la cuota máxima de tu tramo real, la Seguridad Social te devuelve el exceso de oficio, sin intereses, antes del 30 de abril del año siguiente a aquel en que Hacienda le comunicó tus rendimientos. Si tu cuota está entre la mínima y la máxima del tramo, no cambia nada."),
        ("¿Qué rendimiento usa la Seguridad Social?",
         f'El rendimiento neto de tu actividad en el IRPF, más las cuotas de autónomo que has pagado, menos un 7 % por gastos genéricos, repartido entre los meses de alta. En 2026, en estimación directa simplificada, el rendimiento neto ya resta un 10 % de gastos de difícil justificación, con un máximo de 3.000 €, por el <a href="{FUENTE_RDL_43[1]}">Real Decreto-ley 43/2026</a>.'),
        ("¿Me pasará con 30.000 € de ingresos?",
         "Con 30.000 € de ingresos y 3.000 € de gastos en estimación directa simplificada, tu rendimiento queda en el tramo 5 de la tabla general, con una cuota mínima de 380,88 € al mes. Si has pagado todo el año la mínima del tramo 1, 299,56 €, tendrás que pagar 975,84 €."),
        ("¿Y si tengo la tarifa plana?",
         f'Los meses con tarifa plana no se regularizan, según el <a href="{BOE_LETA}">artículo 38 ter.6 de la Ley 20/2007</a>. En la prórroga de 12 meses tampoco, si tus rendimientos del año quedan por debajo del salario mínimo.'),
        ("¿Puedo evitar una regularización grande?",
         f'Sí: puedes cambiar tu base de cotización durante el año para ajustarla a lo que prevés ganar, como indica el <a href="{BOE_LGSS_308}">artículo 308.1.a, regla 3.ª, de la Ley General de la Seguridad Social</a>. Con la <a href="../cuota-autonomos-2026/">calculadora de la cuota</a> ves qué tramo te corresponde con tus previsiones.'),
    ],
    "aviso": "es una estimación orientativa y no sustituye la resolución de la Seguridad Social ni el consejo de un asesor. Supone la misma cuota todos los meses de alta y solo rendimientos de tu actividad como autónomo persona física: no vale para autónomos societarios ni familiares colaboradores, que tienen otras reglas. Fuentes:",
    "fuentes": FUENTES,
}

REGULARIZACION_CA = {
    "lang": "ca",
    "clave": "regularizacion",
    "script": "regularizacion-app.js",
    "formulario": formulario("ca"),
    "titulo": "Regularització quota autònoms 2026 · Et retornen o pagues?",
    "descripcion": "Calcula gratis si la Seguretat Social et retornarà diners o et cobrarà més per la teva quota d'autònoms del 2026, segons els teus rendiments reals.",
    "og_titulo": "Calculadora de la regularització de la quota d'autònoms 2026",
    "og_descripcion": "Si la Seguretat Social et retornarà o et cobrarà la diferència de la quota del 2026.",
    "h1": "Regularització de la quota d'autònoms 2026: et retornaran o hauràs de pagar?",
    "entradilla": "Durant l'any pagues una quota provisional. Quan Hisenda comunica els teus rendiments reals, la Seguretat Social la compara amb la del teu tram: calcula si et retornaran diners o hauràs de pagar la diferència.",
    "faq": [
        ("Què és la regularització de la quota d'autònoms?",
         f'Des del 2023, els autònoms coticen segons els seus rendiments reals. Durant l\'any pagues una quota provisional segons el que preveus guanyar, i quan Hisenda comunica a la Seguretat Social els teus rendiments de l\'any, es compara el que vas pagar amb la quota del tram que et correspon, segons l\'<a href="{BOE_LGSS_308}">article 308.1.c de la Llei general de la Seguretat Social</a>.'),
        ("Quan em retornen o he de pagar?",
         "Si vas pagar menys que la quota mínima del teu tram real, pagues la diferència fins a l'últim dia del mes següent a la notificació, sense recàrrec ni interessos. Si vas pagar més que la quota màxima del teu tram real, la Seguretat Social et retorna l'excés d'ofici, sense interessos, abans del 30 d'abril de l'any següent a aquell en què Hisenda li va comunicar els teus rendiments. Si la teva quota és entre la mínima i la màxima del tram, no canvia res."),
        ("Quin rendiment fa servir la Seguretat Social?",
         f'El rendiment net de la teva activitat a l\'IRPF, més les quotes d\'autònom que has pagat, menys un 7 % per despeses genèriques, repartit entre els mesos d\'alta. El 2026, en estimació directa simplificada, el rendiment net ja resta un 10 % de despeses de difícil justificació, amb un màxim de 3.000 €, pel <a href="{FUENTE_RDL_43[1]}">Reial decret llei 43/2026</a>.'),
        ("Em passarà amb 30.000 € d'ingressos?",
         "Amb 30.000 € d'ingressos i 3.000 € de despeses en estimació directa simplificada, el teu rendiment queda al tram 5 de la taula general, amb una quota mínima de 380,88 € al mes. Si has pagat tot l'any la mínima del tram 1, 299,56 €, hauràs de pagar 975,84 €."),
        ("I si tinc la tarifa plana?",
         f'Els mesos amb tarifa plana no es regularitzen, segons l\'<a href="{BOE_LETA}">article 38 ter.6 de la Llei 20/2007</a>. A la pròrroga de 12 mesos tampoc, si els teus rendiments de l\'any queden per sota del salari mínim.'),
        ("Puc evitar una regularització gran?",
         f'Sí: pots canviar la teva base de cotització durant l\'any per ajustar-la al que preveus guanyar, com indica l\'<a href="{BOE_LGSS_308}">article 308.1.a, regla 3a, de la Llei general de la Seguretat Social</a>. Amb la <a href="../quota-autonoms-2026/">calculadora de la quota</a> veus quin tram et correspon amb les teves previsions.'),
    ],
    "aviso": "és una estimació orientativa i no substitueix la resolució de la Seguretat Social ni el consell d'un assessor. Suposa la mateixa quota tots els mesos d'alta i només rendiments de la teva activitat com a autònom persona física: no serveix per a autònoms societaris ni familiars col·laboradors, que tenen altres regles. Fonts, en castellà:",
    "fuentes": FUENTES,
}

PAGINAS = [*PAGINAS_ANTERIORES, REGULARIZACION_ES, REGULARIZACION_CA]
