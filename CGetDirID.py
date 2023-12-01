from google.oauth2 import service_account
from googleapiclient.discovery import build
import webbrowser

# Path to the service account key JSON file
credentials_path = 'service_account.json'

# Google Drive API scope and version
SCOPES = ['https://www.googleapis.com/auth/drive.file']
API_VERSION = 'v3'

# Create credentials
credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=SCOPES)

# Create Google Drive API service
drive_service = build('drive', API_VERSION, credentials=credentials)

def find_folder_id(folder_name, parent_id=None):
    # Search for a folder with the given name in the specified parent folder
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
    if parent_id:
        query += f" and '{parent_id}' in parents"

    folders = drive_service.files().list(q=query).execute().get('files', [])
    return folders[0]['id'] if folders else None

def create_folder(folder_name, parent_id=None):
    existing_folder_id = find_folder_id(folder_name, parent_id)
    if existing_folder_id:
        return existing_folder_id

    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id] if parent_id else None
    }

    folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
    return folder.get('id')

def share_folder(folder_id):
    drive_service.permissions().create(
        fileId=folder_id,
        body={'type': 'anyone', 'role': 'writer'},
        fields='id'
    ).execute()

def save_folder_id_to_file(folder_id):
    with open('put_folder_id_here.txt', 'w') as file:
        file.write(folder_id)

# Create the main folder 'VWIFI-MAIN' or use existing if present
main_folder_id = create_folder('VWIFI-MAIN')

# Create the subfolder 'vouchers' inside 'VWIFI-MAIN' or use existing if present
subfolder_id = create_folder('vouchers', parent_id=main_folder_id)

# Share both folders with anyone with the link and writer role
share_folder(main_folder_id)
share_folder(subfolder_id)

# Save the main folder ID to the text file
save_folder_id_to_file(subfolder_id)

url = f"https://drive.google.com/drive/u/0/folders/{subfolder_id}"
webbrowser.open(url)
