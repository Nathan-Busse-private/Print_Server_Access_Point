#!/bin/bash

project_dir="../../.."
python_exe="/usr/bin/python3"  # Update with the correct Python executable path on Raspberry Pi
venv_name="venv"

echo "Creating virtual environment..."
"$python_exe" -m venv "$project_dir/$venv_name"

echo "Activating virtual environment..."
source "$project_dir/$venv_name/bin/activate"

echo "Virtual environment created and activated."
