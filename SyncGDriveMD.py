import os
import webbrowser
from tkinter import messagebox

filename = 'put_md_url_here.txt'

if os.path.getsize(filename) > 0:
    with open(filename) as file:
        md_url = file.read().strip()

    try:
        webbrowser.open(md_url)
        print(f"Opening URL: {md_url}")
    except webbrowser.Error:
        print("Invalid URL. Please check and try again.")
else:
    messagebox.showerror("Error", "Please check your md_url file for a valid URL.")
