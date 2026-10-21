"""Dibuja el diagrama del modelo relacional de olist.duckdb (Módulo 0).

Las filas y cardinalidades provienen de sql/00_datos/llaves_unicidad.sql y
sql/00_datos/cardinalidad_relaciones.sql.

Uso:
    uv run python scripts/diagrama_relacional.py
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from olist.config import FIG_DIR, PROJECT_ROOT

ANCHO = 3.45  # ancho de cada tabla
COL = (0.3, 4.65, 9.0, 13.35)  # x de cada columna de tablas
ALTO_TITULO = 0.55
ALTO_CAMPO = 0.37
AZUL = "#1F4E79"
GRIS = "#555555"
LINEA = "#4A4A4A"

# nombre: (x, y_superior, filas, [(marca, campo)])
TABLAS = {
    "customers": (COL[0], 10.0, "99.441", [
        ("PK", "customer_id"), ("", "customer_unique_id (persona)"),
        ("", "customer_zip_code_prefix"), ("", "customer_city"), ("", "customer_state")]),
    "geolocation": (COL[0], 4.6, "1.000.163", [
        ("", "geolocation_zip_code_prefix"), ("", "  (19.015 prefijos: no es única)"),
        ("", "geolocation_lat / _lng"), ("", "geolocation_city"), ("", "geolocation_state")]),
    "orders": (COL[1], 10.0, "99.441", [
        ("PK", "order_id"), ("FK", "customer_id"), ("", "order_status"),
        ("", "order_purchase_timestamp"), ("", "order_approved_at"),
        ("", "order_delivered_carrier_date"), ("", "order_delivered_customer_date"),
        ("", "order_estimated_delivery_date")]),
    "order_payments": (COL[1], 5.5, "103.886", [
        ("PK FK", "order_id"), ("PK", "payment_sequential"), ("", "payment_type"),
        ("", "payment_installments"), ("", "payment_value")]),
    "order_reviews": (COL[1], 2.7, "99.224", [
        ("PK", "review_id"), ("PK FK", "order_id"), ("", "review_score"),
        ("", "review_comment_title, _message"), ("", "review_creation_date")]),
    "order_items": (COL[2], 10.0, "112.650", [
        ("PK FK", "order_id"), ("PK", "order_item_id"), ("FK", "product_id"),
        ("FK", "seller_id"), ("", "shipping_limit_date"), ("", "price"), ("", "freight_value")]),
    "sellers": (COL[2], 5.5, "3.095", [
        ("PK", "seller_id"), ("", "seller_zip_code_prefix"), ("", "seller_city"),
        ("", "seller_state")]),
    "products": (COL[3], 10.0, "32.951", [
        ("PK", "product_id"), ("FK", "product_category_name"),
        ("", "peso y dimensiones"), ("", "product_photos_qty")]),
    "category_translation": (COL[3], 6.9, "71", [
        ("PK", "product_category_name"), ("", "product_category_name_english")]),
}


def caja(ax, nombre, x, y, filas, campos):
    alto = ALTO_TITULO + ALTO_CAMPO * len(campos) + 0.12
    ax.add_patch(FancyBboxPatch((x, y - alto), ANCHO, alto, boxstyle="round,pad=0,rounding_size=0.08",
                                fc="white", ec=AZUL, lw=1.4, zorder=3))
    ax.add_patch(FancyBboxPatch((x, y - ALTO_TITULO), ANCHO, ALTO_TITULO,
                                boxstyle="round,pad=0,rounding_size=0.08", fc=AZUL, ec=AZUL, zorder=4))
    ax.text(x + 0.12, y - ALTO_TITULO / 2, nombre, color="white", fontsize=10.5, weight="bold",
            va="center", zorder=5)
    ax.text(x + ANCHO - 0.12, y - ALTO_TITULO / 2, f"{filas} filas", color="white", fontsize=8,
            va="center", ha="right", zorder=5)
    for i, (marca, campo) in enumerate(campos):
        yc = y - ALTO_TITULO - ALTO_CAMPO * (i + 0.5) - 0.06
        ax.text(x + 0.12, yc, marca, fontsize=7.2, weight="bold", color="#9C2A2A", va="center", zorder=5)
        ax.text(x + 0.62, yc, campo, fontsize=8.3, va="center", zorder=5,
                weight="bold" if "PK" in marca else "normal")
    return y - alto


def conector(ax, puntos, etiqueta, pos_etiqueta, ha="center"):
    xs, ys = zip(*puntos)
    ax.plot(xs, ys, color=LINEA, lw=1.3, zorder=2, solid_joinstyle="round")
    ax.text(*pos_etiqueta, etiqueta, fontsize=8, ha=ha, va="center", color="#222222", zorder=6,
            bbox=dict(boxstyle="round,pad=0.18", fc="#FFF4E5", ec="#E8A33D", lw=0.8))


def main() -> None:
    fig, ax = plt.subplots(figsize=(16.8, 10.4))
    ax.set_xlim(0, 17.0)
    ax.set_ylim(-0.6, 10.3)
    ax.axis("off")

    fondo = {n: caja(ax, n, x, y, f, c) for n, (x, y, f, c) in TABLAS.items()}

    a, b, c, d = COL
    m = ANCHO / 2
    # customers 1:1 orders (customer_id es único por orden)
    conector(ax, [(a + ANCHO, 9.2), (b, 9.2)], "1 : 1", ((a + ANCHO + b) / 2, 9.55))
    # orders 1:N order_items
    conector(ax, [(b + ANCHO, 9.2), (c, 9.2)], "1 : 0..21", ((b + ANCHO + c) / 2, 9.55))
    # order_items N:1 products
    conector(ax, [(c + ANCHO, 9.2), (d, 9.2)], "N : 1", ((c + ANCHO + d) / 2, 9.55))
    # products N:0..1 category_translation (13 productos de 2 categorías sin traducción)
    conector(ax, [(d + m, fondo["products"]), (d + m, 6.9)], "N : 0..1", (d + m + 0.75, 7.45))
    # order_items N:1 sellers
    conector(ax, [(c + m, fondo["order_items"]), (c + m, 5.5)], "N : 1", (c + m + 0.55, 6.2))
    # orders 1:N order_payments
    conector(ax, [(b + m, fondo["orders"]), (b + m, 5.5)], "1 : 0..29", (b + m + 0.75, 5.95))
    # orders 1:N order_reviews (rodea order_payments por la derecha)
    x_ret = b + ANCHO + 0.45
    conector(ax, [(b + ANCHO, 6.75), (x_ret, 6.75), (x_ret, 1.4), (b + ANCHO, 1.4)], "1 : 0..3", (x_ret, 2.2))
    # customers N:M geolocation por prefijo postal
    conector(ax, [(a + m, fondo["customers"]), (a + m, 4.6)], "N : M por prefijo", (a + m, 6.15))
    # sellers N:M geolocation por prefijo postal (por abajo)
    conector(ax, [(c + m, fondo["sellers"]), (c + m, -0.25), (a + m, -0.25), (a + m, fondo["geolocation"])],
             "N : M por prefijo", ((a + c) / 2 + m, -0.25))

    ax.text(0.3, 10.25, "Modelo relacional de olist.duckdb", fontsize=14, weight="bold", color=AZUL)
    ax.text(COL[3], 3.9,
            "PK = llave primaria   FK = llave foránea\n"
            "1 : 0..21 = cada orden tiene de 0 a 21 filas\n"
            "en la tabla hija: unir sin agregar\n"
            "antes multiplica filas.\n\n"
            "geolocation repite prefijos: se agrega\n"
            "a una coordenada por prefijo antes\n"
            "de unirla con clientes o vendedores.",
            fontsize=8.3, va="top", color=GRIS,
            bbox=dict(boxstyle="round,pad=0.45", fc="#F3F4F6", ec="#CCCCCC"))

    for destino in (FIG_DIR / "00_datos", PROJECT_ROOT / "reports" / "informe"):
        destino.mkdir(parents=True, exist_ok=True)
        fig.savefig(destino / "modelo_relacional.png", dpi=200, bbox_inches="tight")
    print("Diagrama guardado en reports/figures/00_datos/ y reports/informe/")


if __name__ == "__main__":
    main()
