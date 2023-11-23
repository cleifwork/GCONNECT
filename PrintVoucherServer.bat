@echo off

:: Check if http-server is already running
tasklist /FI "IMAGENAME eq node.exe" 2>NUL | find /I /N "node.exe" >NUL
if "%ERRORLEVEL%"=="0" (
    echo http-server is already running. Stopping it...
    taskkill /F /IM "node.exe" /T >NUL
    timeout /t 2 >NUL
)

:: Start http-server
start /min cmd /k http-server

:: Wait for 2 seconds
timeout /t 2 >NUL

:: Open the URL in the default browser
start "" "http://localhost:8080/PrintVoucher.html"

:: Allocate 3 seconds loading time to make sure web form has been rendered completely, allocate higher value for slow internet connection
timeout /t 3

:: Execute the PrintVoucher.vbs script to press Ctrl+P
pushd %~dp0
cscript PrintVoucher.vbs
exit
