# Calculadoras para autónomos

Web estática y gratuita con calculadoras para autónomos, en castellano y en catalán. Se publica con GitHub Pages en <https://calculadorasautonomos.es/>.

| Calculadora | Castellano | Catalán | Ámbito |
|---|---|---|---|
| IRPF por comunidad autónoma | `/calculadora-irpf-autonomos/` | `/ca/calculadora-irpf-autonoms/` | 15 comunidades de régimen común, 2025 y 2026 |
| IRPF de autónomos | `/` | `/ca/` | Cataluña, 2025 y 2026 |
| Cuota de autónomos 2026 | `/cuota-autonomos-2026/` | `/ca/quota-autonoms-2026/` | Toda España |
| Tarifa plana 2026 | `/tarifa-plana-autonomos-2026/` | `/ca/tarifa-plana-autonoms-2026/` | Toda España |
| Regularización de la cuota 2026 | `/regularizacion-cuota-autonomos-2026/` | `/ca/regularitzacio-quota-autonoms-2026/` | Toda España |
| Factura con IVA e IRPF | `/factura-autonomos/` | `/ca/factura-autonoms/` | Toda España |
| IVA: añadir o quitar | `/calculadora-iva/` | `/ca/calculadora-iva/` | Toda España salvo Canarias, Ceuta y Melilla |
| Sueldo neto de autónomo | `/sueldo-neto-autonomo/` | `/ca/sou-net-autonom/` | 15 comunidades, 2026 |
| Cuánto facturar para un neto | `/cuanto-facturar-autonomo/` | `/ca/quant-facturar-autonom/` | 15 comunidades, 2026 |
| Modelo 130 | `/modelo-130/` | `/ca/model-130/` | Toda España salvo País Vasco y Navarra |
| Modelo 303 | `/modelo-303/` | `/ca/model-303/` | Toda España salvo Canarias, Ceuta, Melilla, País Vasco y Navarra |
| Plantilla de factura (Excel y Word) | `/plantilla-factura-autonomo/` | `/ca/plantilla-factura-autonom/` | Toda España |
| Calendario fiscal 2027 | `/calendario-fiscal-autonomos-2027/` | `/ca/calendari-fiscal-autonoms-2027/` | Toda España salvo haciendas forales |
| IRPF de cada comunidad | `/calculadora-irpf-autonomos/{comunidad}/` | `/ca/calculadora-irpf-autonoms/{comunitat}/` | 14 páginas: la de Cataluña es la portada |
| Sueldo neto en cada comunidad | `/sueldo-neto-autonomo/{comunidad}/` | `/ca/sou-net-autonom/{comunitat}/` | 15 páginas |
| Calculadoras para otras webs | `/insertar/` | `/ca/inserir/` | Código para copiar y vista previa |

