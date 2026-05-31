# 机房文件收集服务端

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 修改配置
编辑 `config.json`，修改以下字段：
- `machine_id`: 机器唯一编号
- `share_dir`: 共享文件夹绝对路径
- `port`: 服务端口（默认5000）
- `token`: 认证Token（必填，用于安全访问）

### 3. 启动服务
```bash
python server.py
```

## API接口

所有接口都需要在URL后添加 `?token=配置中的token` 进行认证。

| 接口 | 方法 | 说明 |
|------|------|------|
| /info | GET | 查看机器状态 |
| /files | GET | 查看文件列表 |
| /download/文件名 | GET | 下载文件 |

## 示例

### 查看机器状态
```bash
curl http://127.0.0.1:5000/info?token=yoursecret123
```
返回:
```json
{
  "machine_id": "机房-A-01",
  "status": "ok"
}
```

### 查看文件列表
```bash
curl http://127.0.0.1:5000/files?token=yoursecret123
```
返回:
```json
[
  {
    "name": "test.txt",
    "size": 1234,
    "modified_time": "2024-05-31T10:00:00"
  }
]
```

### 下载文件
在浏览器访问: `http://127.0.0.1:5000/download/test.txt?token=yoursecret123`
