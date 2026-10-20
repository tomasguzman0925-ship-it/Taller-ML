-- Módulo 0 · Volumen mensual de órdenes por estado.
-- Sirve para decidir si la demanda representa todos los pedidos recibidos o solo los
-- finalmente entregados; cada orden se cuenta una sola vez por fecha de compra.
SELECT CAST(date_trunc('month', order_purchase_timestamp) AS DATE) AS mes,
       order_status,
       COUNT(*) AS ordenes
FROM orders
GROUP BY 1, 2
ORDER BY 1, 2;
