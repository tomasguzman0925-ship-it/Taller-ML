-- Módulo 0 · Órdenes por día de todo el período observado, incluidos días en cero.
-- Se cuentan todos los registros de orders, sin filtrar por su estado final.
WITH
limites AS (
    SELECT CAST(MIN(order_purchase_timestamp) AS DATE) AS inicio,
           CAST(MAX(order_purchase_timestamp) AS DATE) AS fin
    FROM orders
),
calendario AS (
    SELECT CAST(dia AS DATE) AS fecha
    FROM limites,
         generate_series(CAST(inicio AS TIMESTAMP), CAST(fin AS TIMESTAMP), INTERVAL 1 DAY) AS t(dia)
),
conteo AS (
    SELECT CAST(order_purchase_timestamp AS DATE) AS fecha, COUNT(*) AS ordenes
    FROM orders
    GROUP BY 1
)
SELECT c.fecha, COALESCE(n.ordenes, 0) AS ordenes
FROM calendario AS c
LEFT JOIN conteo AS n USING (fecha)
ORDER BY c.fecha;
