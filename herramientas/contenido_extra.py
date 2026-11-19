"""Páginas de IVA y de cuánto facturar, en castellano y en catalán."""
from contenido import (BOE_IVA, MODALIDAD, SUELDO_ES, FACTURA_ES, FACTURA_CA, SUELDO_CA, M130_ES, M130_CA,
                       campo, seleccion, casilla)

# ---------------------------------------------------------------- IVA
IVA_ES = {
    "lang": "es",
    "clave": "iva",
    "script": "iva-app.js",
    "titulo": "Calculadora de IVA · Añadir o quitar el IVA de un precio",
    "descripcion": "Calcula el IVA de un precio al momento: añade o quita el IVA del 21 %, 10 % o 4 % y obtén la base imponible y el total. Gratis y sin registro.",
    "og_titulo": "Calculadora de IVA: añadir o quitar el IVA",
    "og_descripcion": "Base imponible, IVA y total de cualquier precio con el 21 %, 10 % o 4 %.",
    "h1": "Calculadora de IVA: añadir o quitar el IVA de un precio",
    "entradilla": "Añade el IVA a un precio sin IVA o quítaselo a un precio con IVA incluido, con los tipos del 21 %, 10 % y 4 %. Verás la base imponible, el IVA y el total al momento.",
    "formulario": f"""    <h2>Datos del precio</h2>
    <fieldset class="segmentos">
      <legend>¿Qué quieres hacer?</legend>
      <div class="pastilla">
      <label><input type="radio" name="modo" value="anadir" checked><span>Añadir IVA</span></label>
      <label><input type="radio" name="modo" value="quitar"><span>Quitar IVA</span></label>
      </div>
    </fieldset>
    <div class="rejilla">
{campo("importe", "Precio (€)", "Precio sin IVA.", "100")}
{seleccion("tipo", "Tipo de IVA", [("21", "21 % (general)"), ("10", "10 % (reducido)"), ("4", "4 % (superreducido)")], "El general es el 21 %.")}
    </div>""",
    "faq": [
        ("¿Cómo se quita el IVA de un precio?",
         "Divide el precio con IVA entre 1,21 si el tipo es del 21 %, entre 1,10 si es del 10 % o entre 1,04 si es del 4 %. Por ejemplo, 121 € con IVA incluido son 100 € de base y 21 € de IVA. Restar un 21 % al precio con IVA da un resultado incorrecto."),
        ("¿Cómo se añade el IVA a un precio?",
         "Multiplica el precio sin IVA por 1,21, por 1,10 o por 1,04, según el tipo. Por ejemplo, 100 € más el 21 % de IVA son 121 €."),
        ("¿Qué tipos de IVA hay en España?",
         f'El general del 21 %, el reducido del 10 %, que se aplica por ejemplo a la hostelería o al transporte de viajeros, y el superreducido del 4 %, que se aplica por ejemplo al pan, la leche, los libros o los medicamentos, según los <a href="{BOE_IVA}">artículos 90 y 91 de la Ley del IVA</a>. En Canarias no se aplica el IVA, sino el IGIC, y en Ceuta y Melilla, el IPSI.'),
        ("¿Qué es la base imponible?",
         "Es el precio sin IVA. Sobre ella se calculan el IVA y, en las facturas de los profesionales, la retención de IRPF."),
    ],
    "aviso": "es una estimación orientativa. El tipo que corresponde depende de cada producto o servicio, así que consúltalo si tienes dudas. Fuente:",
    "fuentes": [("Ley 37/1992 del IVA, artículos 90 y 91 (BOE)", BOE_IVA)],
}

