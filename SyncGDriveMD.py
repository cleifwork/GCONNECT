import os
import time
import subprocess
import webbrowser
import win32com.client as win32
from tkinter import messagebox

filename = 'put_md_url_here.txt'

if os.path.getsize(filename) > 0:
    with open(filename) as file:
        md_url = file.read().strip()

    try:
        webbrowser.open(md_url)
        print(f"Opening URL: {md_url}")

        # Create WScript Shell Object to access filesystem.
        WshShell = win32.Dispatch("WScript.Shell")

        # Allocate 5 seconds loading time before closing the tab
        time.sleep(5)
        WshShell.SendKeys("^w")

    except webbrowser.Error:
        print("Invalid URL. Please check and try again.")
else:
    messagebox.showerror("Error", "Please check 'put_md_url_here.txt' for a valid URL.")

    # Open text file after the error
    subprocess.run(['notepad.exe', filename], check=True)
    exit()
