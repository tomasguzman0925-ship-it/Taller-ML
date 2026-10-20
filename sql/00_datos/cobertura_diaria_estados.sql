-- Módulo 0 · Cobertura diaria por estado de orden para revisar el cierre de extracción.
-- Parámetros: 1) fecha de inicio incluida, 2) fecha de fin excluida.
SELECT CAST(order_purchase_timestamp AS DATE) AS fecha,
       order_status,
       COUNT(*) AS ordenes
FROM orders
WHERE order_purchase_timestamp >= ?::TIMESTAMP
  AND order_purchase_timestamp < ?::TIMESTAMP
GROUP BY 1, 2
ORDER BY 1, 2;