IVA_CA = {
    "lang": "ca",
    "clave": "iva",
    "script": "iva-app.js",
    "titulo": "Calculadora d'IVA · Afegir o treure l'IVA d'un preu",
    "descripcion": "Calcula l'IVA d'un preu al moment: afegeix o treu l'IVA del 21 %, 10 % o 4 % i obtén la base imposable i el total. Gratuïta i sense registre.",
    "og_titulo": "Calculadora d'IVA: afegir o treure l'IVA",
    "og_descripcion": "Base imposable, IVA i total de qualsevol preu amb el 21 %, 10 % o 4 %.",
    "h1": "Calculadora d'IVA: afegir o treure l'IVA d'un preu",
    "entradilla": "Afegeix l'IVA a un preu sense IVA o treu-l'hi a un preu amb IVA inclòs, amb els tipus del 21 %, 10 % i 4 %. Veuràs la base imposable, l'IVA i el total al moment.",
    "formulario": f"""    <h2>Dades del preu</h2>
    <fieldset class="segmentos">
      <legend>Què vols fer?</legend>
      <div class="pastilla">
      <label><input type="radio" name="modo" value="anadir" checked><span>Afegir IVA</span></label>
      <label><input type="radio" name="modo" value="quitar"><span>Treure IVA</span></label>
      </div>
    </fieldset>
    <div class="rejilla">
{campo("importe", "Preu (€)", "Preu sense IVA.", "100")}
{seleccion("tipo", "Tipus d'IVA", [("21", "21 % (general)"), ("10", "10 % (reduït)"), ("4", "4 % (superreduït)")], "El general és el 21 %.")}
    </div>""",
    "faq": [
        ("Com es treu l'IVA d'un preu?",
         "Divideix el preu amb IVA entre 1,21 si el tipus és del 21 %, entre 1,10 si és del 10 % o entre 1,04 si és del 4 %. Per exemple, 121 € amb IVA inclòs són 100 € de base i 21 € d'IVA. Restar un 21 % al preu amb IVA dona un resultat incorrecte."),
        ("Com s'afegeix l'IVA a un preu?",
         "Multiplica el preu sense IVA per 1,21, per 1,10 o per 1,04, segons el tipus. Per exemple, 100 € més el 21 % d'IVA són 121 €."),
        ("Quins tipus d'IVA hi ha a Espanya?",
         f'El general del 21 %, el reduït del 10 %, que s\'aplica per exemple a l\'hostaleria o al transport de viatgers, i el superreduït del 4 %, que s\'aplica per exemple al pa, la llet, els llibres o els medicaments, segons els <a href="{BOE_IVA}">articles 90 i 91 de la Llei de l\'IVA</a>. A les Canàries no s\'aplica l\'IVA, sinó l\'IGIC, i a Ceuta i Melilla, l\'IPSI.'),
        ("Què és la base imposable?",
         "És el preu sense IVA. Sobre aquesta base es calculen l'IVA i, a les factures dels professionals, la retenció d'IRPF."),
    ],
    "aviso": "és una estimació orientativa. El tipus que correspon depèn de cada producte o servei, així que consulta-ho si tens dubtes. Font, en castellà:",
    "fuentes": IVA_ES["fuentes"],
}

# ---------------------------------------------------------------- Cuánto facturar
INICIO = {
    "es": ("Acabo de empezar como autónomo", "Reducción del 20 % del IRPF (art. 32.3 de la Ley del IRPF). Márcala solo si no tuviste actividad económica el año anterior al inicio, es tu primer o segundo año con beneficios y no facturas más del 50 % a quien te pagó como asalariado ese año anterior."),
    "ca": ("Acabo de començar com a autònom", "Reducció del 20 % de l'IRPF (art. 32.3 de la Llei de l'IRPF). Marca-la només si no vas tenir activitat econòmica l'any anterior a l'inici, és el teu primer o segon any amb beneficis i no factures més del 50 % a qui et va pagar com a assalariat aquell any anterior."),
}
CLIENTE = {
    "es": ("Cumplo los requisitos de la reducción para autónomos dependientes", "Art. 32.2.2.º de la Ley del IRPF: entre otros, un único cliente no vinculado y gastos que no superen el 30 % de los ingresos."),
    "ca": ("Compleixo els requisits de la reducció per a autònoms dependents", "Art. 32.2.2n de la Llei de l'IRPF: entre d'altres, un únic client no vinculat i despeses que no superin el 30 % dels ingressos."),
}

OBJETIVO_ES = {
    "lang": "es",
    "clave": "objetivo",
    "script": "objetivo-app.js",
    "titulo": "¿Cuánto tengo que facturar como autónomo? Calculadora 2026",
    "descripcion": "¿Cuánto tienes que facturar como autónomo para ganar 2.000 € netos al mes? Calcúlalo con la cuota de autónomos y el IRPF de Cataluña en 2026.",
    "og_titulo": "¿Cuánto tengo que facturar como autónomo?",
    "og_descripcion": "La facturación y el precio por hora para ganar el sueldo neto que quieres.",
    "h1": "¿Cuánto tengo que facturar como autónomo para ganar lo que quiero?",
    "entradilla": "Escribe el sueldo neto que quieres al mes y calcula cuánto tienes que facturar al año, con la cuota de autónomos y el IRPF de Cataluña en 2026. También te da el precio mínimo por hora.",
    "formulario": f"""    <h2>Tu objetivo para 2026</h2>
    <div class="rejilla">
{campo("neto", "Sueldo neto que quieres al mes (€)", "Lo que quieres que te quede limpio, en 12 pagas.", "2000")}
{campo("gastos", "Gastos de la actividad al año (€)", "Sin contar las cuotas de autónomo.", "5000")}
{campo("horas", "Horas que facturas al mes", "Solo las que cobras a clientes, no las de gestión.", "120")}
{seleccion("modalidad", "Estimación en el IRPF", MODALIDAD["es"], "La que usas en el IRPF. La más habitual es la simplificada.")}
    </div>
{casilla("inicio", *INICIO["es"])}
{casilla("cliente", *CLIENTE["es"])}""",
    "faq": [
        ("¿Cuánto tiene que facturar un autónomo para ganar 2.000 € netos al mes?",
         "En Cataluña en 2026, con 5.000 € de gastos al año y la cuota mínima de su tramo, unos 39.730 € al año sin IVA, unos 3.311 € al mes. De ahí salen 427,21 € al mes de cuota de autónomos y unos 5.601 € de IRPF en el año."),
        ("¿Cómo se calcula?",
         "La calculadora busca la facturación con la que, después de restar los gastos, la cuota mínima de autónomos de tu tramo y el IRPF del año, te queda el sueldo neto que has pedido."),
        ("¿Qué precio por hora debo cobrar?",
         "Divide la facturación anual entre las horas que facturas al año. Cuenta solo las horas que cobras: las vacaciones, los días sin clientes y el tiempo de gestión no se pagan, y por eso el precio por hora tiene que ser más alto de lo que parece."),
        ("¿La facturación incluye el IVA?",
         "No. Es la facturación sin IVA, porque el IVA que cobras lo ingresas a Hacienda. Si facturas con IVA, el cliente pagará además el IVA correspondiente."),
        ("¿Por qué solo vale para Cataluña?",
         "El IRPF tiene una parte autonómica y esta calculadora usa la escala catalana. La cuota de autónomos es igual en toda España."),
    ],
    "aviso": "es una estimación orientativa y no sustituye el consejo de un asesor fiscal o laboral. No incluye la tarifa plana, otras rentas, el mínimo por hijos ni las deducciones. Fuentes:",
    "fuentes": SUELDO_ES["fuentes"],
}

