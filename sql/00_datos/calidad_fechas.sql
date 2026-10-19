-- Módulo 0 · Calidad: marcas de tiempo faltantes e inconsistentes
-- Cuenta, por estado de la orden, los nulos y las secuencias imposibles
-- (por ejemplo, entrega al cliente antes de la compra).
SELECT order_status,
       COUNT(*) AS ordenes,
       SUM(CASE WHEN order_approved_at IS NULL THEN 1 ELSE 0 END)              AS sin_aprobacion,
       SUM(CASE WHEN order_delivered_carrier_date IS NULL THEN 1 ELSE 0 END)   AS sin_entrega_transportador,
       SUM(CASE WHEN order_delivered_customer_date IS NULL THEN 1 ELSE 0 END)  AS sin_entrega_cliente,
       SUM(CASE WHEN order_approved_at < order_purchase_timestamp THEN 1 ELSE 0 END)             AS aprobada_antes_compra,
       SUM(CASE WHEN order_delivered_carrier_date < order_purchase_timestamp THEN 1 ELSE 0 END)  AS transportador_antes_compra,
       SUM(CASE WHEN order_delivered_customer_date < order_purchase_timestamp THEN 1 ELSE 0 END) AS entrega_antes_compra,
       SUM(CASE WHEN order_delivered_customer_date < order_delivered_carrier_date THEN 1 ELSE 0 END) AS cliente_antes_transportador
FROM orders
GROUP BY order_status
ORDER BY ordenes DESC;
