import os
import time
import subprocess
import webbrowser
from tkinter import messagebox
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# List to store error messages and actions
error_messages = []
actions_to_take = []

# Check 1: Check if "service_account.json" is present
if not os.path.isfile("service_account.json"):
    error_messages.append("Please add 'service_account.json' to your root folder.")
    folder_path = os.path.join(os.path.expanduser("~"), "Desktop", "GCONNECT")
    actions_to_take.append(lambda: os.startfile(folder_path))

# Check 2: Check if "put_api_key_here.txt" is not empty
if os.path.isfile("put_api_key_here.txt"):
    with open("put_api_key_here.txt", "r") as api_key_file:
        api_key = api_key_file.read().strip()

    if not api_key:
        error_messages.append("Please add your GDrive API Key to 'put_api_key_here.txt'")
        text_file_path = "put_api_key_here.txt"
        actions_to_take.append(lambda: subprocess.run(['notepad.exe', text_file_path], check=True))
else:
    error_messages.append("The file 'put_api_key_here.txt' is missing.")

# Display all error messages in a single prompt
if error_messages:
    error_message = "\n".join(error_messages)
    messagebox.showerror("Error", error_message)

    # Execute actions
    for action in actions_to_take:
        action()

    exit()

# Continue with the rest of your script if all checks pass
print("All initial checks passed. Proceeding...")
time.sleep(1)

