# Calculadoras para autónomos

Web estática y gratuita con calculadoras para autónomos, en castellano y en catalán. Se publica con GitHub Pages en <https://juli2006farres.github.io/calculadora-irpf-autonomos-cataluna/>.

| Calculadora | Castellano | Catalán | Ámbito |
|---|---|---|---|
| IRPF de autónomos | `/` | `/ca/` | Cataluña, 2025 y 2026 |
| Cuota de autónomos 2026 | `/cuota-autonomos-2026/` | `/ca/quota-autonoms-2026/` | Toda España |
| Factura con IVA e IRPF | `/factura-autonomos/` | `/ca/factura-autonoms/` | Toda España |
| IVA: añadir o quitar | `/calculadora-iva/` | `/ca/calculadora-iva/` | Toda España salvo Canarias, Ceuta y Melilla |
| Sueldo neto de autónomo | `/sueldo-neto-autonomo/` | `/ca/sou-net-autonom/` | Cataluña, 2026 |
| Cuánto facturar para un neto | `/cuanto-facturar-autonomo/` | `/ca/quant-facturar-autonom/` | Cataluña, 2026 |
| Modelo 130 | `/modelo-130/` | `/ca/model-130/` | Toda España salvo País Vasco y Navarra |

- **Sin servidor ni datos guardados:** el cálculo se hace en el navegador. No hay registro, cookies ni analítica.
- **Mismo cálculo que el servidor MCP:** las carpetas `irpf/`, `cuota/`, `factura/` y `modelo130/` son copias exactas de la compilación de `irpf-pymes-cat-mcp`. Si cambian las tablas, hay que compilar el servidor y volver a copiarlas.
- **Cálculos propios de la web:** `iva/`, `objetivo/` y `sueldo/`. El modelo 130 sigue el art. 110 del Reglamento del IRPF y las instrucciones del modelo de la AEAT, revisados el 17 de noviembre de 2026.
- **Pruebas:** `node --test test/`.
- **Generador:** las páginas, el menú, las tarjetas y el sitemap salen de `herramientas/generar.py` (textos en `herramientas/contenido*.py`). Se ejecuta con `python -I herramientas/generar.py .` desde esta carpeta. Las páginas de IRPF y cuota se escribieron a mano: el generador solo actualiza sus partes comunes.
- **Enlace al servidor MCP:** las páginas ofrecen el servidor en MCPize, que tiene un plan gratuito.

Son estimaciones orientativas y no sustituyen a un asesor fiscal.
