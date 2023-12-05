
import time
import webbrowser
from tkinter import messagebox
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to the service account key JSON file
credentials_path = 'service_account.json'

# Google Drive API scope and version
SCOPES = ['https://www.googleapis.com/auth/drive.file']
API_VERSION = 'v3'

# Create credentials
credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=SCOPES)

# Create Google Drive API service
drive_service = build('drive', API_VERSION, credentials=credentials)

def create_and_share_folder(folder_name, parent_id=None, role='writer'):
    # Create or get the folder ID
    folder_id = find_folder_id(folder_name, parent_id)
    if not folder_id:
        folder_id = create_folder(folder_name, parent_id)

    # Share the folder with anyone with the link and the specified role
    share_folder(folder_id, role=role)

    return folder_id

def find_folder_id(folder_name, parent_id=None):
    # Search for a folder with the given name in the specified parent folder
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
    if parent_id:
        query += f" and '{parent_id}' in parents"

    folders = drive_service.files().list(q=query).execute().get('files', [])
    return folders[0]['id'] if folders else None

def create_folder(folder_name, parent_id=None):
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id] if parent_id else None
    }

    folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
    return folder.get('id')

def share_folder(folder_id, role='writer'):
    drive_service.permissions().create(
        fileId=folder_id,
        body={'type': 'anyone', 'role': role},
        fields='id'
    ).execute()

def save_folder_id_to_file(folder_id, file_name):
    with open(file_name, 'w') as file:
        file.write(folder_id)

# Create and share the main folder 'VWIFI-MAIN'
main_folder_id = create_and_share_folder('VWIFI-MAIN', role='writer')

# Create and share the subfolder 'vouchers' inside 'VWIFI-MAIN'
subfolder_id = create_and_share_folder('vouchers', parent_id=main_folder_id)

# Save the subfolder 'vouchers' ID to the text file
save_folder_id_to_file(subfolder_id, 'put_folder_id_here.txt')

# Save the main folder 'VWIFI-MAIN' ID to the text file
save_folder_id_to_file(main_folder_id, 'main_folder_id.txt')

messagebox.showinfo("Success", "Main folder and voucher folder successfully created...")

print("Opening voucher folder...")
time.sleep(2)

url = f"https://drive.google.com/drive/u/0/folders/{subfolder_id}"
webbrowser.open(url)


