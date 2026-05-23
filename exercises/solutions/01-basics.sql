-- SQL 基础练习题解答

-- 1. 查询所有产品的名称和价格
SELECT name, price FROM products;

-- 2. 查询价格大于 1000 元的产品
SELECT name, price FROM products WHERE price > 1000;

-- 3. 查询所有用户并按城市排序
SELECT * FROM users ORDER BY city;

-- 4. 查询前 5 条订单记录
SELECT * FROM orders LIMIT 5;

-- 5. 查询所有来自中国的用户
SELECT * FROM users WHERE country = '中国';
