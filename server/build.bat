@echo off
chcp 65001 >nul
echo ========================================
echo   机房文件收集服务端 - PyInstaller 打包
echo ========================================
echo.

:: 检查是否安装了PyInstaller
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo 正在安装 PyInstaller...
    pip install pyinstaller
)

:: 检查是否安装了Flask
python -c "import flask" 2>nul
if errorlevel 1 (
    echo 正在安装 Flask...
    pip install flask
)

echo.
echo 开始打包...
echo.

:: 执行打包
pyinstaller server.spec --clean

echo.
echo ========================================
echo   打包完成！
echo ========================================
echo.
echo 输出目录: dist\server\
echo.
echo 部署步骤:
echo   1. 将 dist\server\ 文件夹拷贝到目标机器
echo   2. 修改 config.json 中的配置
echo   3. 运行 install_startup.bat 注册开机自启
echo ========================================
pause
