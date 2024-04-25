' Create WScript Shell Object to access filesystem.
Set WshShell = WScript.CreateObject("WScript.Shell")

' Select, or bring Focus to a window named `Setup`
WshShell.AppActivate "Python 3.11.4 (64-bit) Setup"

WScript.Sleep 5000
WshShell.SendKeys "{TAB}"
WScript.Sleep 2000
WshShell.SendKeys "{TAB}"
WScript.Sleep 2000
WshShell.SendKeys " "
WScript.Sleep 2000
WshShell.SendKeys "+{TAB}"
WScript.Sleep 2000
WshShell.SendKeys "+{TAB}"
WScript.Sleep 2000
WshShell.SendKeys "{ENTER}"
WScript.Sleep 40000
WshShell.SendKeys "+{TAB}"
WScript.Sleep 2000
WshShell.SendKeys "{ENTER}"