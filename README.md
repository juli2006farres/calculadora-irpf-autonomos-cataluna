# Calculadoras para autónomos

Web estática y gratuita con calculadoras para autónomos, en castellano y en catalán. Se publica con GitHub Pages en <https://juli2006farres.github.io/calculadora-irpf-autonomos-cataluna/>.

| Calculadora | Castellano | Catalán | Ámbito |
|---|---|---|---|
| IRPF por comunidad autónoma | `/calculadora-irpf-autonomos/` | `/ca/calculadora-irpf-autonoms/` | 15 comunidades de régimen común, 2025 y 2026 |
| IRPF de autónomos | `/` | `/ca/` | Cataluña, 2025 y 2026 |
| Cuota de autónomos 2026 | `/cuota-autonomos-2026/` | `/ca/quota-autonoms-2026/` | Toda España |
| Tarifa plana 2026 | `/tarifa-plana-autonomos-2026/` | `/ca/tarifa-plana-autonoms-2026/` | Toda España |
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

- **Sin servidor ni datos guardados:** el cálculo se hace en el navegador. No hay registro, cookies ni analítica.
- **Mismo cálculo que el servidor MCP:** las carpetas `irpf/`, `cuota/`, `factura/`, `modelo130/` y `modelo303/` son copias exactas de la compilación de `irpf-pymes-cat-mcp`. Si cambian las tablas, hay que compilar el servidor y volver a copiarlas.
- **Cálculos propios de la web:** `iva/`, `objetivo/`, `sueldo/` y `tarifa/`. La tarifa plana sigue el art. 38 ter de la Ley 20/2007 y usa el importe de 2026 que publica la Seguridad Social (80 € más el MEI, 88,64 €) y el salario mínimo de 2026 y 2027 (RD 126/2026 y RD 1013/2026), revisados el 20 de noviembre de 2026. El modelo 130 sigue el art. 110 del Reglamento del IRPF y las instrucciones del modelo de la AEAT, revisados el 17 de noviembre de 2026.
- **Pruebas:** `node --test test/`.
- **Generador:** las páginas, el menú, las tarjetas y el sitemap salen de `herramientas/generar.py` (textos en `herramientas/contenido*.py`). Se ejecuta con `python -I herramientas/generar.py .` desde esta carpeta. Las tablas y los ejemplos de las páginas de cada comunidad salen de `herramientas/datos_comunidades.json`: si cambian las escalas o la cuota, primero hay que ejecutar `node herramientas/datos_comunidades.mjs`. Las páginas de IRPF y cuota se escribieron a mano: el generador solo actualiza sus partes comunes.
- **Imágenes para compartir:** `compartir/*.jpg` (1200 × 630) son las que se ven al pegar un enlace en WhatsApp, Telegram o redes. Salen de `herramientas/imagenes.py` (`python -I herramientas/imagenes.py .`, necesita Windows con Microsoft Edge) con el título de cada página; después hay que volver a ejecutar el generador. Si cambia un título, hay que volver a crearlas.
- **Enlace al servidor MCP:** las páginas ofrecen el servidor en MCPize, que tiene un plan gratuito.
- **Plantillas:** `plantillas/` sale de `herramientas/plantillas.py` (`python -I herramientas/plantillas.py .`). No llevan macros ni libro registro, para no ser un sistema de facturación sujeto a Verifactu.
- **Buscadores:** verificada en Google Search Console (meta `google-site-verification`) y en Bing Webmaster Tools (meta `msvalidate.01` y `BingSiteAuth.xml`), con el sitemap enviado a los dos. No hay que borrar esas etiquetas ni el archivo.
- **IndexNow:** cada publicación que cambia páginas avisa a Bing y otros buscadores con `.github/workflows/indexnow.yml` y la clave de la raíz (`*.txt` de 32 caracteres).
- **Afiliado de Quipu:** las calculadoras de factura, IVA, modelo 130, modelo 303, tarifa plana, el calendario y la plantilla muestran un recuadro con un enlace de afiliado de Quipu (`?via=juli`, panel en quipu.getrewardful.com), marcado como tal. `/transparencia/` explica cómo se financia la web.

Son estimaciones orientativas y no sustituyen a un asesor fiscal.
