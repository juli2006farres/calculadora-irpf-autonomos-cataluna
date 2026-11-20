"""Calculadora de la tarifa plana de autónomos 2026 (cuota reducida del art. 38 ter de la Ley 20/2007)."""
from contenido import BOE_CUOTA, MODALIDAD, campo, casilla, seleccion
from contenido_espana import PAGINAS as PAGINAS_ANTERIORES
from contenido_extra import CLIENTE

BOE_LETA = "https://www.boe.es/buscar/act.php?id=BOE-A-2007-13409#a3-5"
BOE_RDL_13_2022 = "https://www.boe.es/buscar/act.php?id=BOE-A-2022-12482#dt-5"
BOE_SMI_2026 = "https://www.boe.es/buscar/act.php?id=BOE-A-2026-3815"
BOE_SMI_2027 = "https://www.boe.es/buscar/act.php?id=BOE-A-2026-24189"
SS_GUIA = "https://portal.seg-social.gob.es/wps/portal/importass/importass/Colectivos/Trabajo+Autonomo/guia"

ESPECIAL = {
    "es": ("Tengo una discapacidad del 33 % o más, o soy víctima de violencia de género o de terrorismo",
           "En estos casos la tarifa plana dura 24 meses y la prórroga, 36 (art. 38 ter.10 de la Ley 20/2007)."),
    "ca": ("Tinc una discapacitat del 33 % o més, o soc víctima de violència de gènere o de terrorisme",
           "En aquests casos la tarifa plana dura 24 mesos i la pròrroga, 36 (art. 38 ter.10 de la Llei 20/2007)."),
}


def formulario(lang):
    t = {
        "es": ("Tus previsiones", "Ingresos anuales previstos (€)", "Lo que prevés facturar en un año, sin IVA.",
               "Gastos deducibles (€)", "Sin contar las cuotas de autónomo.", "Estimación en el IRPF",
               "La que usas en el IRPF. La más habitual es la simplificada."),
        "ca": ("Les teves previsions", "Ingressos anuals previstos (€)", "El que preveus facturar en un any, sense IVA.",
               "Despeses deduïbles (€)", "Sense comptar les quotes d'autònom.", "Estimació a l'IRPF",
               "La que fas servir a l'IRPF. La més habitual és la simplificada."),
    }[lang]
    cab, ing, ing_a, gas, gas_a, mod, mod_a = t
    return f"""    <h2>{cab}</h2>
    <div class="rejilla">
{campo("ingresos", ing, ing_a, "20000")}
{campo("gastos", gas, gas_a, "3000")}
{seleccion("modalidad", mod, MODALIDAD[lang], mod_a)}
    </div>
{casilla("cliente", *CLIENTE[lang])}
{casilla("especial", *ESPECIAL[lang])}"""


FUENTES = [
    ("Ley 20/2007 del Estatuto del trabajo autónomo, artículo 38 ter (BOE)", BOE_LETA),
    ("Real Decreto-ley 13/2022, disposición transitoria 5.ª: cuota de 2023 a 2025 (BOE)", BOE_RDL_13_2022),
    ("Guía práctica de trabajo autónomo: tarifa plana de 2026 (Seguridad Social)", SS_GUIA),
    ("Salario mínimo de 2026: Real Decreto 126/2026 (BOE)", BOE_SMI_2026),
    ("Salario mínimo de 2027: Real Decreto 1013/2026 (BOE)", BOE_SMI_2027),
    ("Bases y tipos de cotización de 2026: Orden PJC/297/2026 (BOE)", BOE_CUOTA),
]

TARIFA_ES = {
    "lang": "es",
    "clave": "tarifa",
    "script": "tarifa-app.js",
    "titulo": "Tarifa plana autónomos 2026: calculadora de ahorro y prórroga",
    "descripcion": "Calcula cuánto te ahorras con la tarifa plana de autónomos de 2026, de 88,64 € al mes, frente a tu cuota normal, y si puedes alargarla 12 meses más.",
    "og_titulo": "Calculadora de la tarifa plana de autónomos 2026",
    "og_descripcion": "Cuánto te ahorras con la tarifa plana frente a tu cuota normal y si puedes alargarla.",
    "h1": "Tarifa plana de autónomos 2026: cuánto te ahorras",
    "entradilla": "Compara la tarifa plana con la cuota que pagarías según lo que ganas, mira cuánto te ahorras el primer año y comprueba si puedes alargarla 12 meses más.",
    "formulario": formulario("es"),
    "faq": [
        ("¿Cuánto es la tarifa plana de autónomos en 2026?",
         f'80 € al mes de cuota reducida más la cotización del Mecanismo de Equidad Intergeneracional (MEI), en total 88,64 € al mes, según la <a href="{SS_GUIA}">guía de trabajo autónomo de la Seguridad Social</a>. La ley deja el importe de 2026 en manos de los Presupuestos, que no se han aprobado, y la Seguridad Social sigue aplicando los mismos 80 € que entre 2023 y 2025.'),
        ("¿Quién puede pedir la tarifa plana?",
         "Quien se da de alta como autónomo por primera vez o no ha estado de alta en los dos años anteriores, o en los tres anteriores si ya tuvo la tarifa plana. No la tienen los familiares que trabajan con un autónomo (hasta el segundo grado). Se pide al darse de alta, en Importass, y hay que estar al corriente con la Seguridad Social y con Hacienda."),
        ("¿Cuánto me ahorro con la tarifa plana?",
         "Depende de lo que ganes, porque sin ella pagarías la cuota de tu tramo. Con 40.000 € de ingresos y 5.000 € de gastos, la cuota normal mínima es de 427,21 € al mes: con la tarifa plana te ahorras 338,57 € al mes, 4.062,84 € en el primer año."),
        ("¿Se puede alargar la tarifa plana?",
         "Sí, 12 meses más si tu rendimiento neto del año queda por debajo del salario mínimo: 17.094 € en 2026 y 18.004 € en 2027. Hay que pedirlo antes de que acabe el primer periodo, con una declaración de que no lo superarás. Si al final lo superas, la Seguridad Social te cobra la diferencia de ese año."),
        ("¿Y si tengo una discapacidad o soy víctima de violencia de género o de terrorismo?",
         "La tarifa plana dura 24 meses en lugar de 12, y la prórroga, 36 meses en lugar de 12, con la misma condición del salario mínimo. La discapacidad tiene que ser del 33 % o más. Entre 2023 y 2025 la cuota de la prórroga era de 160 € al mes; para 2026 no se ha publicado la cifra."),
        ("¿Qué no cubre la tarifa plana?",
         "Mientras la tienes no cotizas por cese de actividad, el paro de los autónomos, ni por formación profesional. Y tus prestaciones, como una baja, se calculan con la base mínima del tramo 1 de la tabla general, no con la de tus ingresos."),
        ("¿Cuánto me queda al mes con la tarifa plana?",
         'Usa la <a href="../sueldo-neto-autonomo/">calculadora de sueldo neto</a> y escribe 88,64 € en el campo de la cuota. Si acabas de empezar, marca también la reducción del 20 % del IRPF por inicio de actividad.'),
    ],
    "aviso": "es una estimación orientativa y no sustituye el consejo de un asesor laboral. La cuota normal es la mínima de tu tramo con las tablas oficiales de 2026, y los 88,64 € son el importe que publica la Seguridad Social para 2026. Fuentes:",
    "fuentes": FUENTES,
}

