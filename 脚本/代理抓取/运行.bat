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

:: 使用 start 命令运行 Python 脚本，并隐藏窗口
start "" /B pythonw "%SCRIPT_DIR%UI1.py"

:: /B 参数使得在同一窗口中运行，不会打开新窗口