@echo off
set /p port="Enter port (9092): "
if not [%port%] == [] goto launch
  set port="9092"
:launch
echo Launching xabbo.py on port %port%

py . -p %port%
pause