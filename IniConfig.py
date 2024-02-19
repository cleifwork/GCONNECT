import os
import re
import csv
import glob
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

# Initial Checks
for file_name in ["service_account.json", "put_api_key_here.txt"]:
    if not os.path.isfile(file_name):
        error_messages.append(f"Please add '{file_name}' to your root folder.")
        actions_to_take.append(lambda: os.startfile(os.path.join(os.path.expanduser("~"), "Desktop", "GCONNECT")))

    elif file_name == "put_api_key_here.txt":
        with open(file_name, "r") as api_key_file:
            api_key = api_key_file.read().strip()

        if not api_key:
            error_messages.append("Please add your GDrive API Key to 'put_api_key_here.txt'")
            text_file_path = "put_api_key_here.txt"
            actions_to_take.append(lambda: subprocess.run(['notepad.exe', text_file_path], check=True))

# Display all error messages in a single prompt
if error_messages:
    error_message = "\n".join(error_messages)
    messagebox.showerror("Error", error_message)

    # Execute actions
    for action in actions_to_take:
        action()

    exit()

# Continue with the rest of your script if all checks pass
print("All initial checks passed. Proceeding...\n")
time.sleep(1)

# Creating CSV processing function for better readability
def process_csv(csv_file):
    unique_prices = set()
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            price = ''.join(char for char in row["Price"] if char.isdigit())
            if price:
                unique_prices.add(price)

    if not unique_prices:
        messagebox.showerror("Error", f"No valid prices found in the CSV file: {csv_file}.")
    else:
        with open("put_voucher_amt_here.txt", "w") as output_file:
            output_file.write("\n".join(map(str, sorted(unique_prices, key=int))))
            print("Successfully added voucher prices from the CSV file!")
            time.sleep(1)

# Read the amounts from the input file "put_voucher_amt_here.txt"
with open("put_voucher_amt_here.txt", "r") as input_file:
    amounts = [line.strip() for line in input_file]

# Check if the amounts list is empty
if not amounts:
    print("The input file is empty. Proceed getting prices from the CSV file...")
    time.sleep(1)

    # Get the folder name from the file
    main_folder_name_file = 'main_folder_name.txt'

    # Check if the file exists
    if os.path.exists(main_folder_name_file):
        with open(main_folder_name_file, 'r') as file:
            app_name = file.read().strip()

        # Check if app_name is empty
        if not app_name:
            print(f"Error: The folder name in {main_folder_name_file} is empty.")
            # Handle the error or exit the program as needed
    else:
        print(f"Error: The file {main_folder_name_file} does not exist.")
        # Handle the error or exit the program as needed

    # Specify the directory where the CSV file is located
    directory = os.path.join(os.environ['USERPROFILE'], 'Desktop', app_name, 'raw_csv')

    # Search for CSV files in the directory
    csv_files = glob.glob(os.path.join(directory, '*.csv'))

    # Check if there are CSV files in the directory
    if not csv_files:
        error_message = "Please provide voucher amounts in 'put_voucher_amt_here.txt'."
        messagebox.showerror("Error", error_message)

        # Open the file for editing
        file_path = "put_voucher_amt_here.txt"
        os.system(f"notepad.exe {file_path}")

        exit()
    else:
        # Take the first CSV file found
        csv_file = csv_files[0]
        print(f"Processing CSV file: '{csv_file}'...")
        time.sleep(1)
        process_csv(csv_file)

        # Re-read the amounts from the input file "put_voucher_amt_here.txt"
        with open("put_voucher_amt_here.txt", "r") as input_file:
            amounts = [line.strip() for line in input_file]
else:
    # Check if all elements in the amounts list are numbers
    if not all(amount.isdigit() for amount in amounts):
        messagebox.showerror("Error", "Please provide valid voucher amounts.")

        # Open the file for editing
        file_path = "put_voucher_amt_here.txt"
        os.system(f"notepad.exe {file_path}")

        exit()

# Create text files based on the amounts
with open("voucher_logger.txt", "w") as logger_file:
    for amount in amounts:
        # Create the file name
        file_name = f"{amount}php_vouchers.txt"

        # Write content to the file (you can customize this part based on your requirements)
        with open(file_name, "w") as output_file:
            output_file.write(f"This file will contain {amount} PHP vouchers.")

        # Write the file_name to the logger file
        logger_file.write(f"{file_name}\n")

