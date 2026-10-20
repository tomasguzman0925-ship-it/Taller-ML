-- Módulo 0 · Distribuciones de tiempo de entrega y retraso en días calendario.
-- Solo se usa para EDA; no define todavía la población final del Módulo A.
WITH entregas AS (
    SELECT
        date_diff('day', CAST(order_purchase_timestamp AS DATE),
                  CAST(order_delivered_customer_date AS DATE)) AS dias_entrega,
        date_diff('day', CAST(order_estimated_delivery_date AS DATE),
                  CAST(order_delivered_customer_date AS DATE)) AS dias_retraso
    FROM orders
    WHERE order_status = 'delivered'
      AND order_delivered_customer_date IS NOT NULL
      AND order_estimated_delivery_date IS NOT NULL
),
barras AS (
    SELECT 'tiempo_entrega' AS medida,
           CAST(FLOOR(dias_entrega / 5.0) * 5 AS INTEGER) AS inicio_intervalo_dias,
           COUNT(*) AS ordenes
    FROM entregas
    GROUP BY 1, 2
    UNION ALL
    SELECT 'retraso_vs_estimado',
           CAST(FLOOR(dias_retraso / 5.0) * 5 AS INTEGER),
           COUNT(*)
    FROM entregas
    GROUP BY 1, 2
)
SELECT medida, inicio_intervalo_dias, ordenes
FROM barras
ORDER BY medida, inicio_intervalo_dias;
