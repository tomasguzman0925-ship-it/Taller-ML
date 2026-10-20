-- Módulo B · Serie diaria de órdenes
-- Una fila por día del período [?, ?) según order_purchase_timestamp, INCLUYENDO los días
-- sin órdenes (se completan con 0 gracias al calendario generado con generate_series).
-- Parámetros: 1) fecha de inicio (incluida), 2) fecha de fin (excluida).
-- Decisión Módulo 0: incluir todos los estados. La serie mide pedidos recibidos por
-- fecha de compra, no entregas completadas; cancelación o indisponibilidad son desenlaces.
WITH calendario AS (
    SELECT CAST(dia AS DATE) AS fecha
    FROM generate_series(CAST(?::DATE AS TIMESTAMP), CAST(?::DATE AS TIMESTAMP) - INTERVAL 1 DAY, INTERVAL 1 DAY) AS t(dia)
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
