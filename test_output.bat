@echo off
echo Testing Python output...
python -c "print('Hello World from Python')"
python -c "import os; print('Current directory:', os.getcwd())"
python -c "import os; print('Files in directory:'); [print(f) for f in os.listdir('.')]"
pause
