import os
import time
import subprocess
from tkinter import messagebox
import win32com.client as win32

# Get the path of the root folder
root_folder = os.getcwd()

# Remove the existing 'VoucherList.csv' file if it exists
voucher_list_path = os.path.join(root_folder, "VoucherList.csv")
if os.path.exists(voucher_list_path):
    os.remove(voucher_list_path)

# List all CSV files in the root folder
csv_files = [file for file in os.listdir(root_folder) if file.endswith('.csv')]

if not os.path.isfile("VoucherList.csv"):
    messagebox.showerror("Error", "No 'VoucherList.csv' file found! \nPlease run 'EXTRUP + SYNC' first.")
    exit()

# Determine the latest CSV file based on modification time
latest_csv_file = max(csv_files, key=lambda x: os.path.getmtime(os.path.join(root_folder, x)))

# Rename the latest CSV file to 'VoucherList.csv'
new_file_name = 'VoucherList.csv'
os.rename(os.path.join(root_folder, latest_csv_file), os.path.join(root_folder, new_file_name))

print(f"The latest CSV file found: {latest_csv_file}")

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
subprocess.Popen('start "" "http://localhost:8080/PVOS.html"', shell=True)

# Allocate 3 seconds loading time to make sure web form has been rendered completely, allocate higher value for slow internet connection
time.sleep(3)

# Create WScript Shell Object to access filesystem.
WshShell = win32.Dispatch("WScript.Shell")

# Select, or bring Focus to a window named `Google Chrome`
WshShell.AppActivate("Google Chrome")

# Wait for 2 sec then press Ctrl+P to open print window
time.sleep(2)
WshShell.SendKeys("^p")
