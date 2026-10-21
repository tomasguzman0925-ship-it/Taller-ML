-- Módulo D · Integración (plan de capacidad)
-- Despachos históricos por estado de origen (vendedor) en una ventana de compras.
-- Un despacho es un par (orden, vendedor): una orden con 3 ítems del mismo vendedor genera
-- un solo despacho, y una orden con 2 vendedores genera 2. Así no se multiplican filas por ítem.
-- despachos_por_orden convierte órdenes pronosticadas (Módulo B) en despachos por estado;
-- incluye en el denominador las órdenes sin ítems, que no generan despacho.
-- Parámetros: 1) fecha de inicio (incluida), 2) fecha de fin (excluida) de la ventana histórica.
WITH ventana AS (
    SELECT order_id
    FROM orders
    WHERE order_purchase_timestamp >= ?::TIMESTAMP
      AND order_purchase_timestamp <  ?::TIMESTAMP
),
despachos AS (
    SELECT DISTINCT i.order_id, i.seller_id
    FROM order_items AS i
    JOIN ventana AS v USING (order_id)
)
SELECT s.seller_state AS estado_vendedor,
       COUNT(*) AS despachos,
       COUNT(*) / SUM(COUNT(*)) OVER () AS participacion,
       COUNT(*) / (SELECT COUNT(*) FROM ventana) AS despachos_por_orden
FROM despachos AS d
JOIN sellers AS s USING (seller_id)
GROUP BY 1
ORDER BY despachos DESC;
