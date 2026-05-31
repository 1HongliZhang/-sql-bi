import os
import sys
import subprocess
from pathlib import Path


def create_venv():
    venv_dir = Path(__file__).parent / "venv"
    if not venv_dir.exists():
        print("创建虚拟环境...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)


def install_requirements():
    venv_dir = Path(__file__).parent / "venv"
    requirements = Path(__file__).parent / "requirements.txt"
    
    pip_path = venv_dir / "Scripts" / "pip.exe" if sys.platform == "win32" else venv_dir / "bin" / "pip"
    
    print("安装依赖...")
    subprocess.run([str(pip_path), "install", "-r", str(requirements)], check=True)


def main():
    create_venv()
    install_requirements()
    
    venv_dir = Path(__file__).parent / "venv"
    python_path = venv_dir / "Scripts" / "python.exe" if sys.platform == "win32" else venv_dir / "bin" / "python"
    
    print("启动系统...")
    subprocess.run([str(python_path), str(Path(__file__).parent / "app" / "main.py")])


if __name__ == "__main__":
    main()
