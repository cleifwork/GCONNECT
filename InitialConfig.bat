@echo off
:: Check for admin privileges
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

:: If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"
:: Run commands here with administrative privileges
echo Installing http-server globally...
call npm install --global http-server

echo Installing customtkinter...
call pip install customtkinter

echo Installing packaging...
call pip install packaging

echo Installing Pillow...
call pip install Pillow

echo Installing google-auth...
call pip install google-auth

echo Installing google-api-python-client...
call pip install google-api-python-client

echo Installing pywin32...
call pip install pywin32

echo Starting http-server...
start "" http-server




