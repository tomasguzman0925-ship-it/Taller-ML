-- Módulo 0 · Resumen de estados y ventana observada de compra.
SELECT order_status,
       COUNT(*) AS ordenes,
       MIN(CAST(order_purchase_timestamp AS DATE)) AS primera_fecha_compra,
       MAX(CAST(order_purchase_timestamp AS DATE)) AS ultima_fecha_compra,
       COUNT(DISTINCT CAST(order_purchase_timestamp AS DATE)) AS dias_con_ordenes
FROM orders
GROUP BY order_status
ORDER BY ordenes DESC;
