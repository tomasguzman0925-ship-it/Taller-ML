-- Módulo D · Integración (plan de capacidad)
-- Participación histórica de cada estado de origen (vendedor) en los despachos.
-- Se cuentan pares (orden, vendedor) para no multiplicar filas por ítem: una orden con
-- 3 ítems del mismo vendedor genera un solo despacho.
-- Parámetros: 1) fecha de inicio (incluida), 2) fecha de fin (excluida) de la ventana histórica.
WITH despachos AS (
    SELECT DISTINCT i.order_id, i.seller_id
    FROM order_items AS i
    JOIN orders AS o USING (order_id)
    WHERE o.order_purchase_timestamp >= ?::TIMESTAMP
      AND o.order_purchase_timestamp <  ?::TIMESTAMP
)
SELECT s.seller_state AS estado_vendedor,
       COUNT(*) AS despachos,
       COUNT(*) / SUM(COUNT(*)) OVER () AS participacion
FROM despachos AS d
JOIN sellers AS s USING (seller_id)
GROUP BY 1
ORDER BY despachos DESC;
