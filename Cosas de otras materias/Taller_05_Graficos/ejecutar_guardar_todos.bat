@echo off
setlocal
cd /d "%~dp0"

set "PY_CMD="
where py >nul 2>nul
if not errorlevel 1 (
    set "PY_CMD=py"
) else (
    where python >nul 2>nul
    if not errorlevel 1 (
        set "PY_CMD=python"
    ) else if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" (
        set "PY_CMD=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
    )
)

if "%PY_CMD%"=="" (
    echo No se encontro Python. Instala Python o ejecuta desde un entorno que lo tenga disponible.
    pause
    exit /b 1
)

"%PY_CMD%" "taller_05_graficos_15_25.py" --todos --guardar
pause