- **Sin servidor ni datos guardados:** el cálculo se hace en el navegador. No hay registro ni cookies.
- **Contador de visitas:** GoatCounter (cuenta `calculadoras-autonomos`, panel en https://calculadoras-autonomos.goatcounter.com), sin cookies ni datos personales. El script va con versión fija y huella SRI (`CONTADOR` en `herramientas/generar.py`) en todas las páginas menos las calculadoras para otras webs. Solo envía la dirección sin la parte de «#», así que los datos de los enlaces para compartir no salen del navegador.
- **Mismo cálculo que el servidor MCP:** las carpetas `irpf/`, `cuota/`, `factura/`, `modelo130/` y `modelo303/` son copias exactas de la compilación de `irpf-pymes-cat-mcp`. Si cambian las tablas, hay que compilar el servidor y volver a copiarlas.
- **Cálculos propios de la web:** `iva/`, `objetivo/`, `sueldo/`, `tarifa/` y `regularizacion/`. La tarifa plana sigue el art. 38 ter de la Ley 20/2007 y usa el importe de 2026 que publica la Seguridad Social (80 € más el MEI, 88,64 €) y el salario mínimo de 2026 y 2027 (RD 126/2026 y RD 1013/2026), revisados el 20 de noviembre de 2026. El modelo 130 sigue el art. 110 del Reglamento del IRPF y las instrucciones del modelo de la AEAT, revisados el 17 de noviembre de 2026.
- **Pruebas:** `node --test test/`.
- **Generador:** las páginas, el menú, las tarjetas y el sitemap salen de `herramientas/generar.py` (textos en `herramientas/contenido*.py`). Se ejecuta con `python -I herramientas/generar.py .` desde esta carpeta. Las tablas y los ejemplos de las páginas de cada comunidad salen de `herramientas/datos_comunidades.json`: si cambian las escalas o la cuota, primero hay que ejecutar `node herramientas/datos_comunidades.mjs`. Las páginas de IRPF y cuota se escribieron a mano: el generador solo actualiza sus partes comunes.
- **Imágenes para compartir:** `compartir/*.jpg` (1200 × 630) son las que se ven al pegar un enlace en WhatsApp, Telegram o redes. Salen de `herramientas/imagenes.py` (`python -I herramientas/imagenes.py .`, necesita Windows con Microsoft Edge) con el título de cada página; después hay que volver a ejecutar el generador. Si cambia un título, hay que volver a crearlas.
- **Enlace al servidor MCP:** las páginas ofrecen el servidor en MCPize, que tiene un plan gratuito.
- **Plantillas:** `plantillas/` sale de `herramientas/plantillas.py` (`python -I herramientas/plantillas.py .`). No llevan macros ni libro registro, para no ser un sistema de facturación sujeto a Verifactu.
- **Buscadores:** verificada en Google Search Console (meta `google-site-verification`) y en Bing Webmaster Tools (meta `msvalidate.01` y `BingSiteAuth.xml`), con el sitemap enviado a los dos. No hay que borrar esas etiquetas ni el archivo.
- **IndexNow:** cada publicación que cambia páginas avisa a Bing y otros buscadores con `.github/workflows/indexnow.yml` y la clave de la raíz (`*.txt` de 32 caracteres).
- **Afiliado de Quipu:** las calculadoras de IRPF (también las de cada comunidad), sueldo neto (también las de cada comunidad), factura, IVA, modelo 130, modelo 303, tarifa plana, el calendario y la plantilla muestran, justo debajo de la calculadora, un recuadro con un enlace de afiliado de Quipu (`?via=juli`, panel en quipu.getrewardful.com), marcado como tal. `/transparencia/` explica cómo se financia la web.
- **Compartir e imprimir:** `compartir.js` añade debajo de cada resultado los botones «Compartir» (si el navegador lo permite), «Copiar enlace» e «Imprimir o guardar en PDF». El enlace lleva los datos del formulario después de `#` (por ejemplo `#v=1&ingresos=40000&gastos=5000`), una parte que el navegador no envía al servidor; al abrirlo, el formulario se rellena solo. Al imprimir solo salen el formulario, el resultado y el aviso, con la fecha y el enlace.
- **Calendario para el móvil:** el generador crea `plazos-fiscales-2027.ics` y `ca/.../terminis-fiscals-2027.ics` con los 12 plazos de la tabla del calendario fiscal, cada uno con un aviso 5 días antes. Las fechas están en `FECHAS_CALENDARIO` (`herramientas/contenido_espana.py`), en el mismo orden que las filas. `.gitattributes` mantiene sus saltos de línea CRLF, como pide el estándar iCalendar. Se activa con `OFRECER_ICS` (`False` quita el botón y los archivos). Revisado con el Real Decreto-ley 43/2026: los plazos no cambian, y la página y los eventos de 2027 del 303 y el 130 avisan de las novedades (IVA anual y dispensa del modelo 130).
- **Regularización de la cuota:** `regularizacion/calculo.js` sigue el art. 308.1.c de la Ley General de la Seguridad Social: rendimiento neto del IRPF de 2026 más las cuotas pagadas, menos el 7 %, entre los meses de alta; si la cuota pagada queda por debajo de la mínima del tramo real se paga la diferencia, y si queda por encima de la máxima se devuelve. Supone la misma cuota todos los meses y excluye la tarifa plana, que no se regulariza (art. 38 ter.6 de la Ley 20/2007).
- **Calculadoras para otras webs:** `/insertar/irpf/` y `/insertar/sueldo/` (y sus versiones en catalán) son páginas mínimas, sin indexar, para ponerlas en un iframe. `widget.js` envía su altura a la página que las contiene, e `insertar.js` monta la vista previa y el código para copiar (un iframe, un enlace y una línea que ajusta la altura).
- **llms.txt:** el generador escribe `llms.txt`, un resumen de la web con todas sus calculadoras para asistentes de IA (formato de llmstxt.org).
- **Migas de pan:** todas las páginas menos la portada muestran dónde están (Inicio › IRPF por comunidad autónoma › Madrid) y lo repiten en datos estructurados `BreadcrumbList` para Google.

## Cómo se calcula

Los cálculos son funciones puras de JavaScript, sin red ni datos guardados, y redondean los importes a céntimos.

- **IRPF** (`irpf/calculo.js`, tablas en `irpf/tablas.js`):
  1. Rendimiento previo: ingresos − gastos deducibles − cuotas de autónomo.
  2. En estimación directa simplificada se restan los gastos de difícil justificación: en 2025, el 5 % del rendimiento previo positivo con un máximo de 2.000 € (art. 30.2.4.ª de la Ley del IRPF), y en 2026, el 10 % con un máximo de 3.000 € (Real Decreto-ley 43/2026, BOE del 25 de noviembre de 2026). No se aplican junto con la reducción del art. 32.2.1.º.
  3. Reducciones del art. 32.2 de la Ley del IRPF, sin dejar el rendimiento en negativo, suponiendo que no hay otras rentas.
  4. Reducción por inicio de actividad del 20 % (art. 32.3), sobre un máximo de 100.000 €.
  5. A la base se le aplican la escala estatal y la de la comunidad. A cada cuota se le resta la misma escala aplicada al mínimo personal y familiar: el estatal en la parte estatal y el de la comunidad en la autonómica. Las escalas y los mínimos son los del Manual de Renta 2025 de la Agencia Tributaria, con los cambios de 2026 que recoge el informe de Hacienda sobre la tributación autonómica.
- **Cuota de autónomos** (`cuota/calculo.js`): rendimiento computable del art. 308 de la Ley General de la Seguridad Social, con la deducción del 7 % por gastos genéricos, dividido entre 12. Con ese rendimiento mensual se busca el tramo de la Orden PJC/297/2026 y la cuota es la base mínima del tramo por el 31,5 %. Se repite hasta que la cuota no cambia, porque en la estimación simplificada los gastos de difícil justificación (los de 2026: 10 %, máximo 3.000 €) dependen de las propias cuotas.
- **Sueldo neto** (`sueldo/calculo.js`): ingresos − gastos − cuota anual − IRPF del año, dividido entre 12.
- **Cuánto facturar** (`objetivo/calculo.js`): la calculadora de sueldo neto al revés, por bisección, redondeando hacia arriba al céntimo.
- **Tarifa plana** (`tarifa/calculo.js`): 88,64 € al mes durante 12 meses, y otros 12 si el rendimiento computable, menos el 7 %, es inferior al salario mínimo del año (art. 38 ter de la Ley 20/2007).
- **Modelos 130 y 303, factura e IVA:** `modelo130/`, `modelo303/`, `factura/` e `iva/`, con los tipos vigentes en 2026. En el modelo 130, el cuarto trimestre de 2026 usa ya el 10 % de difícil justificación con un máximo de 3.000 €, como dice el Real Decreto-ley 43/2026.

**Cómo se comprueba:** `node --test test/` prueba casos calculados a mano con las tablas del BOE y de la Agencia Tributaria. Antes de publicar un cambio de cifras, además, se comparan miles de casos con una implementación independiente y se revisa la web publicada.

**Qué no incluye:** deducciones autonómicas, otras rentas (sueldos, alquileres), tributación conjunta ni las haciendas forales del País Vasco y Navarra.

## Licencia

El código es software libre con [licencia MIT](LICENSE): puedes usarlo, copiarlo y modificarlo, también en proyectos comerciales, manteniendo el aviso de copyright. Si usas estos cálculos en tu web o proyecto, se agradece un enlace a <https://calculadorasautonomos.es/>.

Son estimaciones orientativas y no sustituyen a un asesor fiscal.
