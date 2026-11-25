"""Avisa a IndexNow (Bing, Yandex, Seznam...) de todas las URL del sitemap.

Lo ejecuta GitHub Actions después de cada publicación. Espera a que GitHub Pages sirva el archivo de
la clave y las páginas nuevas, y después envía la lista de URL. Uso: python3 herramientas/indexnow.py
"""
import glob
import json
import re
import sys
import time
import urllib.request

BASE = "https://calculadorasautonomos.es/"
claves = [f[:-4] for f in glob.glob("*.txt") if re.fullmatch(r"[0-9a-f]{32}\.txt", f)]
if len(claves) != 1:
    sys.exit("Debe haber exactamente un archivo de clave de IndexNow en la raíz")
clave = claves[0]
urls = re.findall(r"<loc>(.*?)</loc>", open("sitemap.xml", encoding="utf-8").read())


def leer(url):
    with urllib.request.urlopen(url, timeout=20) as r:
        return r.read().decode("utf-8", "replace")


# Espera hasta 10 minutos a que GitHub Pages publique la versión nueva.
for intento in range(30):
    try:
        if leer(f"{BASE}{clave}.txt?n={intento}").strip() == clave and all(leer(f"{u}?n={intento}") for u in urls[-2:]):
            break
    except Exception:
        pass
    time.sleep(20)
else:
    sys.exit("GitHub Pages no ha publicado la clave a tiempo")

cuerpo = json.dumps({
    "host": "calculadorasautonomos.es",
    "key": clave,
    "keyLocation": f"{BASE}{clave}.txt",
    "urlList": urls,
}).encode("utf-8")
peticion = urllib.request.Request(
    "https://api.indexnow.org/indexnow", data=cuerpo, headers={"Content-Type": "application/json; charset=utf-8"}
)
with urllib.request.urlopen(peticion, timeout=30) as r:
    print("IndexNow respondió", r.status, "con", len(urls), "URL")
