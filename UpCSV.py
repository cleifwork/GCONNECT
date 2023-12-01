import os
import time
from tkinter import messagebox
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

# Replace 'credentials.json' with the path to your service account key JSON file
credentials_file = "service_account.json"

# Open the text file and read the content
with open('put_folder_id_here.txt', 'r') as file:
    # Read the content and remove any leading or trailing whitespace
    destination_folder_id = file.read().strip()

# Define the function to authenticate and create a Drive service
def create_drive_service():
    credentials = service_account.Credentials.from_service_account_file(credentials_file, scopes=["https://www.googleapis.com/auth/drive"])
    return build("drive", "v3", credentials=credentials)

output_file5 = "5php_vouchers.txt"
output_file10 = "10php_vouchers.txt"
output_file15 = "15php_vouchers.txt"
output_file20 = "20php_vouchers.txt"
output_file30 = "30php_vouchers.txt"
output_file50 = "50php_vouchers.txt"
output_file99 = "99php_vouchers.txt"

def main():
    service = create_drive_service()

    # Upload the output files to Google Drive
    upload_files = [output_file5, output_file10, output_file15, output_file20,
                    output_file30, output_file50, output_file99]

    for upload_file_path in upload_files:
        upload_file(service, upload_file_path, destination_folder_id)

def upload_file(service, file_path, folder_id):
    file_name = os.path.basename(file_path)
    existing_file_id = get_file_id(service, file_name, folder_id)
    
    if existing_file_id:
        # If the file exists, update its content
        media = MediaFileUpload(file_path, resumable=True)
        file = service.files().update(fileId=existing_file_id, media_body=media).execute()
        print(f"Updated '{file_name}' in Google Drive with ID: {file['id']}")
    else:
        # If the file does not exist, create a new one
        file_metadata = {
            "name": file_name,
            "parents": [folder_id]
        }
        media = MediaFileUpload(file_path, resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        print(f"Uploaded '{file_name}' to Google Drive with ID: {file['id']}")

    # Set the permission to anyone with the link
    service.permissions().create(
        fileId=file["id"],
        body={"role": "reader", "type": "anyone", "withLink": True},
        fields="id"
    ).execute()

def get_file_id(service, file_name, folder_id):
    # Retrieve the file ID by name in the specified folder
    results = service.files().list(q=f"'{folder_id}' in parents and name = '{file_name}'", fields="files(id)").execute()
    items = results.get('files', [])
    return items[0]['id'] if items else None

if __name__ == "__main__":
    main()

def list_files_in_folder(service, folder_id, output_file):
    try:
        # List files in the folder
        results = service.files().list(
            q=f"'{folder_id}' in parents",
            fields="files(id, name)"
        ).execute()

        files = results.get('files', [])

        # Check if the folder contains any files
        if not files:
            messagebox.showwarning("Error", "Specified folder does not contain any files.")
            return

        # Reverse the order of files
        reversed_files = reversed(files)

        # Write only file_ids to the text file
        with open(output_file, 'w') as file:
            for file_info in reversed_files:
                file.write(f"{file_info['id']}\n")

    except Exception as e:
        print(f"An error occurred: {e}")

# Write file_ids to text file
output_file = 'put_file_ids_here.txt'

# Create the service and list files
service = create_drive_service()
list_files_in_folder(service, destination_folder_id, output_file)

print("\nDone...")
time.sleep(1)

print("Exiting process...")
time.sleep(1)
