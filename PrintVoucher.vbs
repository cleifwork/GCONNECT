' Create WScript Shell Object to access filesystem.
Set WshShell = WScript.CreateObject("WScript.Shell")

' Select, or bring Focus to a window named `Google Chrome`
WshShell.AppActivate "Google Chrome"

' Wait for 2 sec then press Ctrl+P to open print window
WScript.Sleep 2000
WshShell.SendKeys "^p"