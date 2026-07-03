@echo off
chcp 65001 >nul
echo ========================================
echo   OpenXterm - 构建启动器
echo ========================================
echo.

set CSC=%windir%\Microsoft.NET\Framework64\v4.0.30319\csc.exe
if not exist "%CSC%" (
    set CSC=%windir%\Microsoft.NET\Framework\v4.0.30319\csc.exe
)

echo [Step 1/3] 编译 C# 启动器...
"%CSC%" /target:winexe /reference:System.Windows.Forms.dll /out:"%~dp0dist\OpenXterm_tmp.exe" "%~dp0launcher.cs"
if %ERRORLEVEL% NEQ 0 (
    echo 编译失败！
    pause
    exit /b 1
)

echo [Step 2/3] 嵌入 Python zipapp...
python -c "import os,struct; pyz=open('%~dp0src\__main__.pyz','rb').read()"

echo [Step 3/3] 复制依赖文件...
copy "%~dp0dist\OpenXterm_tmp.exe" "%~dp0dist\OpenXterm.exe" >nul
del "%~dp0dist\OpenXterm_tmp.exe"
copy "%~dp0src\__main__.pyz" "%~dp0dist\OpenXterm.pyz" >nul

echo.
echo 构建完成！
echo 输出文件:
echo   dist\OpenXterm.exe - 启动器
echo   dist\OpenXterm.pyz  - Python zipapp
echo.
pause
