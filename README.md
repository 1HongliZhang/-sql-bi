# SQL & BI 练习仓库

一个包含真实世界场景的 SQL 和 BI 练习仓库，支持一键部署。

## 🚀 快速开始

### 方式一：Docker 部署（推荐）

```bash
# 一键启动
docker-compose up -d

# 访问数据库
# PostgreSQL: localhost:5432
# pgAdmin: http://localhost:8080 (admin@example.com / admin)
```

### 方式二：本地安装

```bash
# 创建数据库
createdb sales_analytics

# 导入数据
psql -d sales_analytics -f database/schema.sql
psql -d sales_analytics -f database/data.sql
```

## 📁 项目结构

```
sql-bi-practice/
├── database/
│   ├── schema.sql      # 数据库表结构
│   └── data.sql        # 示例数据
├── exercises/          # SQL 练习题
│   ├── 01-basics.sql
│   ├── 02-joins.sql
│   ├── 03-aggregations.sql
│   └── solutions/      # 参考答案
├── docker/             # Docker 配置
└── docker-compose.yml  # 一键部署配置
```

## 📊 数据模型

包含一个完整的电商销售数据库：

- `users` - 用户表
- `products` - 产品表
- `orders` - 订单表
- `order_items` - 订单明细表
- `categories` - 分类表

## 🎯 练习题

| 难度 | 题目 | 知识点 |
|------|------|--------|
| ⭐ | 基础查询 | SELECT, WHERE, ORDER BY |
| ⭐⭐ | 多表关联 | JOIN, INNER/LEFT/RIGHT |
| ⭐⭐⭐ | 聚合分析 | GROUP BY, HAVING, Window Functions |

## 🐳 Docker 服务

- **PostgreSQL**: 数据库 (端口 5432)
- **pgAdmin**: 数据库管理界面 (端口 8080)
- **Metabase**: BI 可视化工具 (端口 3000)

## 📝 License

MIT
