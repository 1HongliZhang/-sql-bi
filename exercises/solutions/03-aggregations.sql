-- 聚合与分析练习题解答

-- 1. 计算所有订单的总金额
SELECT SUM(total_amount) as total_revenue
FROM orders;

-- 2. 计算每个产品的销售数量
SELECT p.name, SUM(oi.quantity) as total_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.id
GROUP BY p.name
ORDER BY total_sold DESC;

-- 3. 查询销售额最高的产品
SELECT p.name, SUM(oi.subtotal) as total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.id
GROUP BY p.name
ORDER BY total_revenue DESC
LIMIT 1;

-- 4. 按月统计销售额
SELECT 
    DATE_TRUNC('month', created_at) as month,
    SUM(total_amount) as monthly_revenue
FROM orders
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month;

-- 5. 找出购买金额最高的用户
SELECT u.username, SUM(o.total_amount) as total_spent
FROM orders o
JOIN users u ON o.user_id = u.id
GROUP BY u.username
ORDER BY total_spent DESC
LIMIT 1;
