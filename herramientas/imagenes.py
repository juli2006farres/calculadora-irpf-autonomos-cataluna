"""Crea las imágenes que se ven al compartir un enlace (WhatsApp, Telegram, redes): una por página.

Usa el título (h1) de cada página y el icono de su calculadora, y las dibuja con Microsoft Edge
en modo sin ventana, así que solo funciona en Windows. Uso, desde la carpeta de la web y después
de generar las páginas:
    python -I herramientas/imagenes.py .
Escribe compartir/*.jpg. Luego hay que volver a ejecutar generar.py para que las páginas las enlacen.
"""
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

WEB = Path(sys.argv[1]).resolve()
sys.argv = [sys.argv[0], str(WEB)]
sys.path.insert(0, str(Path(__file__).parent))
import generar  # noqa: E402
from contenido_comunidades import PADRE_COMUNIDADES, RUTAS_COMUNIDADES  # noqa: E402

EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
SALIDA = WEB / "compartir"
CHIPS = {"es": ["Gratis", "Sin registro", "Datos oficiales"], "ca": ["Gratuït", "Sense registre", "Dades oficials"]}

PLANTILLA = """<!doctype html><html><head><meta charset="utf-8"><style>
* {{ margin: 0; box-sizing: border-box; }}
html, body {{ width: 1200px; height: 630px; overflow: hidden; }}
body {{ font-family: "Segoe UI", Arial, sans-serif; color: #fff; position: relative;
  background: linear-gradient(135deg, #1b64a0 0%, #1d7a7a 55%, #1f8a5b 100%); }}
.b1, .b2 {{ position: absolute; border-radius: 50%; }}
.b1 {{ width: 560px; height: 560px; right: -160px; top: -230px; background: radial-gradient(circle, rgba(255,255,255,.20), transparent 70%); }}
.b2 {{ width: 460px; height: 460px; left: 360px; bottom: -300px; background: radial-gradient(circle, rgba(255,255,255,.14), transparent 70%); }}
.marca {{ position: absolute; left: 72px; top: 62px; display: flex; align-items: center; gap: 18px; font-size: 30px; font-weight: 700; }}
.logo {{ width: 58px; height: 58px; border-radius: 16px; background: #fff; color: #1b64a0; display: grid; place-items: center; font-size: 34px; font-weight: 800; }}
h1 {{ position: absolute; left: 72px; top: 160px; width: 740px; font-size: 66px; line-height: 1.08; font-weight: 800; letter-spacing: -1.5px; }}
.chips {{ position: absolute; left: 72px; bottom: 62px; display: flex; gap: 14px; }}
.chips span {{ background: rgba(255,255,255,.16); border: 1.5px solid rgba(255,255,255,.4); border-radius: 999px; padding: 9px 22px; font-size: 25px; font-weight: 600; }}
.icono {{ position: absolute; right: 92px; top: 175px; width: 260px; height: 260px; border-radius: 64px; background: #fff;
  display: grid; place-items: center; color: #1b64a0; box-shadow: 0 30px 70px rgba(0,0,0,.22); }}
.icono svg {{ width: 150px; height: 150px; stroke-width: 1.6; }}
</style></head><body>
<div class="b1"></div><div class="b2"></div>
<div class="marca"><span class="logo">€</span>{marca}</div>
<h1 id="t">{titulo}</h1>
<div class="chips">{chips}</div>
<div class="icono">{icono}</div>
<script>
  // Reduce la letra hasta que el título quepa entre la marca y las etiquetas.
  const t = document.getElementById("t");
  let tam = 66;
  while (t.scrollHeight > 300 && tam > 30) {{ tam -= 2; t.style.fontSize = tam + "px"; }}
</script>
</body></html>"""


def nombre_imagen(ruta, extension=".png"):
    return (ruta.strip("/").replace("/", "-") or "inicio") + extension


def main():
    if not EDGE.exists():
        raise SystemExit(f"No se encuentra Microsoft Edge en {EDGE}")
    SALIDA.mkdir(exist_ok=True)
    rutas = dict(generar.RUTAS)
    rutas.update(RUTAS_COMUNIDADES)
    hechas = 0
    with tempfile.TemporaryDirectory() as tmp:
        for clave, por_idioma in rutas.items():
            if clave == "transparencia":
                continue
            icono = generar.ICONOS[PADRE_COMUNIDADES.get(clave, clave)]
            for lang, ruta in por_idioma.items():
                pagina = WEB / ruta / "index.html"
                h1 = re.search(r"<h1>(.*?)</h1>", pagina.read_text(encoding="utf-8"), re.S)
                titulo = html.escape(html.unescape(re.sub(r"<[^>]+>", "", h1.group(1))).strip())
                documento = PLANTILLA.format(
                    marca=generar.T[lang]["marca"], titulo=titulo,
                    chips="".join(f"<span>✓ {c}</span>" for c in CHIPS[lang]), icono=icono,
                )
                origen = Path(tmp) / "tarjeta.html"
                origen.write_text(documento, encoding="utf-8")
                destino = SALIDA / nombre_imagen(ruta)
                subprocess.run(
                    [str(EDGE), "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                     "--window-size=1200,630", f"--screenshot={destino}", origen.as_uri()],
                    check=True, capture_output=True, timeout=60,
                )
                hechas += 1
    a_jpg()
    print(f"{hechas} imágenes en {SALIDA}")


# Las capturas salen en PNG y pesan unos 360 KB; en JPG de calidad 88 pesan unas diez veces menos,
# que es lo que conviene para WhatsApp y las redes. Se convierten con la librería de imágenes de Windows.
CONVERTIR = r"""
Add-Type -AssemblyName System.Drawing
$codec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' }
$parametros = New-Object System.Drawing.Imaging.EncoderParameters 1
$parametros.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter ([System.Drawing.Imaging.Encoder]::Quality), 88L
Get-ChildItem -LiteralPath $args[0] -Filter *.png | ForEach-Object {
  $imagen = [System.Drawing.Image]::FromFile($_.FullName)
  $imagen.Save([System.IO.Path]::ChangeExtension($_.FullName, '.jpg'), $codec, $parametros)
  $imagen.Dispose()
  Remove-Item -LiteralPath $_.FullName
}
"""


def a_jpg():
    with tempfile.TemporaryDirectory() as tmp:
        script = Path(tmp) / "a_jpg.ps1"
        script.write_text(CONVERTIR, encoding="utf-8-sig")
        subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script), str(SALIDA)],
                       check=True, capture_output=True, timeout=300)


if __name__ == "__main__":
    main()
