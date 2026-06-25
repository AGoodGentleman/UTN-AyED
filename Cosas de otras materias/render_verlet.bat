@echo off
set "ROOT=%~dp0.."
call "%ROOT%\manim.bat" -pql "%~dp0verlet_smr_scene.py" VerletSMRScene
