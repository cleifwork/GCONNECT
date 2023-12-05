import os
import time
import webbrowser
from tkinter import messagebox
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Initialize Google Drive service
credentials_path = 'service_account.json'
SCOPES = ['https://www.googleapis.com/auth/drive.file']
API_VERSION = 'v3'
credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
drive_service = build('drive', API_VERSION, credentials=credentials)

# Paths to the source files
file_ids_path = 'put_file_ids_here.txt'
api_key_path = 'put_api_key_here.txt'
source_file_path = 'VWiFi_Name_-_GCash.macro'

# Check if source files exist
if not (os.path.exists(file_ids_path) and os.path.exists(api_key_path) and os.path.exists(source_file_path)):
    messagebox.showwarning("Error", "One or more source files do not exist.")
else:
    # Read FILE_IDs from the first text file
    with open(file_ids_path, 'r') as file:
        file_ids = [line.strip() for line in file]

    # Read the API key from the 'put_api_key_here.txt' file
    with open(api_key_path, 'r') as api_key_file:
        api_key = api_key_file.read().strip()

    # Read the content of the second text file
    with open(source_file_path, 'r') as file:
        original_content = file.read()

    # Replace "PASTE_FILE_ID_HERE" with each extracted FILE_ID
    modified_content = original_content
    for file_id in file_ids:
        # Replace only the first occurrence of "PASTE_FILE_ID_HERE"
        modified_content = modified_content.replace("PASTE_FILE_ID_HERE", file_id, 1)

    # Replace all occurrences of "PASTE_YOUR_KEY_HERE" with the API key
    modified_content = modified_content.strip()
    modified_content = modified_content.replace("PASTE_API_KEY_HERE", api_key)

    # Check if any replacements were made
    if modified_content == original_content:
        messagebox.showwarning("Warning", "Seems like File IDs and API Key are already added...")
    else:
        print("Processing please wait...")

        # Write the modified content back to the second text file
        with open(source_file_path, 'w') as file:
            file.write(modified_content)

        # Open the text file and read the content
        with open('main_folder_id.txt', 'r') as file:
            # Read the content and remove any leading or trailing whitespace
            main_folder_id = file.read().strip()

        # Check if the file 'VWiFi_Name_-_GCash.macro' already exists in Google Drive
        file_path = 'VWiFi_Name_-_GCash.macro'
        file_metadata = {'name': os.path.basename(file_path), 'parents': [main_folder_id]}
        existing_files = drive_service.files().list(q=f"name='{file_metadata['name']}' and '{main_folder_id}' in parents").execute().get('files', [])

        if existing_files:
            # The file already exists, update its content
            existing_file_id = existing_files[0]['id']
            media = MediaFileUpload(file_path, resumable=True)
            drive_service.files().update(fileId=existing_file_id, media_body=media).execute()
            print(f"Macro successfully updated in GDrive with ID: {existing_file_id}")
        else:
            # The file does not exist, create a new one
            media = MediaFileUpload(file_path, resumable=True)
            uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id, webContentLink').execute()

            # Share the file with anyone with the link and writer role
            drive_service.permissions().create(
                fileId=uploaded_file['id'],
                body={'type': 'anyone', 'role': 'writer'},
                fields='id'
            ).execute()

            print("New macro successfully pushed to GDrive!")
            time.sleep(1)

        print("Launching download link...")
        time.sleep(2)      

        # Open the text file and read the content
        with open('main_folder_id.txt', 'r') as file:
            # Read the content and remove any leading or trailing whitespace
            folder_id = file.read().strip()
            url = f"https://drive.google.com/drive/u/0/folders/{folder_id}"

        # Open the web browser to the Google Drive folder URL
        webbrowser.open(url)
