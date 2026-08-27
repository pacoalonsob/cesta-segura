# -*- coding: utf-8 -*-
"""
Scraper de producción para carrefour.es — extrae productos etiquetados
"sin gluten" y/o "sin lactosa" a partir de los sitemaps públicos del sitio.

IMPORTANTE — dónde ejecutar esto:
Este script necesita salida a internet real hacia www.carrefour.es. NO se
puede ejecutar dentro de este sandbox de Claude (su red saliente está
restringida a un proxy controlado, no a dominios arbitrarios). Debe
correr en tu propio servidor, una función en la nube (Cloud Run, un VPS
barato, GitHub Actions con cron, etc.) con acceso normal a internet.

Respeta robots.txt:
- Permitido: fichas de producto /supermercado/<slug>/R-<id>/p
- Bloqueado: /buscador/, /myaccount/*, carrito, checkout, valoraciones
Este script solo usa las rutas de sitemap y de ficha de producto, que
están permitidas. Aun así, incluye rate limiting para no sobrecargar su
servidor — sé buen ciudadano aunque esté permitido.

Instalación:
    pip install requests beautifulsoup4 lxml

Uso:
    python3 scraper_carrefour.py --out productos_carrefour.json
"""
import argparse
import json
import re
import time
import sys
from datetime import date

import requests
from bs4 import BeautifulSoup

BASE = "https://www.carrefour.es"
SITEMAP_INDEX = f"{BASE}/crs/cdn-static/sitemap-food/index.xml"
HEADERS = {
    # Carrefour (Akamai u otra CDN anti-bot por delante) devuelve 403 a
    # clientes que no parecen un navegador real, incluidas muchas IPs de
    # datacenter (como las de GitHub Actions). Un User-Agent de navegador
    # normal + cabeceras Accept habituales evita el bloqueo mas basico;
    # si el bloqueo es por reputacion de IP (no solo por cabeceras), esto
    # no bastara y hara falta otro host/IP (ver notas mas abajo).
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9",
}
RATE_LIMIT_SECONDS = 1.5  # margen prudente entre peticiones a fichas de producto
KEYWORDS = ["sin-gluten", "sin-lactosa", "no-gluten"]


def get(url, **kw):
    r = requests.get(url, headers=HEADERS, timeout=20, **kw)
    r.raise_for_status()
    return r


def discover_product_sitemaps():
    xml = get(SITEMAP_INDEX).text
    return re.findall(r"<loc>(.*?)</loc>", xml)


def discover_candidate_urls(sitemap_url):
    xml = get(sitemap_url).text
    locs = re.findall(r"<loc>(.*?)</loc>", xml)
    return [u for u in locs if any(k in u for k in KEYWORDS)]


def parse_product(url):
    """Extrae los campos relevantes de una ficha de producto.

    NOTA: la estructura HTML real de carrefour.es puede cambiar y este
    parser probablemente necesite ajustes con selectores CSS reales
    (aquí se deja un esqueleto con heurísticas de texto porque este
    entorno no puede inspeccionar el HTML/JS renderizado en vivo).
    Antes de usarlo en producción: abre una ficha de producto en el
    navegador, inspecciona el HTML real y ajusta los selectores.
    """
    html = get(url).text
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(" ", strip=True)

    def find_price():
        m = re.search(r"(\d+,\d{2})\s*€", text)
        return float(m.group(1).replace(",", ".")) if m else None

    nombre = soup.title.get_text(strip=True) if soup.title else None

    sin_gluten = "sin gluten" in text.lower() or "no gluten" in text.lower()
    sin_lactosa = "sin lactosa" in text.lower()
    contains_gluten_allergen = bool(
        re.search(r"contiene[^.]*gluten", text.lower())
    )

    return {
        "supermercado": "Carrefour",
        "nombre": nombre,
        "precio_eur": find_price(),
        "sin_gluten_declarado": sin_gluten,
        "sin_lactosa_declarado": sin_lactosa,
        # señal de alerta: la propia ficha se contradice (pasa en la práctica,
        # ver ejemplo real en seed_data.py)
        "posible_contradiccion_gluten": sin_gluten and contains_gluten_allergen,
        "url": url,
        "fecha_actualizacion": date.today().isoformat(),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="productos_carrefour.json")
    ap.add_argument("--limit", type=int, default=None,
                     help="límite de productos a procesar (para pruebas)")
    args = ap.parse_args()

    print("Descubriendo sub-sitemaps de alimentación...", file=sys.stderr)
    sub_sitemaps = [u for u in discover_product_sitemaps() if "products" in u]

    candidate_urls = []
    for sm in sub_sitemaps:
        print(f"  Leyendo {sm}", file=sys.stderr)
        candidate_urls.extend(discover_candidate_urls(sm))
        time.sleep(RATE_LIMIT_SECONDS)

    candidate_urls = sorted(set(candidate_urls))
    print(f"{len(candidate_urls)} productos candidatos encontrados", file=sys.stderr)

    if args.limit:
        candidate_urls = candidate_urls[: args.limit]

    results = []
    for i, url in enumerate(candidate_urls, 1):
        try:
            results.append(parse_product(url))
        except Exception as e:
            print(f"  [WARN] fallo en {url}: {e}", file=sys.stderr)
        if i % 10 == 0:
            print(f"  {i}/{len(candidate_urls)}", file=sys.stderr)
        time.sleep(RATE_LIMIT_SECONDS)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Guardado {args.out} ({len(results)} productos)", file=sys.stderr)


if __name__ == "__main__":
    main()
