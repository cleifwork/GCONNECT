import os

def load_desktop_path():
    try:
        with open("desktop_path.txt", "r") as file:
            return os.path.expandvars(file.read().strip())
    except FileNotFoundError:
        raise FileNotFoundError("Error: 'desktop_path.txt' not found!")
    except Exception as e:
        raise Exception(f"Failed to load desktop path: {e}")

# import csv
# import time
# import subprocess
# from tkinter import messagebox

# # 1. Desktop Path Retrieval
# def load_desktop_path():
#     """Load the desktop path from a file or default to the user's Desktop."""
#     try:
#         with open("desktop_path.txt", "r") as file:
#             return file.read().strip()
#     except FileNotFoundError:
#         raise FileNotFoundError("Error: 'desktop_path.txt' not found!")
#     except Exception as e:
#         raise Exception(f"Failed to load desktop path: {e}")

# # 2. File Validation
# def ensure_file_exists(file_path, error_message, actions=None):
#     """Ensure a file exists or raise an error."""
#     if not os.path.isfile(file_path):
#         if actions:
#             for action in actions:
#                 action()
#         raise FileNotFoundError(error_message)

# def ensure_non_empty(file_path, error_message, actions=None):
#     """Ensure a file is not empty or raise an error."""
#     ensure_file_exists(file_path, error_message, actions)
#     with open(file_path, "r") as file:
#         content = file.read().strip()
#         if not content:
#             if actions:
#                 for action in actions:
#                     action()
#             raise ValueError(error_message)
#         return content

# # 3. CSV Processing
# def read_csv(file_path):
#     """Read a CSV file and return a list of dictionaries."""
#     ensure_file_exists(file_path, f"CSV file {file_path} not found.")
#     with open(file_path, "r") as file:
#         return list(csv.DictReader(file))

# def write_csv(data, file_path):
#     """Write data to a CSV file."""
#     keys = data[0].keys()
#     with open(file_path, "w", newline="") as file:
#         writer = csv.DictWriter(file, fieldnames=keys)
#         writer.writeheader()
#         writer.writerows(data)

# # 4. Logging
# def log(message, delay=1):
#     """Log a message to the console with an optional delay."""
#     print(message)
#     time.sleep(delay)

# # 5. Common Actions
# def open_with_notepad(file_path):
#     """Open a file with Notepad."""
#     subprocess.run(['notepad.exe', file_path], check=True)

# def open_folder(folder_path):
#     """Open a folder using the default file explorer."""
#     os.startfile(folder_path)

# # 6. Reusable Google Drive Utilities (Optional)
# # If this functionality is shared across multiple scripts, include it here.
# # You can import your existing GoogleDriveManager class or refactor it to be part of utils.py.

# # Example utility to create a Google Drive service
# from google.oauth2 import service_account
# from googleapiclient.discovery import build

# def create_drive_service(credentials_path, scopes=None):
#     """Create a Google Drive service."""
#     if scopes is None:
#         scopes = ["https://www.googleapis.com/auth/drive"]
#     credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=scopes)
#     return build("drive", "v3", credentials=credentials)
