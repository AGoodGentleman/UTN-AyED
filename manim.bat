@echo off
set "PATH=%APPDATA%\TinyTeX\bin\windows;%PATH%"
"%~dp0.venv_manim\Scripts\manim.exe" %*
