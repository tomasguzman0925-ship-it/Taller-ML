-- Módulo 0 · Órdenes por semana calendario, con semanas sin órdenes en cero.
-- Parámetros: 1) inicio incluido, 2) fin excluido.
WITH
calendario AS (
    SELECT CAST(inicio AS DATE) AS semana
    FROM generate_series(
        date_trunc('week', CAST(?::DATE AS TIMESTAMP)),
        date_trunc('week', CAST(?::DATE AS TIMESTAMP) - INTERVAL 1 DAY),
        INTERVAL 1 WEEK
    ) AS t(inicio)
),
conteo AS (
    SELECT CAST(date_trunc('week', order_purchase_timestamp) AS DATE) AS semana,
           COUNT(*) AS ordenes
    FROM orders
    WHERE order_purchase_timestamp >= ?::TIMESTAMP
      AND order_purchase_timestamp < ?::TIMESTAMP
    GROUP BY 1
)
SELECT c.semana, COALESCE(n.ordenes, 0) AS ordenes
FROM calendario AS c
LEFT JOIN conteo AS n USING (semana)
ORDER BY c.semana;
