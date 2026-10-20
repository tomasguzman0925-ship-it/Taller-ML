-- Módulo 0 · Cardinalidad de las relaciones entre tablas.
-- Una fila por relación; las tablas hijas se resumen por llave antes de cualquier unión.
WITH
items_por_orden AS (
    SELECT order_id, COUNT(*) AS filas
    FROM order_items
    GROUP BY order_id
),
pagos_por_orden AS (
    SELECT order_id, COUNT(*) AS filas
    FROM order_payments
    GROUP BY order_id
),
resenas_por_orden AS (
    SELECT order_id, COUNT(*) AS filas
    FROM order_reviews
    GROUP BY order_id
),
items_por_producto AS (
    SELECT product_id, COUNT(*) AS filas
    FROM order_items
    GROUP BY product_id
),
items_por_vendedor AS (
    SELECT seller_id, COUNT(*) AS filas
    FROM order_items
    GROUP BY seller_id
),
productos_por_categoria AS (
    SELECT product_category_name, COUNT(*) AS filas
    FROM products
    WHERE product_category_name IS NOT NULL
    GROUP BY product_category_name
),
geoloc_por_prefijo AS (
    SELECT geolocation_zip_code_prefix AS prefijo, COUNT(*) AS filas
    FROM geolocation
    WHERE geolocation_zip_code_prefix IS NOT NULL
    GROUP BY geolocation_zip_code_prefix
),
clientes_por_prefijo AS (
    SELECT customer_zip_code_prefix AS prefijo, COUNT(*) AS filas
    FROM customers
    WHERE customer_zip_code_prefix IS NOT NULL
    GROUP BY customer_zip_code_prefix
),
vendedores_por_prefijo AS (
    SELECT seller_zip_code_prefix AS prefijo, COUNT(*) AS filas
    FROM sellers
    WHERE seller_zip_code_prefix IS NOT NULL
    GROUP BY seller_zip_code_prefix
)
SELECT 'orders.order_id → order_items.order_id' AS relacion,
       (SELECT COUNT(*) FROM orders) AS filas_padre,
       (SELECT COUNT(*) FROM order_items) AS filas_hijas,
       (SELECT COUNT(*) FROM orders o JOIN items_por_orden i USING (order_id)) AS llaves_con_hijas,
       (SELECT COUNT(*) FROM items_por_orden WHERE filas > 1) AS llaves_con_varias_hijas,
       COALESCE((SELECT MAX(filas) FROM items_por_orden), 0) AS max_hijas_por_llave,
       (SELECT COUNT(*) FROM order_items i WHERE NOT EXISTS
           (SELECT 1 FROM orders o WHERE o.order_id = i.order_id)) AS filas_huerfanas
UNION ALL
SELECT 'orders.order_id → order_payments.order_id',
       (SELECT COUNT(*) FROM orders), (SELECT COUNT(*) FROM order_payments),
       (SELECT COUNT(*) FROM orders o JOIN pagos_por_orden p USING (order_id)),
       (SELECT COUNT(*) FROM pagos_por_orden WHERE filas > 1),
       COALESCE((SELECT MAX(filas) FROM pagos_por_orden), 0),
       (SELECT COUNT(*) FROM order_payments p WHERE NOT EXISTS
           (SELECT 1 FROM orders o WHERE o.order_id = p.order_id))
UNION ALL
SELECT 'orders.order_id → order_reviews.order_id',
       (SELECT COUNT(*) FROM orders), (SELECT COUNT(*) FROM order_reviews),
       (SELECT COUNT(*) FROM orders o JOIN resenas_por_orden r USING (order_id)),
       (SELECT COUNT(*) FROM resenas_por_orden WHERE filas > 1),
       COALESCE((SELECT MAX(filas) FROM resenas_por_orden), 0),
       (SELECT COUNT(*) FROM order_reviews r WHERE NOT EXISTS
           (SELECT 1 FROM orders o WHERE o.order_id = r.order_id))
