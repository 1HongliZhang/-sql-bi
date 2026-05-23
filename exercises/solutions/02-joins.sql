-- 多表关联练习题解答

-- 1. 查询所有订单及其用户信息
SELECT o.*, u.username, u.email
FROM orders o
JOIN users u ON o.user_id = u.id;

-- 2. 查询每个产品的分类名称
SELECT p.name, c.name as category_name
FROM products p
JOIN categories c ON p.category_id = c.id;

-- 3. 查询订单详情，包括产品名称
SELECT oi.*, p.name as product_name
FROM order_items oi
JOIN products p ON oi.product_id = p.id;

-- 4. 查询每个用户的订单数量
SELECT u.id, u.username, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.username;
