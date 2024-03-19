@echo off
setlocal

set "targetPath=%USERPROFILE%\Desktop\GCONNECT\LaunchPad.bat"
set "shortcutPath=%USERPROFILE%\Desktop\GConnect.lnk"
set "startIn=%USERPROFILE%\Desktop\GCONNECT"
set "iconPath=%USERPROFILE%\Desktop\GCONNECT\img\launchpad_icon.ico"

(
    echo Set objShell = WScript.CreateObject^("WScript.Shell"^)
    echo Set objShortcut = objShell.CreateShortcut^(WScript.Arguments.Named^("ShortcutPath"^)^)
    echo objShortcut.TargetPath = WScript.Arguments.Named^("TargetPath"^)
    echo objShortcut.WorkingDirectory = WScript.Arguments.Named^("StartIn"^)
    echo objShortcut.IconLocation = WScript.Arguments.Named^("IconPath"^)
    echo objShortcut.Save
) > CreateShortcut.vbs

cscript /nologo CreateShortcut.vbs /ShortcutPath:"%shortcutPath%" /TargetPath:"%targetPath%" /StartIn:"%startIn%" /IconPath:"%iconPath%"

del CreateShortcut.vbs

endlocal

echo Installing...
timeout /t 1 >nul
ren "%USERPROFILE%\Desktop\GCONNECT\PVOD.ini" "PVOD.html"
timeout /t 1 >nul
ren "%USERPROFILE%\Desktop\GCONNECT\PVOS.ini" "PVOS.html"
timeout /t 1 >nul
c: 
attrib +h +r +s %USERPROFILE%\Desktop\GCONNECT\PVOD.html
attrib +h +r +s %USERPROFILE%\Desktop\GCONNECT\PVOS.html
setlocal enabledelayedexpansion
for /l %%i in (5,-1,1) do (
    set /p "=%%i " <nul
    ping -n 2 127.0.0.1 >nul
    <nul set /p "=%"
)
echo ...
timeout /t 1 >nul
echo Done.
timeout /t 1 >nul
echo Exiting...
timeout /t 1 >nul
explorer "%USERPROFILE%\Desktop"


