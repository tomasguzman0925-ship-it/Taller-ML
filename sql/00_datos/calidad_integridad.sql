-- Módulo 0 · Órdenes, pagos, geolocalización y traducción de categorías.
-- Los importes se comparan solo después de agregar cada tabla a una fila por orden.
WITH
items_por_orden AS (
    SELECT order_id, SUM(price + freight_value) AS total_items
    FROM order_items
    GROUP BY order_id
),
pagos_por_orden AS (
    SELECT order_id, SUM(payment_value) AS total_pagos
    FROM order_payments
    GROUP BY order_id
),
comparacion AS (
    SELECT i.order_id, i.total_items, p.total_pagos,
           p.total_pagos - i.total_items AS diferencia
    FROM items_por_orden AS i
    JOIN pagos_por_orden AS p USING (order_id)
),
prefijos_geo AS (
    SELECT DISTINCT geolocation_zip_code_prefix AS prefijo
    FROM geolocation
    WHERE geolocation_zip_code_prefix IS NOT NULL
),
chequeos AS (
    SELECT 'órdenes sin ítems' AS chequeo, COUNT(*) AS registros_afectados,
           (SELECT COUNT(*) FROM orders) AS unidad_referencia
    FROM orders AS o
    WHERE NOT EXISTS (SELECT 1 FROM order_items AS i WHERE i.order_id = o.order_id)
    UNION ALL
    SELECT 'filas de ítems sin orden', COUNT(*), (SELECT COUNT(*) FROM order_items)
    FROM order_items AS i
    WHERE NOT EXISTS (SELECT 1 FROM orders AS o WHERE o.order_id = i.order_id)
    UNION ALL
    SELECT 'órdenes sin pagos', COUNT(*), (SELECT COUNT(*) FROM orders)
    FROM orders AS o
    WHERE NOT EXISTS (SELECT 1 FROM order_payments AS p WHERE p.order_id = o.order_id)
    UNION ALL
    SELECT 'órdenes con ítems y pagos comparables', COUNT(*), (SELECT COUNT(*) FROM orders)
    FROM comparacion
    UNION ALL
    SELECT 'diferencia pagos vs. ítems > 0,01', COUNT(*), (SELECT COUNT(*) FROM comparacion)
    FROM comparacion
    WHERE ABS(diferencia) > 0.01
    UNION ALL
    SELECT 'prefijos postales de clientes sin geolocalización', COUNT(DISTINCT c.customer_zip_code_prefix),
           (SELECT COUNT(DISTINCT customer_zip_code_prefix) FROM customers
            WHERE customer_zip_code_prefix IS NOT NULL)
    FROM customers AS c
    WHERE c.customer_zip_code_prefix IS NOT NULL
      AND NOT EXISTS (
          SELECT 1 FROM prefijos_geo AS g
          WHERE g.prefijo = c.customer_zip_code_prefix
      )
    UNION ALL
    SELECT 'filas de clientes en prefijos sin geolocalización', COUNT(*),
           (SELECT COUNT(*) FROM customers)
    FROM customers AS c
    WHERE c.customer_zip_code_prefix IS NOT NULL
      AND NOT EXISTS (
          SELECT 1 FROM prefijos_geo AS g
          WHERE g.prefijo = c.customer_zip_code_prefix
      )
    UNION ALL
    SELECT 'prefijos postales de vendedores sin geolocalización', COUNT(DISTINCT s.seller_zip_code_prefix),
           (SELECT COUNT(DISTINCT seller_zip_code_prefix) FROM sellers
            WHERE seller_zip_code_prefix IS NOT NULL)
    FROM sellers AS s
    WHERE s.seller_zip_code_prefix IS NOT NULL
      AND NOT EXISTS (
          SELECT 1 FROM prefijos_geo AS g
          WHERE g.prefijo = s.seller_zip_code_prefix
      )
    UNION ALL
    SELECT 'filas de vendedores en prefijos sin geolocalización', COUNT(*),
           (SELECT COUNT(*) FROM sellers)
    FROM sellers AS s
    WHERE s.seller_zip_code_prefix IS NOT NULL
      AND NOT EXISTS (
          SELECT 1 FROM prefijos_geo AS g
          WHERE g.prefijo = s.seller_zip_code_prefix
      )
    UNION ALL
    SELECT 'productos sin categoría', COUNT(*), (SELECT COUNT(*) FROM products)
    FROM products
    WHERE product_category_name IS NULL
    UNION ALL
    SELECT 'productos con categoría sin traducción', COUNT(*), (SELECT COUNT(*) FROM products)
    FROM products AS p
    WHERE p.product_category_name IS NOT NULL
      AND NOT EXISTS (
          SELECT 1 FROM category_translation AS t
          WHERE t.product_category_name = p.product_category_name
      )
    UNION ALL
    SELECT 'categorías distintas sin traducción',
           COUNT(DISTINCT p.product_category_name),
           (SELECT COUNT(DISTINCT product_category_name) FROM products
            WHERE product_category_name IS NOT NULL)
    FROM products AS p
    WHERE p.product_category_name IS NOT NULL
      AND NOT EXISTS (
          SELECT 1 FROM category_translation AS t
          WHERE t.product_category_name = p.product_category_name
      )
)
SELECT chequeo, registros_afectados, unidad_referencia,
       ROUND(100.0 * registros_afectados / NULLIF(unidad_referencia, 0), 3) AS porcentaje
FROM chequeos
ORDER BY chequeo;
