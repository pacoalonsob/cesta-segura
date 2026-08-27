# -*- coding: utf-8 -*-
"""
Crea la base de datos SQLite del prototipo a partir de seed_data.py
y exporta también un products.json (para el buscador web de demo).

Uso:
    python3 build_db.py
"""
import sqlite3
import json
import datetime
from pathlib import Path
from seed_data import PRODUCTS

DB_PATH = Path(__file__).parent / "products.db"
JSON_PATH = Path(__file__).parent / "products.json"

SCHEMA = """
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supermercado TEXT NOT NULL,
    nombre TEXT NOT NULL,
    marca TEXT,
    precio_eur REAL,
    precio_unidad TEXT,
    formato TEXT,
    sin_gluten INTEGER,        -- 1 = sí, 0 = no, NULL = no declarado
    sin_lactosa INTEGER,       -- 1 = sí, 0 = no, NULL = no declarado
    alergenos TEXT,
    ingredientes TEXT,
    url TEXT UNIQUE,
    notas TEXT,
    fecha_actualizacion TEXT
);

CREATE INDEX IF NOT EXISTS idx_supermercado ON productos(supermercado);
CREATE INDEX IF NOT EXISTS idx_marca ON productos(marca);
CREATE INDEX IF NOT EXISTS idx_sin_gluten ON productos(sin_gluten);
CREATE INDEX IF NOT EXISTS idx_sin_lactosa ON productos(sin_lactosa);
"""


def to_flag(v):
    if v is True:
        return 1
    if v is False:
        return 0
    return None


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    now = datetime.date.today().isoformat()

    rows = []
    for p in PRODUCTS:
        rows.append((
            p["supermercado"], p["nombre"], p["marca"], p["precio_eur"],
            p["precio_unidad"], p["formato"], to_flag(p["sin_gluten"]),
            to_flag(p["sin_lactosa"]), p["alergenos"], p["ingredientes"],
            p["url"], p["notas"], now,
        ))

    conn.executemany("""
        INSERT INTO productos
        (supermercado, nombre, marca, precio_eur, precio_unidad, formato,
         sin_gluten, sin_lactosa, alergenos, ingredientes, url, notas, fecha_actualizacion)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(url) DO UPDATE SET
            precio_eur=excluded.precio_eur,
            precio_unidad=excluded.precio_unidad,
            sin_gluten=excluded.sin_gluten,
            sin_lactosa=excluded.sin_lactosa,
            alergenos=excluded.alergenos,
            ingredientes=excluded.ingredientes,
            notas=excluded.notas,
            fecha_actualizacion=excluded.fecha_actualizacion
    """, rows)
    conn.commit()

    cur = conn.execute("SELECT COUNT(*) FROM productos")
    total = cur.fetchone()[0]
    print(f"Base de datos creada/actualizada: {DB_PATH} ({total} productos)")

    # Export a JSON plano para el front-end de demo
    cur = conn.execute("""
        SELECT supermercado, nombre, marca, precio_eur, precio_unidad, formato,
               sin_gluten, sin_lactosa, alergenos, ingredientes, url, notas, fecha_actualizacion
        FROM productos ORDER BY nombre
    """)
    cols = [d[0] for d in cur.description]
    data = [dict(zip(cols, row)) for row in cur.fetchall()]
    JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Export JSON: {JSON_PATH}")

    conn.close()


if __name__ == "__main__":
    main()
