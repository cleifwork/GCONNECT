:: This block of code checks if the script has admin privileges. If not, it relaunches itself with admin privileges.
>NUL 2>&1 REG.exe query "HKU\S-1-5-19" || (
    ECHO SET UAC = CreateObject^("Shell.Application"^) > "%TEMP%\Getadmin.vbs"
    ECHO UAC.ShellExecute "%~f0", "%1", "", "runas", 1 >> "%TEMP%\Getadmin.vbs"
    "%TEMP%\Getadmin.vbs"
    DEL /f /q "%TEMP%\Getadmin.vbs" 2>NUL
    Exit /b
)

@echo off
setlocal

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

:: Install Python
echo Installing python-3.11.4...
timeout /t 1 >nul
start "" "%USERPROFILE%\Desktop\GCONNECT\exe\python-3.11.4-amd64.exe"
pushd %~dp0
start "" /wait PythonEXE.vbs

:: Install Python packages using pip
timeout /t 10 >nul
setlocal

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

endlocal

:: Install Node.js
echo Installing node-v18.16.1...
timeout /t 10 >nul
start "" "%USERPROFILE%\Desktop\GCONNECT\exe\node-v18.16.1-x64.msi"
pushd %~dp0
start "" /wait NodeMSI.vbs

:: Install global npm package
timeout /t 10 >nul
npm install --global http-server

:: Display loading dots
timeout /t 1 >nul
setlocal enabledelayedexpansion

for /l %%i in (1,1,5) do (
    set "dots="
    for /l %%j in (1,1,%%i) do (
        set "dots=!dots!. "
    )
    <nul set /p "=!dots!"
    ping -n 2 127.0.0.1 >nul
)

endlocal

:: Final messages and cleanup
timeout /t 1 >nul
echo Done.
timeout /t 1 >nul
echo Exiting...
timeout /t 1 >nul
explorer "%USERPROFILE%\Desktop"
