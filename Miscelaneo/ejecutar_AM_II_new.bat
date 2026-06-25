@echo off
setlocal

set "ROOT=%~dp0.."
set "PYTHON=%ROOT%\.venv_manim\Scripts\python.exe"
set "SCRIPT=%~dp0AM II_new.py"

if not exist "%PYTHON%" (
    echo No se encontro el interprete local:
    echo %PYTHON%
    echo.
    echo Crea o repara el entorno virtual antes de ejecutar este archivo.
    pause
    exit /b 1
)

"%PYTHON%" "%SCRIPT%"

if errorlevel 1 (
    echo.
    echo El script termino con un error.
    pause
)
