# Calculadoras para autónomos

Web estática y gratuita con calculadoras para autónomos, en castellano y en catalán. Se publica con GitHub Pages en <https://juli2006farres.github.io/calculadora-irpf-autonomos-cataluna/>.

| Calculadora | Castellano | Catalán | Ámbito |
|---|---|---|---|
| IRPF por comunidad autónoma | `/calculadora-irpf-autonomos/` | `/ca/calculadora-irpf-autonoms/` | 15 comunidades de régimen común, 2025 y 2026 |
| IRPF de autónomos | `/` | `/ca/` | Cataluña, 2025 y 2026 |
| Cuota de autónomos 2026 | `/cuota-autonomos-2026/` | `/ca/quota-autonoms-2026/` | Toda España |
| Factura con IVA e IRPF | `/factura-autonomos/` | `/ca/factura-autonoms/` | Toda España |
| IVA: añadir o quitar | `/calculadora-iva/` | `/ca/calculadora-iva/` | Toda España salvo Canarias, Ceuta y Melilla |
| Sueldo neto de autónomo | `/sueldo-neto-autonomo/` | `/ca/sou-net-autonom/` | 15 comunidades, 2026 |
| Cuánto facturar para un neto | `/cuanto-facturar-autonomo/` | `/ca/quant-facturar-autonom/` | 15 comunidades, 2026 |
| Modelo 130 | `/modelo-130/` | `/ca/model-130/` | Toda España salvo País Vasco y Navarra |
| Modelo 303 | `/modelo-303/` | `/ca/model-303/` | Toda España salvo Canarias, Ceuta, Melilla, País Vasco y Navarra |
| Plantilla de factura (Excel y Word) | `/plantilla-factura-autonomo/` | `/ca/plantilla-factura-autonom/` | Toda España |
| Calendario fiscal 2027 | `/calendario-fiscal-autonomos-2027/` | `/ca/calendari-fiscal-autonoms-2027/` | Toda España salvo haciendas forales |

- **Sin servidor ni datos guardados:** el cálculo se hace en el navegador. No hay registro, cookies ni analítica.
- **Mismo cálculo que el servidor MCP:** las carpetas `irpf/`, `cuota/`, `factura/`, `modelo130/` y `modelo303/` son copias exactas de la compilación de `irpf-pymes-cat-mcp`. Si cambian las tablas, hay que compilar el servidor y volver a copiarlas.
- **Cálculos propios de la web:** `iva/`, `objetivo/` y `sueldo/`. El modelo 130 sigue el art. 110 del Reglamento del IRPF y las instrucciones del modelo de la AEAT, revisados el 17 de noviembre de 2026.
- **Pruebas:** `node --test test/`.
- **Generador:** las páginas, el menú, las tarjetas y el sitemap salen de `herramientas/generar.py` (textos en `herramientas/contenido*.py`). Se ejecuta con `python -I herramientas/generar.py .` desde esta carpeta. Las páginas de IRPF y cuota se escribieron a mano: el generador solo actualiza sus partes comunes.
- **Enlace al servidor MCP:** las páginas ofrecen el servidor en MCPize, que tiene un plan gratuito.
- **Plantillas:** `plantillas/` sale de `herramientas/plantillas.py` (`python -I herramientas/plantillas.py .`). No llevan macros ni libro registro, para no ser un sistema de facturación sujeto a Verifactu.
- **Buscadores:** verificada en Google Search Console (meta `google-site-verification`) y en Bing Webmaster Tools (meta `msvalidate.01` y `BingSiteAuth.xml`), con el sitemap enviado a los dos. No hay que borrar esas etiquetas ni el archivo.
- **IndexNow:** cada publicación que cambia páginas avisa a Bing y otros buscadores con `.github/workflows/indexnow.yml` y la clave de la raíz (`*.txt` de 32 caracteres).
- **Afiliado de Quipu:** las calculadoras de factura, IVA, modelo 130, modelo 303 y la plantilla muestran un recuadro con un enlace de afiliado de Quipu (`?via=juli`, panel en quipu.getrewardful.com), marcado como tal. `/transparencia/` explica cómo se financia la web.

Son estimaciones orientativas y no sustituyen a un asesor fiscal.
