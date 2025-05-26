SELECT name, order_id
FROM customers, orders WHERE customers.customer_id = orders.customer_id