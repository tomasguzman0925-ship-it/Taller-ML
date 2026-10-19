-- Módulo 0 · Cobertura temporal
-- Órdenes por mes de compra y por estado. Sirve para definir el período útil
-- (hay meses al inicio y al final con muy pocas órdenes).
SELECT DATE_TRUNC('month', order_purchase_timestamp) AS mes,
       COUNT(*) AS ordenes,
       SUM(CASE WHEN order_status = 'delivered' THEN 1 ELSE 0 END) AS entregadas,
       SUM(CASE WHEN order_status = 'canceled'  THEN 1 ELSE 0 END) AS canceladas
FROM orders
GROUP BY 1
ORDER BY 1;
