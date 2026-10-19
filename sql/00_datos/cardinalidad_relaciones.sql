-- Módulo 0 · Cardinalidad de las relaciones con orders
-- Cuántas filas de cada tabla hija corresponden a una orden. Si el máximo es > 1, unir
-- esa tabla directamente con orders multiplica filas: hay que agregarla primero
-- (GROUP BY order_id) y luego unir.
WITH por_orden AS (
    SELECT o.order_id,
           (SELECT COUNT(*) FROM order_items    i WHERE i.order_id = o.order_id) AS n_items,
           (SELECT COUNT(*) FROM order_payments p WHERE p.order_id = o.order_id) AS n_pagos,
           (SELECT COUNT(*) FROM order_reviews  r WHERE r.order_id = o.order_id) AS n_resenas
    FROM orders AS o
)
SELECT 'order_items' AS tabla_hija,
       MIN(n_items) AS minimo, MAX(n_items) AS maximo, AVG(n_items) AS promedio,
       SUM(CASE WHEN n_items = 0 THEN 1 ELSE 0 END) AS ordenes_sin_filas,
       SUM(CASE WHEN n_items > 1 THEN 1 ELSE 0 END) AS ordenes_con_varias
FROM por_orden
UNION ALL
SELECT 'order_payments', MIN(n_pagos), MAX(n_pagos), AVG(n_pagos),
       SUM(CASE WHEN n_pagos = 0 THEN 1 ELSE 0 END), SUM(CASE WHEN n_pagos > 1 THEN 1 ELSE 0 END)
FROM por_orden
UNION ALL
SELECT 'order_reviews', MIN(n_resenas), MAX(n_resenas), AVG(n_resenas),
       SUM(CASE WHEN n_resenas = 0 THEN 1 ELSE 0 END), SUM(CASE WHEN n_resenas > 1 THEN 1 ELSE 0 END)
FROM por_orden;
