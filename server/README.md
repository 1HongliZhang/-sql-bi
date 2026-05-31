# 机房文件收集服务端

## 快速开始

### 方式一：直接运行（开发/测试）
```bash
pip install -r requirements.txt
python server.py
```

### 方式二：打包为 exe（生产部署）

#### 1. 打包
双击运行 `build.bat`，或命令行执行：
```bash
pyinstaller server.spec --clean
```

#### 2. 打包后的目录结构
```
dist/server/
├── server.exe              # 主程序
├── server/                 # 依赖文件夹
│   ├── python*.dll
│   ├── _struct.cpython-*.pyd
│   └── ...（各种依赖文件）
├── config.json             # 配置文件
└── config.example.json     # 配置模板
```

#### 3. 部署
将整个 `dist/server/` 文件夹拷贝到目标机器即可运行。

## 配置说明

编辑 `config.json`：
```json
{
  "machine_id": "机房-A-01",
  "share_dir": "D:/SharedFiles",
  "port": 5000,
  "token": "yoursecret123"
}
```

| 字段 | 说明 |
|------|------|
| machine_id | 机器唯一编号 |
| share_dir | 共享文件夹路径（绝对或相对） |
| port | 服务端口 |
| token | 认证Token |

## API接口

所有接口都需要在URL后添加 `?token=配置中的token` 进行认证。

| 接口 | 方法 | 说明 |
|------|------|------|
| /info | GET | 查看机器状态 |
| /files | GET | 查看文件列表 |
| /download/文件名 | GET | 下载文件 |

## 示例

```bash
curl http://127.0.0.1:5000/info?token=yoursecret123
curl http://127.0.0.1:5000/files?token=yoursecret123
```
