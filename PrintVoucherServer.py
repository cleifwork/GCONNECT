import os
import sys
import time
import subprocess
from tkinter import messagebox
import win32com.client as win32

# Check if VoucherList.csv is present in the root folder
if not os.path.isfile("VoucherList.csv"):
    # If not found, check the raw_csv folder
    raw_csv_path = os.path.join("raw_csv", "VoucherList.csv")
    if not os.path.isfile(raw_csv_path):
        # If still not found, display an error message
        messagebox.showerror("Error", "No 'VoucherList.csv' file found! \nPlease run 'EXTRUP + SYNC' first.")
        sys.exit()

# Check if http-server is already running
if "node.exe" in subprocess.check_output('tasklist /FI "IMAGENAME eq node.exe" 2>NUL', shell=True).decode('utf-8'):
    print("http-server is already running. Stopping it...")
    subprocess.call('taskkill /F /IM "node.exe" /T >NUL', shell=True)
    time.sleep(2)

# Start http-server
subprocess.Popen('start "" /min cmd /k "http-server"', shell=True)

# Wait for 2 seconds
time.sleep(2)

# Open the URL in the default browser
subprocess.Popen('start "" "http://localhost:8080/PrintVoucher.html"', shell=True)

# Allocate 3 seconds loading time to make sure web form has been rendered completely, allocate higher value for slow internet connection
time.sleep(3)

# Create WScript Shell Object to access filesystem.
WshShell = win32.Dispatch("WScript.Shell")

# Select, or bring Focus to a window named `Google Chrome`
WshShell.AppActivate("Google Chrome")

# Wait for 2 sec then press Ctrl+P to open print window
time.sleep(2)
WshShell.SendKeys("^p")
