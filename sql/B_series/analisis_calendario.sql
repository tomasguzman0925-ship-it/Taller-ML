-- Módulo B · Resúmenes de tendencia mensual y estacionalidad semanal.
-- Parámetros: 1) inicio incluido, 2) fin excluido.
WITH diaria AS (
    SELECT CAST(order_purchase_timestamp AS DATE) AS fecha, COUNT(*) AS ordenes
    FROM orders
    WHERE order_purchase_timestamp >= ?::TIMESTAMP
      AND order_purchase_timestamp < ?::TIMESTAMP
    GROUP BY 1
)
SELECT 'dia_semana' AS agrupacion,
       strftime(fecha, '%w') AS periodo,
       COUNT(*) AS dias_observados,
       ROUND(AVG(ordenes), 1) AS media_ordenes,
       approx_quantile(ordenes, 0.5) AS mediana_ordenes,
       SUM(ordenes) AS total_ordenes
FROM diaria
GROUP BY 1, 2
UNION ALL
SELECT 'mes',
       strftime(fecha, '%Y-%m'),
       COUNT(*),
       ROUND(AVG(ordenes), 1),
       approx_quantile(ordenes, 0.5),
       SUM(ordenes)
FROM diaria
GROUP BY 1, 2
ORDER BY agrupacion, periodo;
