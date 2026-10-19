-- Módulo 0 · Unicidad de llaves
-- Para cada tabla compara el número de filas con el número de valores distintos de su
-- llave candidata. Si filas > distintos, la llave NO es única en esa tabla.
SELECT 'orders' AS tabla, 'order_id' AS llave, COUNT(*) AS filas, COUNT(DISTINCT order_id) AS distintos FROM orders
UNION ALL
SELECT 'customers', 'customer_id', COUNT(*), COUNT(DISTINCT customer_id) FROM customers
UNION ALL
SELECT 'customers', 'customer_unique_id', COUNT(*), COUNT(DISTINCT customer_unique_id) FROM customers
UNION ALL
SELECT 'order_items', 'order_id + order_item_id', COUNT(*), COUNT(DISTINCT (order_id, order_item_id)) FROM order_items
UNION ALL
SELECT 'order_payments', 'order_id + payment_sequential', COUNT(*), COUNT(DISTINCT (order_id, payment_sequential)) FROM order_payments
UNION ALL
SELECT 'order_reviews', 'review_id', COUNT(*), COUNT(DISTINCT review_id) FROM order_reviews
UNION ALL
SELECT 'order_reviews', 'order_id', COUNT(*), COUNT(DISTINCT order_id) FROM order_reviews
UNION ALL
SELECT 'products', 'product_id', COUNT(*), COUNT(DISTINCT product_id) FROM products
UNION ALL
SELECT 'sellers', 'seller_id', COUNT(*), COUNT(DISTINCT seller_id) FROM sellers
UNION ALL
SELECT 'geolocation', 'geolocation_zip_code_prefix', COUNT(*), COUNT(DISTINCT geolocation_zip_code_prefix) FROM geolocation
UNION ALL
SELECT 'category_translation', 'product_category_name', COUNT(*), COUNT(DISTINCT product_category_name) FROM category_translation;
