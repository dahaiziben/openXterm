@echo off
chcp 65001 >nul
title OpenXterm

:: Find Python
set PYTHON=python.exe
where python.exe >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 错误: 未找到 Python! 请先安装 Python 3.10+
    echo 下载: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Get the directory where this script is running from
set APP_DIR=%~dp0

:: Launch the app
start "" python "%APP_DIR%src\main.py"
exit /b 0
