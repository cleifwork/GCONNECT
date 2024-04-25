' Create WScript Shell Object to access filesystem.
Set WshShell = WScript.CreateObject("WScript.Shell")

' Select, or bring Focus to a window named `Setup`
WshShell.AppActivate "Node.js Setup"

WScript.Sleep 5000
WshShell.SendKeys "{ENTER}"
WScript.Sleep 2000
WshShell.SendKeys " "
WScript.Sleep 2000
WshShell.SendKeys "{ENTER}"
WScript.Sleep 2000
WshShell.SendKeys "{ENTER}"
WScript.Sleep 2000
WshShell.SendKeys "{ENTER}"
WScript.Sleep 2000
WshShell.SendKeys "{ENTER}"
WScript.Sleep 2000
WshShell.SendKeys "{ENTER}"
WScript.Sleep 20000
WshShell.SendKeys "{ENTER}"