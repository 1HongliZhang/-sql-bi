import os
import sys
import json
import argparse
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


def load_targets():
    """从同目录下的targets.json加载目标机器列表"""
    targets_path = Path(__file__).parent / "targets.json"
    
    if not targets_path.exists():
        raise FileNotFoundError(f"目标机器列表文件不存在: {targets_path}")
    
    with open(targets_path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_machine(target):
    """检查单台机器状态，返回结果字典"""
    ip = target["ip"]
    port = target["port"]
    name = target["name"]
    token = target["token"]
    
    result = {
        "ip": ip,
        "name": name,
        "machine_id": None,
        "status": "离线"
    }
    
    try:
        # 检查/info接口，超时3秒
        url = f"http://{ip}:{port}/info?token={token}"
        response = requests.get(url, timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            result["machine_id"] = data.get("machine_id")
            result["status"] = "在线"
        
        elif response.status_code == 403:
            result["status"] = "Token错误"
    
    except requests.exceptions.Timeout:
        result["status"] = "超时"
    except requests.exceptions.RequestException:
        result["status"] = "连接失败"
    
    return result


def download_file_from_machine(target, filename, download_dir):
    """从单台机器下载指定文件"""
    ip = target["ip"]
    port = target["port"]
    name = target["name"]
    token = target["token"]
    
    machine_dir = download_dir / name
    machine_dir.mkdir(parents=True, exist_ok=True)
    file_path = machine_dir / filename
    
    try:
        print(f"正在从 {name} 下载 {filename}...")
        url = f"http://{ip}:{port}/download/{filename}?token={token}"
        response = requests.get(url, stream=True, timeout=30)
        
        if response.status_code == 404:
            print(f"{name} 上未找到文件 {filename}")
            return False
        
        if response.status_code != 200:
            print(f"{name} 下载失败，状态码: {response.status_code}")
            return False
        
        # 写入文件，显示进度
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = int((downloaded / total_size) * 100)
                        print(f"{name}: {percent}% ({downloaded}/{total_size} bytes)", end="\r")
        
        print(f"{name}: 下载完成！")
        return True
    
    except Exception as e:
        print(f"{name}: 下载出错 - {str(e)}")
        if file_path.exists():
            file_path.unlink()
        return False


def main():
    parser = argparse.ArgumentParser(description="机房文件收集工具 - 客户端")
    parser.add_argument("--download", type=str, help="指定要下载的文件名")
    args = parser.parse_args()
    
    # 加载目标机器列表
    try:
        targets = load_targets()
    except Exception as e:
        print(f"加载目标列表失败: {e}")
        sys.exit(1)
    
    # 并发检查所有机器状态
    print("=" * 60)
    print("正在检查所有机器状态...")
    print("=" * 60)
    
    results = []
    success_count = 0
    fail_count = 0
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_target = {executor.submit(check_machine, t): t for t in targets}
        
        for future in as_completed(future_to_target):
            result = future.result()
            results.append(result)
            
            if result["status"] == "在线":
                success_count += 1
                print(f"[✓] {result['name']} ({result['ip']}) - 在线, 机器ID: {result['machine_id']}")
            else:
                fail_count += 1
                print(f"[✗] {result['name']} ({result['ip']}) - {result['status']}")
    
    # 保存状态结果
    output_path = Path(__file__).parent / "info_result.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("=" * 60)
    print(f"状态汇总: 在线 {success_count} 台, 离线/失败 {fail_count} 台")
    print(f"详细结果已保存到: {output_path}")
    print("=" * 60)
    
    # 如果指定了下载，则并发下载文件
    if args.download:
        filename = args.download
        download_dir = Path(__file__).parent / "downloads"
        download_dir.mkdir(exist_ok=True)
        
        # 筛选出在线的机器
        online_targets = [t for t, r in zip(targets, results) if r["status"] == "在线"]
        
        if not online_targets:
            print("没有在线的机器，无法下载文件")
            return
        
        print(f"\n准备从 {len(online_targets)} 台在线机器下载文件: {filename}")
        print("=" * 60)
        
        download_success = 0
        download_fail = 0
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(download_file_from_machine, t, filename, download_dir) 
                      for t in online_targets]
            
            for future in as_completed(futures):
                if future.result():
                    download_success += 1
                else:
                    download_fail += 1
        
        print("=" * 60)
        print(f"下载汇总: 成功 {download_success} 台, 失败 {download_fail} 台")
        print(f"文件已保存到: {download_dir}")
        print("=" * 60)


if __name__ == "__main__":
    main()
