import os
import json
from pathlib import Path
from datetime import datetime
from flask import Flask, jsonify, send_from_directory, safe_join, abort, request

app = Flask(__name__)


def load_config():
    """从同目录下的config.json读取配置"""
    config_path = Path(__file__).parent / "config.json"
    
    if not config_path.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_path}")
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    # 验证必需字段
    required_fields = ["machine_id", "share_dir", "token"]
    for field in required_fields:
        if field not in config:
            raise ValueError(f"配置缺少必需字段: {field}")
    
    # 确保port为整数，默认5000
    config["port"] = int(config.get("port", 5000))
    
    return config


# 全局配置
try:
    config = load_config()
except Exception as e:
    print(f"加载配置失败: {e}")
    exit(1)


def validate_share_dir():
    """验证共享目录是否存在，不存在则创建"""
    share_dir = Path(config["share_dir"])
    if not share_dir.exists():
        share_dir.mkdir(parents=True, exist_ok=True)
        print(f"共享目录不存在，已创建: {share_dir}")
    elif not share_dir.is_dir():
        raise NotADirectoryError(f"配置的路径不是目录: {share_dir}")
    return share_dir


# 初始化时验证共享目录
try:
    share_dir = validate_share_dir()
except Exception as e:
    print(f"验证共享目录失败: {e}")
    exit(1)


def check_token():
    """Token认证检查，返回True表示认证通过，False表示失败"""
    token = request.args.get("token")
    if token != config["token"]:
        return False
    return True


@app.before_request
def before_request():
    """在每个请求前执行，检查Token认证"""
    if not check_token():
        return jsonify({"error": "未授权，需要有效的Token"}), 403


@app.route("/info", methods=["GET"])
def get_info():
    """返回机器基本信息"""
    return jsonify({
        "machine_id": config["machine_id"],
        "status": "ok"
    })


@app.route("/files", methods=["GET"])
def get_files():
    """返回共享目录下的文件列表"""
    file_list = []
    
    try:
        for file_path in share_dir.iterdir():
            if file_path.is_file():  # 只处理文件，忽略目录
                stat_info = file_path.stat()
                # 转换时间为ISO格式
                modified_time = datetime.fromtimestamp(stat_info.st_mtime).isoformat()
                
                file_list.append({
                    "name": file_path.name,
                    "size": stat_info.st_size,
                    "modified_time": modified_time
                })
    except Exception as e:
        return jsonify({
            "error": f"读取文件列表失败: {str(e)}"
        }), 500
    
    return jsonify(file_list)


@app.route("/download/<path:filepath>", methods=["GET"])
def download_file(filepath):
    """下载指定文件，防止路径穿越"""
    try:
        # 安全拼接路径，防止路径穿越
        safe_path = safe_join(str(share_dir), filepath)
        if not safe_path or not os.path.exists(safe_path):
            abort(404, description="文件不存在")
        
        if not os.path.isfile(safe_path):
            abort(400, description="不能下载目录")
        
        # 检查是否在共享目录内
        resolved_share_dir = os.path.realpath(str(share_dir))
        resolved_file_path = os.path.realpath(safe_path)
        
        if not resolved_file_path.startswith(resolved_share_dir):
            abort(403, description="路径越权访问被拒绝")
        
        # 返回文件流
        filename = os.path.basename(safe_path)
        return send_from_directory(str(share_dir), filepath, as_attachment=True)
    
    except Exception as e:
        if e.code in (403, 404):
            raise
        return jsonify({"error": f"下载文件失败: {str(e)}"}), 500


def main():
    """主函数，启动服务"""
    # 获取本机IP（用于显示访问地址）
    host = "0.0.0.0"
    port = config["port"]
    
    # 打印启动信息
    print("=" * 50)
    print("机房文件收集服务已启动")
    print("=" * 50)
    print(f"机器编号: {config['machine_id']}")
    print(f"共享目录: {share_dir}")
    print(f"监听地址: http://{host}:{port}")
    print(f"本机访问: http://127.0.0.1:{port}")
    print("=" * 50)
    print("接口说明:")
    print(f"  - GET /info?token=xxx    -> 查看机器状态")
    print(f"  - GET /files?token=xxx   -> 查看文件列表")
    print(f"  - GET /download/文件名?token=xxx -> 下载文件")
    print("=" * 50)
    
    # 启动Flask服务
    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    main()
