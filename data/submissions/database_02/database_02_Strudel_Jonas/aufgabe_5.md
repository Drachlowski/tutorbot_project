SELECT name
FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders)