-- Módulo 0 · Distribución geográfica de clientes y vendedores por estado.
-- Clientes: personas distintas y órdenes. Vendedores: vendedores, órdenes distintas e ítems.
SELECT 'clientes' AS entidad, c.customer_state AS estado,
       COUNT(DISTINCT c.customer_unique_id) AS entidades,
       COUNT(DISTINCT o.order_id) AS ordenes,
       CAST(NULL AS BIGINT) AS items
FROM customers AS c
LEFT JOIN orders AS o USING (customer_id)
GROUP BY c.customer_state
UNION ALL
SELECT 'vendedores', s.seller_state,
       COUNT(DISTINCT s.seller_id),
       COUNT(DISTINCT i.order_id),
       COUNT(i.order_id)
FROM sellers AS s
LEFT JOIN order_items AS i USING (seller_id)
GROUP BY s.seller_state
ORDER BY entidad, entidades DESC;
