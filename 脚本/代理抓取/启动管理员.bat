@echo off
:: 请求管理员权限
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo 需要管理员权限，正在重新启动...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /B
)

:: 获取当前目录
set SCRIPT_DIR=%~dp0

:: 显示正在运行的提示
echo 正在运行 Python 脚本...

:: 运行 Python 脚本，并保持窗口打开以查看输出
python "%SCRIPT_DIR%UI.py"
pause
