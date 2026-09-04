@echo off
cd /d "%~dp0"
echo Generando graficos del Taller 04...
echo Si faltan numpy o matplotlib, el programa intentara instalarlos automaticamente.
echo.
where py >nul 2>nul
if %errorlevel%==0 (
    py taller_04_graficos_obligatorios.py --guardar
) else (
    python taller_04_graficos_obligatorios.py --guardar
)
echo.
echo Listo. Los PNG quedan en la carpeta graficos_taller_04.
pause
