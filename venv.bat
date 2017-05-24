@echo off
if exist virtualenv (
  virtualenv\Scripts\activate.bat
) else (
  py -m venv virtualenv
  virtualenv\Scripts\activate.bat
  cd src\core
  pip install -e .
  cd ..\winforms
  pip install -e .
  cd ..\..
  pip install -e .
)
