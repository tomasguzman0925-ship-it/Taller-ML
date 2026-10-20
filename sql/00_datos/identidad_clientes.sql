-- Módulo 0 · Frecuencia de compra por persona, usando customer_unique_id.
-- customers.customer_id identifica el registro asociado a una orden; customer_unique_id
-- permite agrupar órdenes atribuibles a la misma persona.
WITH frecuencia AS (
    SELECT c.customer_unique_id, COUNT(DISTINCT o.order_id) AS ordenes
    FROM customers AS c
    JOIN orders AS o USING (customer_id)
    WHERE c.customer_unique_id IS NOT NULL
    GROUP BY c.customer_unique_id
)
SELECT ordenes,
       COUNT(*) AS clientes,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 3) AS porcentaje_clientes
FROM frecuencia
GROUP BY ordenes
ORDER BY ordenes;
