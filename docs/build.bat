@echo off
REM Batch script to compile jemdoc files to HTML
REM Usage: Simply double-click this file or run "build.bat" in terminal

echo ========================================
echo Compiling jemdoc files...
echo ========================================
echo.

REM Compile index.jemdoc
echo Compiling index.jemdoc...
python ..\jemdoc -c mysite.conf index.jemdoc
if errorlevel 1 (
    echo [ERROR] Failed to compile index.jemdoc
) else (
    echo [OK] Successfully compiled index.jemdoc
)
echo.

REM Compile publications.jemdoc
echo Compiling publications.jemdoc...
python ..\jemdoc -c mysite.conf publications.jemdoc
if errorlevel 1 (
    echo [ERROR] Failed to compile publications.jemdoc
) else (
    echo [OK] Successfully compiled publications.jemdoc
)
echo.

REM Compile awards.jemdoc
echo Compiling awards.jemdoc...
python ..\jemdoc -c mysite.conf awards.jemdoc
if errorlevel 1 (
    echo [ERROR] Failed to compile awards.jemdoc
) else (
    echo [OK] Successfully compiled awards.jemdoc
)
echo.

echo ========================================
echo Compilation completed!
echo ========================================
pause

