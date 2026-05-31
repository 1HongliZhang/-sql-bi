# 机房部署手册

本文档面向机房管理员，说明如何将打包后的服务端部署到各机房电脑。

---

## 一、部署包准备

### 1.1 打包服务端

1. 在有 Python 环境的电脑上执行打包：
```bash
cd server
pip install -r requirements.txt
build.bat
```

2. 打包完成后，在 `dist/server/` 目录下得到完整的部署包。

### 1.2 部署包结构

```
dist/server/
├── server.exe              # 主程序
├── server/                 # 依赖文件夹（不要修改）
├── install_startup.bat     # 开机自启注册脚本
├── uninstall_startup.bat  # 卸载脚本
├── config.json             # 配置文件
└── config.example.json      # 配置模板
```

---

## 二、拷贝到机房电脑

1. 将整个 `dist/server/` 文件夹拷贝到目标机房电脑。
2. 建议存放路径：`C:\LabFileServer\` 或 `D:\LabFileServer\`
3. 重要：**不要单独移动 exe 文件**，保持文件夹结构完整。

---

## 三、修改配置

用记事本打开 `config.json`，根据实际情况修改：

```json
{
  "machine_id": "机房-A-01",
  "share_dir": "D:/SharedFiles",
  "port": 5000,
  "token": "yoursecret123"
}
```

| 字段 | 说明 | 示例 |
|------|------|------|
| machine_id | 机器唯一编号 | 机房-A-01、机房-B-05 |
| share_dir | 要共享的文件夹路径 | D:/SharedFiles |
| port | 服务端口 | 5000 |
| token | 访问Token | yoursecret123 |

### 注意事项

- 每个机房电脑的 `machine_id` 必须唯一
- `share_dir` 可以是绝对路径（如 `D:/SharedFiles`）或相对路径（如 `SharedFiles`）
- 相对路径相对于 exe 所在目录
- `token` 建议所有机器使用相同值，便于客户端统一访问

---

## 四、放行防火墙端口

### 4.1 命令行方式（管理员权限）

```powershell
# 添加端口入站规则
netsh advfirewall firewall add rule name="LabFileServer" dir=in action=allow protocol=tcp localport=5000

# 验证规则
netsh advfirewall firewall show rule name="LabFileServer"
```

### 4.2 图形界面方式

1. 打开「Windows Defender 防火墙」
2. 点击「高级设置」
3. 点击「入站规则」→「新建规则」
4. 选择「端口」→ 输入 `5000` → 允许连接 → 完成

---

## 五、注册开机自启

### 5.1 注册

1. 右键点击 `install_startup.bat`
2. 选择「以管理员身份运行」
3. 看到「注册成功」提示即完成

### 5.2 验证

1. 打开「任务计划程序」（搜索栏输入 `taskschd.msc`）
2. 左侧展开「任务计划程序库」
3. 找到「LabFileServer」任务
4. 确认「状态」列为「就绪」

### 5.3 测试

1. 注销当前用户并重新登录
2. 打开任务管理器，确认 `server.exe` 在后台运行
3. 在浏览器访问 `http://127.0.0.1:5000/info?token=你的token`

### 5.4 卸载开机自启

如需卸载，右键以管理员身份运行 `uninstall_startup.bat`。

---

## 六、常见问题

### Q1: 浏览器访问显示 403 Forbidden
检查 URL 是否携带正确的 token 参数：
```
http://127.0.0.1:5000/info?token=yoursecret123
```

### Q2: 端口被占用
修改 `config.json` 中的 port 值，然后重启服务。

### Q3: 共享目录不存在
程序会自动创建不存在的目录。如需手动创建，请确保路径正确。

### Q4: 如何查看服务是否运行？
- 任务管理器中查找 `server.exe`
- 或浏览器访问 `/info` 接口

### Q5: 如何更新配置？
修改 `config.json` 后，需要手动重启服务（结束 server.exe 进程后重新启动）。

---

## 七、快速检查清单

- [ ] 部署包拷贝完成
- [ ] config.json 配置正确（machine_id 唯一）
- [ ] 防火墙端口已放行
- [ ] install_startup.bat 已执行
- [ ] 服务启动测试通过
- [ ] 客户端可以连接访问
