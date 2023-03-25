ECHO OFF
chcp 65001
cls


:loop
cls
pylint thermometer_script.py --output-format=colorized
pause
goto loop
