-- Módulo B · Ventanas de referencia para Black Friday 2017 y paro de camioneros 2018.
-- Todas las fechas se enlazan como parámetros; el fin del conjunto consultado es exclusivo.
WITH
diaria AS (
    SELECT CAST(order_purchase_timestamp AS DATE) AS fecha, COUNT(*) AS ordenes
    FROM orders
    WHERE order_purchase_timestamp >= ?::TIMESTAMP
      AND order_purchase_timestamp < ?::TIMESTAMP
    GROUP BY 1
),
ventanas AS (
    SELECT 'black_friday_2017' AS evento, ?::DATE AS inicio, ?::DATE AS fin, 1 AS orden
    UNION ALL
    SELECT 'referencia_black_friday', ?::DATE, ?::DATE, 2
    UNION ALL
    SELECT 'paro_camioneros_2018', ?::DATE, ?::DATE, 3
    UNION ALL
    SELECT 'referencia_pre_paro', ?::DATE, ?::DATE, 4
    UNION ALL
    SELECT 'recuperacion_post_paro', ?::DATE, ?::DATE, 5
)
SELECT v.evento, d.fecha, d.ordenes
FROM ventanas AS v
JOIN diaria AS d ON d.fecha BETWEEN v.inicio AND v.fin
ORDER BY v.orden, d.fecha;