UNION ALL
SELECT 'orders.customer_id → customers.customer_id',
       (SELECT COUNT(*) FROM orders), (SELECT COUNT(*) FROM customers),
       (SELECT COUNT(*) FROM orders o JOIN customers c USING (customer_id)),
       (SELECT COUNT(*) FROM (
           SELECT customer_id FROM customers GROUP BY customer_id HAVING COUNT(*) > 1
       )),
       COALESCE((SELECT MAX(filas) FROM (
           SELECT customer_id, COUNT(*) AS filas FROM customers GROUP BY customer_id
       )), 0),
       (SELECT COUNT(*) FROM orders o WHERE NOT EXISTS
           (SELECT 1 FROM customers c WHERE c.customer_id = o.customer_id))
UNION ALL
SELECT 'products.product_id ← order_items.product_id',
       (SELECT COUNT(*) FROM products), (SELECT COUNT(*) FROM order_items),
       (SELECT COUNT(*) FROM products p JOIN items_por_producto i USING (product_id)),
       (SELECT COUNT(*) FROM items_por_producto WHERE filas > 1),
       COALESCE((SELECT MAX(filas) FROM items_por_producto), 0),
       (SELECT COUNT(*) FROM order_items i WHERE NOT EXISTS
           (SELECT 1 FROM products p WHERE p.product_id = i.product_id))
UNION ALL
SELECT 'sellers.seller_id ← order_items.seller_id',
       (SELECT COUNT(*) FROM sellers), (SELECT COUNT(*) FROM order_items),
       (SELECT COUNT(*) FROM sellers s JOIN items_por_vendedor i USING (seller_id)),
       (SELECT COUNT(*) FROM items_por_vendedor WHERE filas > 1),
       COALESCE((SELECT MAX(filas) FROM items_por_vendedor), 0),
       (SELECT COUNT(*) FROM order_items i WHERE NOT EXISTS
           (SELECT 1 FROM sellers s WHERE s.seller_id = i.seller_id))
UNION ALL
SELECT 'category_translation.category ← products.category',
       (SELECT COUNT(*) FROM category_translation), (SELECT COUNT(*) FROM products),
       (SELECT COUNT(*) FROM category_translation t JOIN productos_por_categoria p
           ON t.product_category_name = p.product_category_name),
       (SELECT COUNT(*) FROM productos_por_categoria WHERE filas > 1),
       COALESCE((SELECT MAX(filas) FROM productos_por_categoria), 0),
       (SELECT COUNT(*) FROM products p WHERE p.product_category_name IS NOT NULL
           AND NOT EXISTS (SELECT 1 FROM category_translation t
                           WHERE t.product_category_name = p.product_category_name))
UNION ALL
SELECT 'geolocation.prefix ← customers.prefix',
       (SELECT COUNT(*) FROM geoloc_por_prefijo), (SELECT COUNT(*) FROM customers),
       (SELECT COUNT(*) FROM customers c JOIN geoloc_por_prefijo g
           ON c.customer_zip_code_prefix = g.prefijo),
       (SELECT COUNT(*) FROM geoloc_por_prefijo WHERE filas > 1),
       COALESCE((SELECT MAX(filas) FROM geoloc_por_prefijo), 0),
       (SELECT COUNT(*) FROM customers c WHERE c.customer_zip_code_prefix IS NOT NULL
           AND NOT EXISTS (SELECT 1 FROM geoloc_por_prefijo g
                           WHERE g.prefijo = c.customer_zip_code_prefix))
UNION ALL
SELECT 'geolocation.prefix ← sellers.prefix',
       (SELECT COUNT(*) FROM geoloc_por_prefijo), (SELECT COUNT(*) FROM sellers),
       (SELECT COUNT(*) FROM sellers s JOIN geoloc_por_prefijo g
           ON s.seller_zip_code_prefix = g.prefijo),
       (SELECT COUNT(*) FROM geoloc_por_prefijo WHERE filas > 1),
       COALESCE((SELECT MAX(filas) FROM geoloc_por_prefijo), 0),
       (SELECT COUNT(*) FROM sellers s WHERE s.seller_zip_code_prefix IS NOT NULL
           AND NOT EXISTS (SELECT 1 FROM geoloc_por_prefijo g
                           WHERE g.prefijo = s.seller_zip_code_prefix))
ORDER BY relacion;
