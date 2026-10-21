-- Módulo D · Integración (validación del plan de capacidad)
-- Despachos reales por estado de origen (vendedor) y por bloque de 7 días desde un origen.
-- Un despacho es un par (orden, vendedor), igual que en participacion_estado_vendedor.sql.
-- Parámetros (en este orden):
--   1) primer día del pronóstico, desde el que se cuentan los bloques de 7 días;
--   2) fecha de inicio (incluida) y 3) fecha de fin (excluida) de las compras.
WITH ventana AS (
    SELECT order_id,
           CAST(FLOOR(date_diff('day', ?::DATE, CAST(order_purchase_timestamp AS DATE)) / 7)
                AS INTEGER) + 1 AS semana
    FROM orders
    WHERE order_purchase_timestamp >= ?::TIMESTAMP
      AND order_purchase_timestamp <  ?::TIMESTAMP
),
despachos AS (
    SELECT DISTINCT v.order_id, v.semana, i.seller_id
    FROM ventana AS v
    JOIN order_items AS i USING (order_id)
)
SELECT d.semana,
       s.seller_state AS estado_vendedor,
       COUNT(*) AS despachos_reales
FROM despachos AS d
JOIN sellers AS s USING (seller_id)
GROUP BY 1, 2
ORDER BY 1, 3 DESC;
