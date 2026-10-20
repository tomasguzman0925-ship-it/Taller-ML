-- Módulo 0 · Valores nulos por columna en todas las tablas.
-- No se imputan ni excluyen valores aquí: la decisión depende del uso de cada variable.
WITH faltantes AS (
    SELECT 'category_translation' AS tabla, 'product_category_name' AS columna,
           COUNT(*) FILTER (WHERE product_category_name IS NULL) AS nulos, COUNT(*) AS filas
    FROM category_translation
    UNION ALL
    SELECT 'category_translation', 'product_category_name_english',
           COUNT(*) FILTER (WHERE product_category_name_english IS NULL), COUNT(*)
    FROM category_translation
    UNION ALL
    SELECT 'customers', 'customer_id', COUNT(*) FILTER (WHERE customer_id IS NULL), COUNT(*) FROM customers
    UNION ALL
    SELECT 'customers', 'customer_unique_id', COUNT(*) FILTER (WHERE customer_unique_id IS NULL), COUNT(*) FROM customers
    UNION ALL
    SELECT 'customers', 'customer_zip_code_prefix', COUNT(*) FILTER (WHERE customer_zip_code_prefix IS NULL), COUNT(*) FROM customers
    UNION ALL
    SELECT 'customers', 'customer_city', COUNT(*) FILTER (WHERE customer_city IS NULL), COUNT(*) FROM customers
    UNION ALL
    SELECT 'customers', 'customer_state', COUNT(*) FILTER (WHERE customer_state IS NULL), COUNT(*) FROM customers
    UNION ALL
    SELECT 'geolocation', 'geolocation_zip_code_prefix', COUNT(*) FILTER (WHERE geolocation_zip_code_prefix IS NULL), COUNT(*) FROM geolocation
    UNION ALL
    SELECT 'geolocation', 'geolocation_lat', COUNT(*) FILTER (WHERE geolocation_lat IS NULL), COUNT(*) FROM geolocation
    UNION ALL
    SELECT 'geolocation', 'geolocation_lng', COUNT(*) FILTER (WHERE geolocation_lng IS NULL), COUNT(*) FROM geolocation
    UNION ALL
    SELECT 'geolocation', 'geolocation_city', COUNT(*) FILTER (WHERE geolocation_city IS NULL), COUNT(*) FROM geolocation
    UNION ALL
    SELECT 'geolocation', 'geolocation_state', COUNT(*) FILTER (WHERE geolocation_state IS NULL), COUNT(*) FROM geolocation
    UNION ALL
    SELECT 'order_items', 'order_id', COUNT(*) FILTER (WHERE order_id IS NULL), COUNT(*) FROM order_items
    UNION ALL
    SELECT 'order_items', 'order_item_id', COUNT(*) FILTER (WHERE order_item_id IS NULL), COUNT(*) FROM order_items
    UNION ALL
    SELECT 'order_items', 'product_id', COUNT(*) FILTER (WHERE product_id IS NULL), COUNT(*) FROM order_items
    UNION ALL
    SELECT 'order_items', 'seller_id', COUNT(*) FILTER (WHERE seller_id IS NULL), COUNT(*) FROM order_items
    UNION ALL
    SELECT 'order_items', 'shipping_limit_date', COUNT(*) FILTER (WHERE shipping_limit_date IS NULL), COUNT(*) FROM order_items
    UNION ALL
    SELECT 'order_items', 'price', COUNT(*) FILTER (WHERE price IS NULL), COUNT(*) FROM order_items
    UNION ALL
    SELECT 'order_items', 'freight_value', COUNT(*) FILTER (WHERE freight_value IS NULL), COUNT(*) FROM order_items
    UNION ALL
    SELECT 'order_payments', 'order_id', COUNT(*) FILTER (WHERE order_id IS NULL), COUNT(*) FROM order_payments
    UNION ALL
    SELECT 'order_payments', 'payment_sequential', COUNT(*) FILTER (WHERE payment_sequential IS NULL), COUNT(*) FROM order_payments
    UNION ALL
    SELECT 'order_payments', 'payment_type', COUNT(*) FILTER (WHERE payment_type IS NULL), COUNT(*) FROM order_payments
    UNION ALL
    SELECT 'order_payments', 'payment_installments', COUNT(*) FILTER (WHERE payment_installments IS NULL), COUNT(*) FROM order_payments
    UNION ALL
    SELECT 'order_payments', 'payment_value', COUNT(*) FILTER (WHERE payment_value IS NULL), COUNT(*) FROM order_payments
    UNION ALL
    SELECT 'order_reviews', 'review_id', COUNT(*) FILTER (WHERE review_id IS NULL), COUNT(*) FROM order_reviews
    UNION ALL
    SELECT 'order_reviews', 'order_id', COUNT(*) FILTER (WHERE order_id IS NULL), COUNT(*) FROM order_reviews
    UNION ALL
    SELECT 'order_reviews', 'review_score', COUNT(*) FILTER (WHERE review_score IS NULL), COUNT(*) FROM order_reviews
    UNION ALL
    SELECT 'order_reviews', 'review_comment_title', COUNT(*) FILTER (WHERE review_comment_title IS NULL), COUNT(*) FROM order_reviews
    UNION ALL
    SELECT 'order_reviews', 'review_comment_message', COUNT(*) FILTER (WHERE review_comment_message IS NULL), COUNT(*) FROM order_reviews
    UNION ALL
    SELECT 'order_reviews', 'review_creation_date', COUNT(*) FILTER (WHERE review_creation_date IS NULL), COUNT(*) FROM order_reviews
    UNION ALL
    SELECT 'order_reviews', 'review_answer_timestamp', COUNT(*) FILTER (WHERE review_answer_timestamp IS NULL), COUNT(*) FROM order_reviews
    UNION ALL
    SELECT 'orders', 'order_id', COUNT(*) FILTER (WHERE order_id IS NULL), COUNT(*) FROM orders
    UNION ALL
    SELECT 'orders', 'customer_id', COUNT(*) FILTER (WHERE customer_id IS NULL), COUNT(*) FROM orders
    UNION ALL
    SELECT 'orders', 'order_status', COUNT(*) FILTER (WHERE order_status IS NULL), COUNT(*) FROM orders
    UNION ALL
    SELECT 'orders', 'order_purchase_timestamp', COUNT(*) FILTER (WHERE order_purchase_timestamp IS NULL), COUNT(*) FROM orders
    UNION ALL
    SELECT 'orders', 'order_approved_at', COUNT(*) FILTER (WHERE order_approved_at IS NULL), COUNT(*) FROM orders
    UNION ALL
    SELECT 'orders', 'order_delivered_carrier_date', COUNT(*) FILTER (WHERE order_delivered_carrier_date IS NULL), COUNT(*) FROM orders
    UNION ALL
    SELECT 'orders', 'order_delivered_customer_date', COUNT(*) FILTER (WHERE order_delivered_customer_date IS NULL), COUNT(*) FROM orders
    UNION ALL
    SELECT 'orders', 'order_estimated_delivery_date', COUNT(*) FILTER (WHERE order_estimated_delivery_date IS NULL), COUNT(*) FROM orders
    UNION ALL
    SELECT 'products', 'product_id', COUNT(*) FILTER (WHERE product_id IS NULL), COUNT(*) FROM products
    UNION ALL
    SELECT 'products', 'product_category_name', COUNT(*) FILTER (WHERE product_category_name IS NULL), COUNT(*) FROM products
    UNION ALL
    SELECT 'products', 'product_name_lenght', COUNT(*) FILTER (WHERE product_name_lenght IS NULL), COUNT(*) FROM products
    UNION ALL
    SELECT 'products', 'product_description_lenght', COUNT(*) FILTER (WHERE product_description_lenght IS NULL), COUNT(*) FROM products
    UNION ALL
    SELECT 'products', 'product_photos_qty', COUNT(*) FILTER (WHERE product_photos_qty IS NULL), COUNT(*) FROM products
    UNION ALL
    SELECT 'products', 'product_weight_g', COUNT(*) FILTER (WHERE product_weight_g IS NULL), COUNT(*) FROM products
    UNION ALL
    SELECT 'products', 'product_length_cm', COUNT(*) FILTER (WHERE product_length_cm IS NULL), COUNT(*) FROM products
    UNION ALL
    SELECT 'products', 'product_height_cm', COUNT(*) FILTER (WHERE product_height_cm IS NULL), COUNT(*) FROM products
    UNION ALL
    SELECT 'products', 'product_width_cm', COUNT(*) FILTER (WHERE product_width_cm IS NULL), COUNT(*) FROM products
    UNION ALL
    SELECT 'sellers', 'seller_id', COUNT(*) FILTER (WHERE seller_id IS NULL), COUNT(*) FROM sellers
    UNION ALL
    SELECT 'sellers', 'seller_zip_code_prefix', COUNT(*) FILTER (WHERE seller_zip_code_prefix IS NULL), COUNT(*) FROM sellers
    UNION ALL
    SELECT 'sellers', 'seller_city', COUNT(*) FILTER (WHERE seller_city IS NULL), COUNT(*) FROM sellers
    UNION ALL
    SELECT 'sellers', 'seller_state', COUNT(*) FILTER (WHERE seller_state IS NULL), COUNT(*) FROM sellers
)
SELECT tabla, columna, nulos, filas,
       ROUND(100.0 * nulos / NULLIF(filas, 0), 3) AS porcentaje_nulos
FROM faltantes
WHERE nulos > 0
ORDER BY tabla, nulos DESC, columna;
