@echo off
chcp 65001 >nul
echo ========================================
echo   机房文件收集服务端 - 卸载开机自启
echo ========================================
echo.

:: 删除计划任务
schtasks /delete /tn "LabFileServer" /f

if errorlevel 1 (
    echo 未找到已注册的任务或删除失败
) else (
    echo 卸载成功！
)

echo.
pause
