@echo off
chcp 65001 >nul
echo ========================================
echo   机房文件收集服务端 - 开机自启注册
echo ========================================
echo.

:: 获取脚本所在目录（exe所在目录）
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

:: 检查server.exe是否存在
if not exist "%SCRIPT_DIR%\server.exe" (
    echo [错误] 未找到 server.exe
    echo 请将此脚本放在 exe 同目录下运行！
    pause
    exit /b 1
)

echo 正在注册开机自启任务...
echo.

:: 删除旧任务（如果存在）
schtasks /delete /tn "LabFileServer" /f 2>nul

:: 创建新任务
:: /sc ONLOGON - 登录时触发
:: /rl LIMITED - 运行权限有限
:: /tr - 运行的程序路径
schtasks /create /tn "LabFileServer" /tr "\"%SCRIPT_DIR%\server.exe\"" /sc ONLOGON /rl LIMITED /f

if errorlevel 1 (
    echo [错误] 注册失败！
    echo 请以管理员身份运行此脚本！
    pause
    exit /b 1
)

echo.
echo ========================================
echo   注册成功！
echo ========================================
echo.
echo 任务信息：
echo   任务名称: LabFileServer
echo   触发条件: 用户登录时
echo   程序路径: %SCRIPT_DIR%\server.exe
echo.
echo 验证方法：
echo   1. 打开"任务计划程序"
echo   2. 在"任务计划程序库"中找到"LabFileServer"
echo   3. 确认状态为"就绪"
echo.
echo 如需卸载开机自启，运行 uninstall_startup.bat
echo ========================================
pause