class GoogleDriveManager:
    def __init__(self, credentials_path='service_account.json'):
        self.credentials_path = credentials_path
        self.SCOPES = ['https://www.googleapis.com/auth/drive.file']
        self.API_VERSION = 'v3'
        self.credentials = service_account.Credentials.from_service_account_file(self.credentials_path, scopes=self.SCOPES)
        self.drive_service = build('drive', self.API_VERSION, credentials=self.credentials)

    def create_and_share_folder(self, folder_name, parent_id=None, role='writer'):
        folder_id = self.find_folder_id(folder_name, parent_id)
        if not folder_id:
            folder_id = self.create_folder(folder_name, parent_id)

        self.share_folder(folder_id, role=role)

        return folder_id

    def find_folder_id(self, folder_name, parent_id=None):
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
        if parent_id:
            query += f" and '{parent_id}' in parents"

        folders = self.drive_service.files().list(q=query).execute().get('files', [])
        return folders[0]['id'] if folders else None

    def create_folder(self, folder_name, parent_id=None):
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id] if parent_id else None
        }

        folder = self.drive_service.files().create(body=folder_metadata, fields='id').execute()
        return folder.get('id')

    def share_folder(self, folder_id, role='writer'):
        self.drive_service.permissions().create(
            fileId=folder_id,
            body={'type': 'anyone', 'role': role},
            fields='id'
        ).execute()

    def save_folder_id_to_file(self, folder_id, file_name):
        with open(file_name, 'w') as file:
            file.write(folder_id)

    def create_drive_service(self, credentials_file):
        credentials = service_account.Credentials.from_service_account_file(credentials_file, scopes=["https://www.googleapis.com/auth/drive"])
        return build("drive", "v3", credentials=credentials)

    def upload_file(self, service, file_path, folder_id):
        file_name = os.path.basename(file_path)
        existing_file_id = self.get_file_id(service, file_name, folder_id)

        if existing_file_id:
            media = MediaFileUpload(file_path, resumable=True)
            file = service.files().update(fileId=existing_file_id, media_body=media).execute()
            print(f"Updated '{file_name}' in GDrive with ID: {file['id']}")
        else:
            file_metadata = {
                "name": file_name,
                "parents": [folder_id]
            }
            media = MediaFileUpload(file_path, resumable=True)
            file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
            print(f"Uploaded '{file_name}' to GDrive with ID: {file['id']}")

        service.permissions().create(
            fileId=file["id"],
            body={"role": "writer", "type": "anyone", "withLink": True},
            fields="id"
        ).execute()

    def get_file_id(self, service, file_name, folder_id):
        results = service.files().list(q=f"'{folder_id}' in parents and name = '{file_name}'", fields="files(id)").execute()
        items = results.get('files', [])
        return items[0]['id'] if items else None

    def list_files_in_folder(self, service, folder_id, output_file):
        try:
            results = service.files().list(
                q=f"'{folder_id}' in parents",
                fields="files(id, name)"
            ).execute()

            files = results.get('files', [])

            if not files:
                messagebox.showwarning("Error", "Specified folder does not contain any files.")
                return

            reversed_files = reversed(files)

            with open(output_file, 'w') as file:
                for file_info in reversed_files:
                    file.write(f"{file_info['id']}\n")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    manager = GoogleDriveManager()

    # 1st Task
    main_folder_name_file = 'main_folder_name.txt'

    # Check if the file exists
    if os.path.exists(main_folder_name_file):
        with open(main_folder_name_file, 'r') as file:
            main_folder_name = file.read().strip()
    else:
        print(f"Error: The file {main_folder_name_file} does not exist.")
        # Handle the error or exit the program as needed

    vouchers_folder_name = 'vouchers'

    main_folder_id = manager.create_and_share_folder(main_folder_name, role='writer')
    subfolder_id = manager.create_and_share_folder(vouchers_folder_name, parent_id=main_folder_id)
    manager.save_folder_id_to_file(subfolder_id, 'put_folder_id_here.txt')
    manager.save_folder_id_to_file(main_folder_id, 'main_folder_id.txt')
    print(f"{main_folder_name} folder and {vouchers_folder_name} folder successfully created...\n")
    time.sleep(1)

    # 2nd Task
    credentials_file = "service_account.json"
    with open('put_folder_id_here.txt', 'r') as file:
        destination_folder_id = file.read().strip()

    service = manager.create_drive_service(credentials_file)
    upload_files = ["5php_vouchers.txt", "10php_vouchers.txt", "15php_vouchers.txt", "20php_vouchers.txt",
                    "30php_vouchers.txt", "50php_vouchers.txt", "99php_vouchers.txt"]

    for upload_file_path in upload_files:
        manager.upload_file(service, upload_file_path, destination_folder_id)

    manager.list_files_in_folder(service, destination_folder_id, 'put_file_ids_here.txt')
    print("Voucher codes successfully uploaded...")
    time.sleep(1)

    # 3rd Task
    file_ids_path = 'put_file_ids_here.txt'
    api_key_path = 'put_api_key_here.txt'
    source_file_path = 'temp.macro'
    modified_macro_file_path = 'VWiFi_Name_-_GCash.macro'

    if not (os.path.exists(file_ids_path) and os.path.exists(api_key_path) and os.path.exists(source_file_path)):
        messagebox.showwarning("Error", "One or more source files do not exist.")
    else:
        with open(file_ids_path, 'r') as file:
            file_ids = [line.strip() for line in file]

        with open(api_key_path, 'r') as api_key_file:
            api_key = api_key_file.read().strip()

        with open(source_file_path, 'r') as file:
            original_content = file.read()

        modified_content = original_content
        for file_id in file_ids:
            modified_content = modified_content.replace("PASTE_FILE_ID_HERE", file_id, 1)

        modified_content = modified_content.strip()
        modified_content = modified_content.replace("PASTE_API_KEY_HERE", api_key)

        if modified_content == original_content:
            messagebox.showwarning("Warning", "Seems like File IDs and API Key are already added...")
        else:
            print("\nConfiguring your macro, please wait...")

            with open(modified_macro_file_path, 'w') as file:
                file.write(modified_content)

            file_metadata = {'name': os.path.basename(modified_macro_file_path)}
            media = MediaFileUpload(modified_macro_file_path, resumable=True)

            existing_files = manager.drive_service.files().list(
                q=f"name='{file_metadata['name']}' and '{main_folder_id}' in parents"
            ).execute().get('files', [])

            if existing_files:
                existing_file_id = existing_files[0]['id']
                
                # Get the parents of the existing file
                existing_parents = manager.drive_service.files().get(
                    fileId=existing_file_id, fields="parents"
                ).execute().get('parents', [])

                # Convert the list of parents to a string
                existing_parents_str = ",".join(existing_parents)

                updated_file = manager.drive_service.files().update(
                    fileId=existing_file_id, media_body=media,
                    addParents=main_folder_id, removeParents=existing_parents_str
                ).execute()
                print(f"Macro successfully updated with ID: {updated_file['id']}")
            else:
                uploaded_file = manager.drive_service.files().create(
                    body={**file_metadata, 'parents': [main_folder_id]},
                    media_body=media, fields='id, webContentLink'
                ).execute()

                manager.drive_service.permissions().create(
                    fileId=uploaded_file['id'],
                    body={'type': 'anyone', 'role': 'writer'},
                    fields='id'
                ).execute()

                print("New macro was successfully configured with ID:", uploaded_file['id'])
                time.sleep(1)

            print("\nOpening macro download folder...")
            time.sleep(3)

            with open('main_folder_id.txt', 'r') as file:
                folder_id = file.read().strip()
                url = f"https://drive.google.com/drive/u/0/folders/{folder_id}"

            webbrowser.open(url)
