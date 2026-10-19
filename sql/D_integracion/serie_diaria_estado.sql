-- Módulo D · Integración (demanda por estado del cliente)
-- Igual que B_series/serie_diaria.sql pero filtrada por un estado (p. ej. 'SP').
-- Parámetros: 1) fecha de inicio (incluida), 2) fecha de fin (excluida), 3) estado del cliente.
WITH calendario AS (
    SELECT CAST(dia AS DATE) AS fecha
    FROM generate_series(CAST(?::DATE AS TIMESTAMP), CAST(?::DATE AS TIMESTAMP) - INTERVAL 1 DAY, INTERVAL 1 DAY) AS t(dia)
),
conteo AS (
    SELECT CAST(o.order_purchase_timestamp AS DATE) AS fecha, COUNT(*) AS ordenes
    FROM orders AS o
    JOIN customers AS c USING (customer_id)
    WHERE c.customer_state = ?
    GROUP BY 1
)
SELECT c.fecha, COALESCE(n.ordenes, 0) AS ordenes
FROM calendario AS c
LEFT JOIN conteo AS n USING (fecha)
ORDER BY c.fecha;
