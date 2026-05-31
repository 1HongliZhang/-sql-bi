# 机房文件收集 - 客户端

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置目标机器
编辑 `targets.json`，添加或修改机房机器列表，每个机器包含：
- `ip`: 机器IP地址
- `port`: 服务端口
- `name`: 机器别名（用于显示和存储）
- `token`: 服务端配置的认证Token

### 3. 检查机器状态
```bash
python collect_info.py
```

### 4. 从所有在线机器下载指定文件
```bash
python collect_info.py --download filename.txt
```

## 输出

下载的文件会保存在 `downloads/机器别名/` 目录下，按机器名称分目录存储。
