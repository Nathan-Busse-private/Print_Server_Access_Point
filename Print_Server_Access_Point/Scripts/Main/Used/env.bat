@echo off
set "project_dir=..\..\.."
set "python_exe=C:\Program Files\Python311\python.exe"
set "venv_name=venv"

echo Creating virtual environment...
"%python_exe%" -m venv "%project_dir%\%venv_name%"

echo Activating virtual environment...
call "%project_dir%\%venv_name%\Scripts\activate"

echo Virtual environment created and activated.