TARIFA_CA = {
    "lang": "ca",
    "clave": "tarifa",
    "script": "tarifa-app.js",
    "titulo": "Tarifa plana autònoms 2026: calculadora d'estalvi i pròrroga",
    "descripcion": "Calcula quant t'estalvies amb la tarifa plana d'autònoms del 2026, de 88,64 € al mes, davant la teva quota normal, i si la pots allargar 12 mesos més.",
    "og_titulo": "Calculadora de la tarifa plana d'autònoms 2026",
    "og_descripcion": "Quant t'estalvies amb la tarifa plana davant la teva quota normal i si la pots allargar.",
    "h1": "Tarifa plana d'autònoms 2026: quant t'estalvies",
    "entradilla": "Compara la tarifa plana amb la quota que pagaries segons el que guanyes, mira quant t'estalvies el primer any i comprova si la pots allargar 12 mesos més.",
    "formulario": formulario("ca"),
    "faq": [
        ("Quant és la tarifa plana d'autònoms el 2026?",
         f'80 € al mes de quota reduïda més la cotització del Mecanisme d\'Equitat Intergeneracional (MEI), en total 88,64 € al mes, segons la <a href="{SS_GUIA}">guia de treball autònom de la Seguretat Social</a>. La llei deixa l\'import del 2026 en mans dels Pressupostos, que no s\'han aprovat, i la Seguretat Social continua aplicant els mateixos 80 € que entre el 2023 i el 2025.'),
        ("Qui pot demanar la tarifa plana?",
         "Qui es dona d'alta com a autònom per primera vegada o no ha estat d'alta els dos anys anteriors, o els tres anteriors si ja va tenir la tarifa plana. No la tenen els familiars que treballen amb un autònom (fins al segon grau). Es demana en donar-se d'alta, a Importass, i cal estar al corrent amb la Seguretat Social i amb Hisenda."),
        ("Quant m'estalvio amb la tarifa plana?",
         "Depèn del que guanyis, perquè sense la tarifa pagaries la quota del teu tram. Amb 40.000 € d'ingressos i 5.000 € de despeses, la quota normal mínima és de 427,21 € al mes: amb la tarifa plana t'estalvies 338,57 € al mes, 4.062,84 € el primer any."),
        ("Es pot allargar la tarifa plana?",
         "Sí, 12 mesos més si el teu rendiment net de l'any queda per sota del salari mínim: 17.094 € el 2026 i 18.004 € el 2027. Cal demanar-ho abans que acabi el primer període, amb una declaració que no el superaràs. Si al final el superes, la Seguretat Social et cobra la diferència d'aquell any."),
        ("I si tinc una discapacitat o soc víctima de violència de gènere o de terrorisme?",
         "La tarifa plana dura 24 mesos en lloc de 12, i la pròrroga, 36 mesos en lloc de 12, amb la mateixa condició del salari mínim. La discapacitat ha de ser del 33 % o més. Entre el 2023 i el 2025 la quota de la pròrroga era de 160 € al mes; per al 2026 no se n'ha publicat la xifra."),
        ("Què no cobreix la tarifa plana?",
         "Mentre la tens no cotitzes per cessament d'activitat, l'atur dels autònoms, ni per formació professional. I les teves prestacions, com una baixa, es calculen amb la base mínima del tram 1 de la taula general, no amb la dels teus ingressos."),
        ("Quant em queda al mes amb la tarifa plana?",
         'Fes servir la <a href="../sou-net-autonom/">calculadora de sou net</a> i escriu 88,64 € al camp de la quota. Si acabes de començar, marca també la reducció del 20 % de l\'IRPF per inici d\'activitat.'),
    ],
    "aviso": "és una estimació orientativa i no substitueix el consell d'un assessor laboral. La quota normal és la mínima del teu tram amb les taules oficials del 2026, i els 88,64 € són l'import que publica la Seguretat Social per al 2026. Fonts, en castellà:",
    "fuentes": FUENTES,
}

PAGINAS = [*PAGINAS_ANTERIORES, TARIFA_ES, TARIFA_CA]
