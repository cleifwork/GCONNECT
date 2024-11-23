@echo off

REM Attempt to find the default Desktop path
set DefaultDesktopPath=%USERPROFILE%\Desktop

REM Check if the GCONNECT folder exists on the default Desktop
echo Checking Default Desktop: %DefaultDesktopPath%\GCONNECT
if exist "%DefaultDesktopPath%\GCONNECT" (
    echo GCONNECT folder found on default Desktop.
    echo %DefaultDesktopPath% > "%USERPROFILE%\Desktop\GCONNECT\desktop_path.txt"
    start "" "pythonw.exe" "%DefaultDesktopPath%\GCONNECT\LaunchPad.py" %*
    exit /b
) else (
    echo GCONNECT folder not found on default Desktop.
)

REM Check for Public Desktop
set PublicDesktopPath=%PUBLIC%\Desktop
echo Checking Public Desktop: %PublicDesktopPath%\GCONNECT
if exist "%PublicDesktopPath%\GCONNECT" (
    echo GCONNECT folder found on Public Desktop.
    echo %PublicDesktopPath% > "%PUBLIC%\Desktop\GCONNECT\desktop_path.txt"
    start "" "pythonw.exe" "%PublicDesktopPath%\GCONNECT\LaunchPad.py" %*
    exit /b
) else (
    echo GCONNECT folder not found on Public Desktop.
    pause
    exit /b
)
