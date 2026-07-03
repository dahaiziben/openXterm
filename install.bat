@echo off
chcp 65001 >nul
echo ========================================
echo   OpenXterm 快速安装脚本
echo ========================================
echo.
echo 正在检查 Python...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 错误：未找到 Python！请先安装 Python 3.10+
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo 正在检查依赖...
pip show cryptography >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 正在安装 cryptography...
    pip install cryptography
)

echo.
echo 正在创建快捷方式...
set STARTMENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs\OpenXterm
if not exist "%STARTMENU%" mkdir "%STARTMENU%"

echo.
echo 安装完成！
echo.
echo 启动方式：
echo   1. 双击运行: src\main.py
echo   2. 命令行: python src\main.py
echo   3. 开始菜单: OpenXterm 文件夹
echo.
echo 如需构建 exe 安装包，请运行 build.bat
echo.
pause
