# Cesta Segura

Buscador de productos sin gluten y sin lactosa en supermercados de Espana, empezando por Carrefour.

## Por que Carrefour primero

Se comprobo el robots.txt de Mercadona, Carrefour y Dia:

- **Mercadona** bloquea el acceso automatizado a practicamente todo el sitio, incluida su propia API interna. No se scrapea.
- **Dia** bloquea las paginas de producto en general (incluida la seccion de "sin gluten").
- **Carrefour** permite explicitamente el acceso a las fichas de producto (`/supermercado/<slug>/R-<id>/p`). Es el punto de partida.

## Estado actual

- `seed_data.py` / `build_db.py`: datos de muestra (8 productos) recogidos a mano, para el prototipo de busqueda.
- `scraper_carrefour.py`: scraper de produccion que recorre los sitemaps publicos de Carrefour y extrae productos etiquetados "sin gluten" / "sin lactosa". Pensado para ejecutarse via GitHub Actions (ver `.github/workflows/scrape.yml`), ya que necesita salida real a internet.
- El workflow de Actions se ha dejado en modo **manual** (`workflow_dispatch`) a proposito: antes de programarlo para que corra solo, hay que lanzarlo una vez, revisar que el resultado (`productos_carrefour.json`) tiene sentido, y solo entonces pasar a un cron automatico.

## Siguiente paso

Ir a la pestana "Actions" de este repositorio, elegir el workflow "Scraper Carrefour (prueba manual)" y ejecutarlo con un limite bajo (ej. 15) para comprobar que funciona antes de escalarlo.
