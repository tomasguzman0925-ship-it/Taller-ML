-- Módulo 0 · Estadísticas del tiempo de entrega y retraso en días calendario.
-- El retraso es positivo si la entrega ocurre después del día estimado.
WITH entregas AS (
    SELECT date_diff('day', CAST(order_purchase_timestamp AS DATE),
                     CAST(order_delivered_customer_date AS DATE)) AS dias_entrega,
           date_diff('day', CAST(order_estimated_delivery_date AS DATE),
                     CAST(order_delivered_customer_date AS DATE)) AS dias_retraso
    FROM orders
    WHERE order_status = 'delivered'
      AND order_delivered_customer_date IS NOT NULL
      AND order_estimated_delivery_date IS NOT NULL
)
SELECT COUNT(*) AS entregas_comparables,
       COUNT(*) FILTER (WHERE dias_retraso > 0) AS entregas_tardias,
       ROUND(100.0 * COUNT(*) FILTER (WHERE dias_retraso > 0) / COUNT(*), 3)
           AS porcentaje_tardias,
       approx_quantile(dias_entrega, 0.5) AS mediana_dias_entrega,
       approx_quantile(dias_entrega, 0.9) AS p90_dias_entrega,
       approx_quantile(dias_retraso, 0.5) AS mediana_dias_vs_estimado,
       approx_quantile(dias_retraso, 0.9) AS p90_dias_vs_estimado,
       MIN(dias_retraso) AS minimo_dias_vs_estimado,
       MAX(dias_retraso) AS maximo_dias_vs_estimado
FROM entregas;