print("Voucher files and logger created successfully!")

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

    # 1ST TASK
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
    print(f"{main_folder_name} folder and {vouchers_folder_name} folder successfully created!\n")
    time.sleep(1)

    # 2ND TASK
    credentials_file = "service_account.json"
    with open('put_folder_id_here.txt', 'r') as file:
        destination_folder_id = file.read().strip()

    service = manager.create_drive_service(credentials_file)
    
    # Read voucher filenames from voucher_logger.txt
    voucher_filenames_file = 'voucher_logger.txt'
    with open(voucher_filenames_file, 'r') as file:
        voucher_files = [line.strip() for line in file]

    for upload_file_path in voucher_files:
        manager.upload_file(service, upload_file_path, destination_folder_id)

    manager.list_files_in_folder(service, destination_folder_id, 'put_file_ids_here.txt')
    print("Voucher files successfully uploaded!")
    time.sleep(1)

    # 3RD TASK
    def check_file_vcodlen(filename):
        # Check if the specified file exists
        if os.path.isfile(filename):
            # Open the file and read its content
            with open(filename, 'r') as file:
                content = file.read().strip()
                
                # Check if the content is empty
                if not content:
                    print("The file 'put_vcodlen_here.txt' is empty. \nProceed checking for exported vouchers in CSV file...")
                    time.sleep(1)
                    check_csv_file()
                
                # Check if the content is a digit and within the range 6-9
                elif content.isdigit() and 6 <= int(content) <= 9:
                    # Call the function replace_str_in_temp_macro with the content as an argument
                    replace_str_in_temp_macro(content)
                
                # Check if the content is a digit and equals 10
                elif content.isdigit() and int(content) == 10:
                    # Ignore and proceed to the next process (do nothing)
                    pass
                
                # If the content is not a valid voucher code length, show an error message
                else:
                    messagebox.showerror("Error", "Specify valid voucher code length in 'put_vcodlen_here.txt'.")
                    exit()
        
        # If the specified file does not exist
        else:
            # Print a message and proceed to check for exported vouchers CSV file
            print("The file 'put_vcodlen_here.txt' does not exist. \nProceed checking for exported vouchers in CSV file...")
            time.sleep(1)
            check_csv_file()

    def replace_str_in_temp_macro(value):
        with open(modified_macro_file_path, 'r') as temp_file:
            content = temp_file.read()
            updated_content = content.replace(r"\w{10}", fr"\w{{{value}}}")
        
        with open(modified_macro_file_path, 'w') as temp_file:
            temp_file.write(updated_content)

    # Function to check the first CSV file found in a specific folder
    def check_csv_file():
        # Construct the path to the folder containing the CSV files
        csv_folder_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'GCONNECT', 'raw_csv')

        # Check if the CSV folder exists
        if os.path.exists(csv_folder_path):
            # Find all CSV files in the folder
            csv_files = [f for f in os.listdir(csv_folder_path) if f.endswith('.csv')]

            # Check if CSV files are found
            if csv_files:
                # Take the first CSV file
                csv_file = csv_files[0]

                # Call the function to check the specific CSV file
                check_csv_str_len(csv_file)
            else:
                # Display an error message if no CSV files are found
                print("Error: No .csv file found!")
                exit()
        else:
            # Print an error message if the CSV folder path does not exist
            print("Error: CSV folder path does not exist!")
            exit()

    # Function to check a specific CSV file
    def check_csv_str_len(csv_file):
        # Construct the full path to the CSV file
        csv_file_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'GCONNECT', 'raw_csv', csv_file)

        # Read the first 11 lines of the "code" column in the CSV file
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            lines = [row["Code"].strip() for _, row in zip(range(11), reader)]

        # Determine the maximum string length
        max_strlen = max(len(code) for code in lines)

        # Check if a maximum length is found
        if max_strlen:
            # Read the content of the "temp.macro" file
            with open(modified_macro_file_path, 'r') as temp_file:
                content = temp_file.read()

                # Update the content by replacing a specific pattern
                updated_content = content.replace(r"\w{10}", fr"\w{{{max_strlen}}}")

            # Write the updated content back to the "temp.macro" file
            with open(modified_macro_file_path, 'w') as temp_file:
                temp_file.write(updated_content)

    # 3rd Task : Function to read lines from a file and handle FileNotFoundError
    def read_file_lines(file_path):
        try:
            with open(file_path, 'r') as file:
                return [line.strip() for line in file]
        except FileNotFoundError:
            messagebox.showwarning("Error", f"File not found: {file_path}")
            exit()
        
    # File paths for source files and destination macro file
    file_ids_path = 'put_file_ids_here.txt'
    api_key_path = 'put_api_key_here.txt'
    voucher_amt_path = 'put_voucher_amt_here.txt'
    source_file_path = 'temp.macro'
    modified_macro_file_path = 'GConnect_-_GCash.macro'

    # Read content from source files
    file_ids = read_file_lines(file_ids_path)
    api_key = read_file_lines(api_key_path)
    original_content = read_file_lines(source_file_path)
    voucher_amounts = read_file_lines(voucher_amt_path)

    # Check if all source files exist
    if not (file_ids and api_key and original_content):
        messagebox.showwarning("Error", "One or more source files do not exist!")
    else:
        modified_content = original_content[0]

        # Replace placeholders with actual content
        for file_id in file_ids:
            modified_content = modified_content.replace("PASTE_FILE_ID_HERE", file_id, 1)

        modified_content = modified_content.replace("PASTE_API_KEY_HERE", api_key[0])

        with open(voucher_amt_path, "r") as amount_file:
            voucher_amounts = [line.strip() for line in amount_file]

        # Define patterns and replacements
        patterns_and_replacements = [
            (fr"\bVCOD_{i}\b", f"VCOD_{voucher_amounts[i-1] if i <= len(voucher_amounts) else i}") for i in range(9, 0, -1)
        ] + [
            (fr"\b{i}PHP\b", f"{voucher_amounts[i-1] if i <= len(voucher_amounts) else i}PHP") for i in range(9, 0, -1)
        ] + [
            (fr"\bPHP{i}\b", f"PHP{voucher_amounts[i-1] if i <= len(voucher_amounts) else i}") for i in range(9, 0, -1)
        ] + [
            (fr"\bPHP {i}.00\b", f"PHP {voucher_amounts[i-1] if i <= len(voucher_amounts) else i}.00") for i in range(9, 0, -1)
        ]

        print("\nConfiguring your macro, please wait...")
        time.sleep(1)

        # Perform replacements in modified_content
        for search_pattern, replace_pattern in patterns_and_replacements:
            modified_content = re.sub(search_pattern, replace_pattern, modified_content)

        # Write the modified content back to GConnect_-_GCash.macro
        with open(modified_macro_file_path, "w") as macro_file:
            macro_file.write(modified_content)

        check_file_vcodlen("put_vcodlen_here.txt") 

        print("Macro configuration completed successfully!")
        time.sleep(1)      

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
