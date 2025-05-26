SELECT name
FROM customers
WHERE customer_id IN (SELECT DISTINCT customer_id FROM orders)