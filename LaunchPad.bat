@echo off

REM Attempt to find the default Desktop path
set DefaultDesktopPath=%USERPROFILE%\Desktop

REM Check if the default Desktop path contains the GCONNECT folder
if exist "%DefaultDesktopPath%\GCONNECT" (
    REM If the GCONNECT folder exists on the default Desktop, launch the Python script
    start "" "pythonw.exe" "%USERPROFILE%\Desktop\GCONNECT\LaunchPad.py" %*  

    REM Exit quietly if the script ran successfully
    exit /b
)

REM Attempt to find the OneDrive path
REM Check if the OneDrive environment variable is set (for personal OneDrive accounts)
if defined OneDrive (
    set OneDrivePath=%OneDrive%
) else if defined OneDriveCommercial (
    REM If the personal OneDrive variable isn't set, check for OneDriveCommercial (for business/organization accounts)
    set OneDrivePath=%OneDriveCommercial%
) else (
    REM If neither environment variable is set, attempt to retrieve the OneDrive path from the Windows registry
    REM This registry query retrieves the OneDrive path for the current user
    for /f "tokens=3 delims=: " %%A in ('reg query "HKEY_CURRENT_USER\Software\Microsoft\OneDrive" /v "UserFolder"') do set OneDrivePath=%%A
)

REM Check if the OneDrive path was successfully found
if defined OneDrivePath (
    REM If OneDrivePath is defined, append \Desktop to form the full path to the Desktop within OneDrive
    set DesktopPath=%OneDrivePath%\Desktop
    echo OneDrive Desktop path is: %DesktopPath%

    REM Check if the symbolic link for GCONNECT already exists on the Desktop

    if not exist "%USERPROFILE%\Desktop\GCONNECT" (
        REM If the symlink doesn't exist, create it
        echo Creating symlink...
        mklink /D "%USERPROFILE%\Desktop\GCONNECT" "%DesktopPath%\GCONNECT"
        REM Inform the user that the symlink was created
        echo Symlink created successfully.
    ) else (
        REM If the symlink already exists or if the target folder doesn't exist, inform the user
        echo Symlink already exists or target folder does not exist.
    )

    REM Launch the Python script via the symlink
    REM Start the Python script located in the GCONNECT folder using pythonw.exe
    REM pythonw.exe is used to run the Python script without showing a console window
    start "" "pythonw.exe" "%USERPROFILE%\Desktop\GCONNECT\LaunchPad.py" %*

    REM Exit quietly if the script ran successfully
    exit /b

) else (
    REM If the OneDrive path could not be found, display an error message
    echo OneDrive path could not be found.
    pause
)