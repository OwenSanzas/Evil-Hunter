@echo off
chcp 65001 >nul
setlocal

:: 定义源文件和目标路径
set "SOURCE_FILE=fmzj3.9J.w3x"
set "DEST_DIR=C:\Users\Owen Sanzas\Documents\Warcraft III\Maps"

:: 检查源文件是否存在
if not exist "%SOURCE_FILE%" (
    echo 源文件 %SOURCE_FILE% 不存在！
    pause
    exit /b
)

:: 创建目标目录（如果不存在）
if not exist "%DEST_DIR%" mkdir "%DEST_DIR%"

:: 复制文件并覆盖
copy /Y "%SOURCE_FILE%" "%DEST_DIR%\"

echo 文件已成功复制到 %DEST_DIR%
pause
