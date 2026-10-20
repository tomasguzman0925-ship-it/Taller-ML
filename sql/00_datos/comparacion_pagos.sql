-- Módulo 0 · Comparación por orden entre pagos y (precio + flete).
-- Se devuelven las órdenes con discrepancia mayor a un centavo; ambas tablas se agregan
-- antes de cruzarlas para evitar la multiplicación de filas.
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
)
SELECT o.order_id, o.order_status,
       i.total_items, p.total_pagos,
       p.total_pagos - i.total_items AS diferencia
FROM orders AS o
JOIN items_por_orden AS i USING (order_id)
JOIN pagos_por_orden AS p USING (order_id)
WHERE ABS(p.total_pagos - i.total_items) > 0.01
ORDER BY ABS(p.total_pagos - i.total_items) DESC, o.order_id;
