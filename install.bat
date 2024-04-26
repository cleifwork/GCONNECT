@echo off
:: This block of code checks if the script has admin privileges. If not, it relaunches itself with admin privileges.
>NUL 2>&1 REG.exe query "HKU\S-1-5-19" || (
    ECHO SET UAC = CreateObject^("Shell.Application"^) > "%TEMP%\Getadmin.vbs"
    ECHO UAC.ShellExecute "%~f0", "%1", "", "runas", 1 >> "%TEMP%\Getadmin.vbs"
    "%TEMP%\Getadmin.vbs"
    DEL /f /q "%TEMP%\Getadmin.vbs" 2>NUL
    Exit /b
)

:: Set variables for creating a desktop shortcut
set "targetPath=%USERPROFILE%\Desktop\GCONNECT\LaunchPad.bat"
set "shortcutPath=%USERPROFILE%\Desktop\GConnect.lnk"
set "startIn=%USERPROFILE%\Desktop\GCONNECT"
set "iconPath=%USERPROFILE%\Desktop\GCONNECT\img\launchpad_icon.ico"

:: Create a VBScript to create a shortcut
(
    echo Set objShell = WScript.CreateObject^("WScript.Shell"^)
    echo Set objShortcut = objShell.CreateShortcut^(WScript.Arguments.Named^("ShortcutPath"^)^)
    echo objShortcut.TargetPath = WScript.Arguments.Named^("TargetPath"^)
    echo objShortcut.WorkingDirectory = WScript.Arguments.Named^("StartIn"^)
    echo objShortcut.IconLocation = WScript.Arguments.Named^("IconPath"^)
    echo objShortcut.Save
) > CreateShortcut.vbs

:: Run the VBScript to create the shortcut
cscript /nologo CreateShortcut.vbs /ShortcutPath:"%shortcutPath%" /TargetPath:"%targetPath%" /StartIn:"%startIn%" /IconPath:"%iconPath%"

:: Clean up temporary VBScript file
del CreateShortcut.vbs

:InstallPyNode
:: Install Python
echo Installing python-3.11.4...
timeout /t 1 >nul
start "" "%USERPROFILE%\Desktop\GCONNECT\exe\python-3.11.4-amd64.exe"
pushd %~dp0
cscript PythonEXE.vbs

:: Install Node.js
echo Installing node-v18.16.1...
timeout /t 10 >nul
start "" "%USERPROFILE%\Desktop\GCONNECT\exe\node-v18.16.1-x64.msi"
pushd %~dp0
cscript NodeMSI.vbs

:: Install Python packages using pip
timeout /t 10 >nul

echo Installing customtkinter...
pip install customtkinter

echo Installing packaging...
pip install packaging

echo Installing Pillow...
pip install Pillow

echo Installing google-auth...
pip install google-auth

echo Installing google-api-python-client...
pip install google-api-python-client

echo Installing pywin32...
pip install pywin32

echo Installation completed.

:: Install global npm package
timeout /t 5 >nul
npm install --global http-server

:: Launching GConnect App
echo Launching GConnect App...
timeout /t 5 >nul
start "" "%USERPROFILE%\Desktop\GCONNECT\LaunchPad.bat"


call :InstallPyNode