OBJETIVO_CA = {
    "lang": "ca",
    "clave": "objetivo",
    "script": "objetivo-app.js",
    "titulo": "Quant he de facturar com a autònom? Calculadora 2026",
    "descripcion": "Quant has de facturar com a autònom per guanyar 2.000 € nets al mes? Calcula-ho amb la quota d'autònoms i l'IRPF de Catalunya del 2026.",
    "og_titulo": "Quant he de facturar com a autònom?",
    "og_descripcion": "La facturació i el preu per hora per guanyar el sou net que vols.",
    "h1": "Quant he de facturar com a autònom per guanyar el que vull?",
    "entradilla": "Escriu el sou net que vols al mes i calcula quant has de facturar a l'any, amb la quota d'autònoms i l'IRPF de Catalunya del 2026. També et dona el preu mínim per hora.",
    "formulario": f"""    <h2>El teu objectiu per al 2026</h2>
    <div class="rejilla">
{campo("neto", "Sou net que vols al mes (€)", "El que vols que et quedi net, en 12 pagues.", "2000")}
{campo("gastos", "Despeses de l'activitat a l'any (€)", "Sense comptar les quotes d'autònom.", "5000")}
{campo("horas", "Hores que factures al mes", "Només les que cobres als clients, no les de gestió.", "120")}
{seleccion("modalidad", "Estimació a l'IRPF", MODALIDAD["ca"], "La que fas servir a l'IRPF. La més habitual és la simplificada.")}
    </div>
{casilla("inicio", *INICIO["ca"])}
{casilla("cliente", *CLIENTE["ca"])}""",
    "faq": [
        ("Quant ha de facturar un autònom per guanyar 2.000 € nets al mes?",
         "A Catalunya el 2026, amb 5.000 € de despeses l'any i la quota mínima del seu tram, uns 39.730 € l'any sense IVA, uns 3.311 € al mes. D'aquí surten 427,21 € al mes de quota d'autònoms i uns 5.601 € d'IRPF a l'any."),
        ("Com es calcula?",
         "La calculadora busca la facturació amb la qual, després de restar les despeses, la quota mínima d'autònoms del teu tram i l'IRPF de l'any, et queda el sou net que has demanat."),
        ("Quin preu per hora he de cobrar?",
         "Divideix la facturació anual entre les hores que factures a l'any. Compta només les hores que cobres: les vacances, els dies sense clients i el temps de gestió no es paguen, i per això el preu per hora ha de ser més alt del que sembla."),
        ("La facturació inclou l'IVA?",
         "No. És la facturació sense IVA, perquè l'IVA que cobres l'ingresses a Hisenda. Si factures amb IVA, el client pagarà a més l'IVA corresponent."),
        ("Per què només serveix per a Catalunya?",
         "L'IRPF té una part autonòmica i aquesta calculadora fa servir l'escala catalana. La quota d'autònoms és igual a tot Espanya."),
    ],
    "aviso": "és una estimació orientativa i no substitueix el consell d'un assessor fiscal o laboral. No inclou la tarifa plana, altres rendes, el mínim per fills ni les deduccions. Fonts, en castellà:",
    "fuentes": SUELDO_ES["fuentes"],
}

PAGINAS = [FACTURA_ES, FACTURA_CA, IVA_ES, IVA_CA, SUELDO_ES, SUELDO_CA, OBJETIVO_ES, OBJETIVO_CA, M130_ES, M130_CA]
