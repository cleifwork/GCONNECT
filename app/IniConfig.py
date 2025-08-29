import os
import re
import csv
import sys
import glob
import time
import shutil
import subprocess
import webbrowser
import GConnectAPI
from tkinter import messagebox
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from utils import exe_dir, FILE_PATHS, check_file_exists

# Check if any file in csv_folder contains file that ends with .csv
csv_files = glob.glob(os.path.join(FILE_PATHS["csv_folder"], '*.csv'))
skip_api_call = bool(csv_files)

if skip_api_call:
    print("VoucherList CSV already exists. Skipping API call.")
else:
    print("No VoucherList CSV found. Running GConnectAPI...")
    GConnectAPI.main()

# List to store error messages and actions
error_messages = []
actions_to_take = []

# Initial Checks
for file_name, file_path in FILE_PATHS.items():
    if file_name == "service_account" or file_name == "api_key":  # Only check specific files
        if not os.path.isfile(file_path):
            error_messages.append(f"Please add '{os.path.basename(file_path)}' to your root folder.")
            actions_to_take.append(lambda: os.startfile(exe_dir))

        elif file_name == "api_key":  # Check if 'put_api_key_here.txt' is empty
            with open(file_path, "r") as api_key_file:
                api_key = api_key_file.read().strip()

            if not api_key:
                error_messages.append("Please add your GDrive API Key to 'put_api_key_here.txt'")
                actions_to_take.append(lambda: subprocess.run(['notepad.exe', file_path], check=True))

# Display all error messages in a single prompt
if error_messages:
    error_message = "\n".join(error_messages)
    messagebox.showerror("Error", error_message)

    # Execute actions
    for action in actions_to_take:
        action()

    sys.exit()

# Continue with the rest of your script if all checks pass
print("\nAll initial checks passed. Proceeding...\n")
time.sleep(1)


# Backup crucial files that might be overwritten accidentally
def manage_backup_folder():
    # Define the paths for the backup folder and the root folder (current working directory)
    backup_folder = FILE_PATHS['backup_folder']
    os.makedirs(backup_folder, exist_ok=True)

    files_to_backup = [
        FILE_PATHS["service_account"],
        FILE_PATHS["api_key"],
        FILE_PATHS["main_folder_id"],
        FILE_PATHS["sub_folder_id"],
        FILE_PATHS["file_ids"],
        FILE_PATHS["md_url"]
    ]

     # Iterate through the files and back them up
    for file_name in files_to_backup:
        # Check if the source file exists
        error_message = check_file_exists(file_name, f"Error: Source file not found: {file_name}")
        if error_message:
            print(error_message)
            time.sleep(1)
            continue

        # Check if the source file is empty
        if os.path.getsize(file_name) == 0:
            print(f"Skipping backup: {os.path.basename(file_name)} is empty.")
            time.sleep(1)
            continue

        # Construct the destination path in the backup folder
        dest_path = os.path.join(backup_folder, os.path.basename(file_name))

        # Check if the destination file is missing or empty
        if not os.path.exists(dest_path) or os.path.getsize(dest_path) == 0:
            try:
                # Copy the file to the backup folder
                time.sleep(1)
                shutil.copy(file_name, dest_path)
                print(f"Backing up {os.path.basename(file_name)} to {backup_folder}")
            except Exception as e:
                print(f"Error backing up {os.path.basename(file_name)} to {backup_folder}: {e}")
            

# Validate that the required columns exist in the CSV
def validate_csv_columns(csv_file, required_columns):
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        
        # Check if all required columns exist in the CSV file
        missing_columns = [col for col in required_columns if col not in reader.fieldnames]
        if missing_columns:
            messagebox.showerror("Error", f"Missing required columns: {', '.join(missing_columns)}")
            sys.exit()


# Creating CSV processing function for better readability
def process_csv(csv_file):
    # Extract unique voucher data (Price, Duration, Type) from the CSV file and store them in a set
    unique_data = set()
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Extract relevant data from the row
            price = ''.join(char for char in row["Price"] if char.isdigit())
            duration = row["Duration"].replace(".0", " ")
            voucher_type = ''.join(char for char in row["Type"] if char.isdigit())
            notes = row["Notes"]

            # Check if the duration ends with "Hours" and if it's greater than 24 and divisible by 24
            if duration.endswith("Hours") and float(duration[:-5]) > 24 and float(duration[:-5]) % 24 == 0:
                # Calculate the equivalent days            
                days = float(duration[:-5]) / 24

                # Create the duration text for display
                duration_text = f"{int(days)} Days"
            else:
                # If the conditions are not met, use the original duration
                duration_text = f"{duration}"

            # Add data to the set only if the Type is not "Expired" and not for "Printing"
            if price and voucher_type != "" and notes != "PRINT VOUCHER":
                unique_data.add((price, duration_text, voucher_type))

    # Display an error message if no valid data is found in the CSV file
    if not unique_data:
        messagebox.showerror("Error", f"No valid data found in the CSV file: {csv_file}.\nProbably your vouchers are PRINT VOUCHERS!")
        sys.exit()
    elif len(unique_data) > 9:
        messagebox.showerror("Error", "This program can handle up to 9 different voucher price variants.")
        sys.exit()
    else:
        # Write the unique voucher data to a text file and print a success message
        with open(FILE_PATHS["voucher_amt"], "w") as output_file:
            # Use a comma to separate the values in the output file
            output_file.write("\n".join(",".join(map(str, data)) for data in sorted(unique_data, key=lambda x: int(x[0]))))
            print("Successfully added voucher data from the CSV file!")
            time.sleep(1)

# Get the folder name from the file
main_folder_name_file = FILE_PATHS["main_folder_name"]

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
directory = FILE_PATHS["csv_folder"]

# Search for CSV files in the directory
csv_files = glob.glob(os.path.join(directory, '*.csv'))

# Specify the required columns
required_columns = ["Code", "Price", "Duration", "Type"]

# Check if there are CSV files in the directory
if not csv_files:
    error_message = "No CSV file found in your 'raw_csv' folder."
    messagebox.showerror("Error", error_message)
    sys.exit()

# Validate the first CSV file found in the directory
validate_csv_columns(csv_files[0], required_columns)

# Take the first CSV file found
csv_file = csv_files[0]
print(f"Processing CSV file: '{csv_file}'...")
time.sleep(1)
process_csv(csv_file)

# Read the amounts from the input file "put_voucher_amt_here.txt"
with open(FILE_PATHS["voucher_amt"], "r") as input_file:
    # Split each line into a tuple (Price, Duration, Type)
    data = [tuple(line.strip().split(',')) for line in input_file]

# Create text files based on the amounts
with open(FILE_PATHS["voucher_log"], "w") as logger_file:
    for row in data:
        # Extract the Price from the tuple
        amount = row[0]

        # Create the full file path (for writing the content)
        file_path = os.path.join(exe_dir, f"{amount}php_vouchers.txt")

        # Write content to the file (using the full path)
        with open(file_path, "w") as output_file:
            output_file.write(f"This file will contain {amount} PHP vouchers.")        

        # Extract only the filename from the full path
        file_name = os.path.basename(file_path)

        # Append only the filename to the logger file
        logger_file.write(file_name + '\n')

print("Voucher files and logger created successfully!")


class GoogleDriveManager:

    def __init__(self, file_paths):
        # Reference the credentials path from FILE_PATHS
        self.credentials_path = file_paths["service_account"]
  
        self.SCOPES = ['https://www.googleapis.com/auth/drive.file']
        self.API_VERSION = 'v3'

        # Load credentials from the service account file
        self.credentials = service_account.Credentials.from_service_account_file(self.credentials_path, scopes=self.SCOPES)
        
        # Create the Google Drive service
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
        # Ensure the credentials file path is absolute
        credentials_file_path = os.path.join(exe_dir, credentials_file)

        # Check if the credentials file exists
        if not os.path.isfile(credentials_file_path):
            raise FileNotFoundError(f"Service account file not found: {credentials_file_path}")

        # Load credentials and create the Drive service
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file_path,
            scopes=["https://www.googleapis.com/auth/drive"])
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
        return file['id']


    def get_file_id(self, service, file_name, folder_id):
        results = service.files().list(q=f"'{folder_id}' in parents and name = '{file_name}'", fields="files(id)").execute()
        items = results.get('files', [])
        return items[0]['id'] if items else None

if __name__ == "__main__":
    manager = GoogleDriveManager(FILE_PATHS)

    # 1ST TASK
    # Define the path to main_folder_name.txt, which contains the name of the main folder to be created
    def read_file_content(file_path):
        """Reads and returns the content of a file if it exists; otherwise, raises an error."""
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return file.read().strip()  # Strip extra whitespace or newline characters
        else:
            raise FileNotFoundError(f"Error: The file {file_path} does not exist.")

    try:
        # Read folder names from respective files
        main_folder_name = read_file_content(FILE_PATHS["main_folder_name"])
        vouchers_folder_name = read_file_content(FILE_PATHS["sub_folder_name"])

        # Create main folder on Google Drive and share with write permissions
        main_folder_id = manager.create_and_share_folder(main_folder_name, role='writer')

        # Create subfolder inside the main folder
        subfolder_id = manager.create_and_share_folder(vouchers_folder_name, parent_id=main_folder_id)

        # Save folder IDs to respective files
        manager.save_folder_id_to_file(subfolder_id, FILE_PATHS["sub_folder_id"])
        manager.save_folder_id_to_file(main_folder_id, FILE_PATHS["main_folder_id"])

        print(f"{main_folder_name} folder and {vouchers_folder_name} folder successfully created!\n")
        time.sleep(1)

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


    # 2ND TASK
    credentials_file = FILE_PATHS["service_account"]
    with open(FILE_PATHS["sub_folder_id"], 'r') as file:
        destination_folder_id = file.read().strip()

    service = manager.create_drive_service(credentials_file)

    # Read voucher filenames from voucher_logger.txt
    voucher_filenames_file = FILE_PATHS["voucher_log"]
    with open(voucher_filenames_file, 'r') as file:
        voucher_files = [line.strip() for line in file]

    # Construct full paths for the voucher files
    voucher_files_full_paths = [os.path.join(exe_dir, file_name) for file_name in voucher_files]

    # Loop over voucher files and upload each file
    file_ids = []
    for upload_file_path in voucher_files_full_paths:
        if not os.path.isfile(upload_file_path):
            print(f"Error: File {upload_file_path} does not exist.")
            continue
        file_id = manager.upload_file(service, upload_file_path, destination_folder_id)
        file_ids.append(file_id)

    # Write the file IDs to put_file_ids_here.txt
    with open(FILE_PATHS["file_ids"], 'w') as file:
        for file_id in file_ids:
            file.write(f"{file_id}\n")

    print("Voucher files successfully uploaded!")
    time.sleep(1)

    # 3RD TASK
    def get_max_strlen_from_csv(csv_file_path):
        """Reads the 'Code' column from the CSV file and calculates the maximum string length."""
        with open(csv_file_path, 'r') as file:  # Open the CSV file for reading
            reader = csv.DictReader(file)  # Create a dictionary reader for the CSV
            return max(len(row["Code"].strip()) for row in reader)  # Find and return the maximum string length in the 'Code' column


    def replace_str_in_temp_macro(value):
        """Replaces the placeholder in the macro file with the specified value."""
        with open(modified_macro_file_path, 'r') as temp_file:  # Open the macro file for reading
            updated_content = temp_file.read().replace(r"\w{10}", fr"\w{{{value}}}")  # Replace placeholder with the value

        with open(modified_macro_file_path, 'w') as temp_file:  # Open the macro file for writing
            temp_file.write(updated_content)  # Write the updated content to the file


    def check_csv_file():
        """Finds the latest CSV file in the folder and processes it."""
        csv_folder_path = FILE_PATHS['csv_folder']  # Get the path to the folder containing CSV files

        if not os.path.exists(csv_folder_path):  # Check if the folder exists
            print("Error: CSV folder path does not exist!")  # Print an error message if the folder does not exist
            sys.exit()  # Exit the script

        csv_files = [f for f in os.listdir(csv_folder_path) if f.endswith('.csv')]  # List all CSV files in the folder
        if not csv_files:  # If no CSV files are found
            print("Error: No .csv file found!")  # Print an error message
            sys.exit()  # Exit the script

        latest_csv_file = max(csv_files, key=lambda f: os.path.getmtime(os.path.join(csv_folder_path, f)))  # Get the most recently modified CSV file
        check_csv_str_len(os.path.join(csv_folder_path, latest_csv_file))  # Check the string lengths in the latest CSV file


    def check_csv_str_len(csv_file_path):
        """Calculates the maximum string length in the CSV and updates relevant files."""
        max_strlen = get_max_strlen_from_csv(csv_file_path)  # Get the maximum string length from the CSV file

        with open(code_length_path, 'w') as length_file:  # Open the code length file for writing
            length_file.write(str(max_strlen))  # Write the maximum string length to the file

        replace_str_in_temp_macro(max_strlen)  # Update the macro file with the maximum string length
        FILE_PATHS["vcodlen"] = str(max_strlen)  # Update the global file paths dictionary with the string length as a string

    csv_file_path = os.path.join(FILE_PATHS["csv_folder"], csv_file)  # Construct the full path to the CSV file
    max_strlen = get_max_strlen_from_csv(csv_file_path)  


    # Function to read lines from a file and handle FileNotFoundError
    def read_file_lines(file_path):
        try:
            with open(file_path, 'r', encoding="utf-8") as file:
                return [line.strip() for line in file]
        except FileNotFoundError:
            messagebox.showwarning("Error", f"File not found: {file_path}")
            sys.exit()
        
    # File paths for source files and destination macro file (Construct absolute paths)
    file_ids_path = FILE_PATHS["file_ids"]
    api_key_path = FILE_PATHS["api_key"]
    voucher_amt_path = FILE_PATHS["voucher_amt"]
    code_length_path = FILE_PATHS["vcodlen"]
    source_file_path = FILE_PATHS["macro_file"]
    modified_macro_file_path = FILE_PATHS["modified_macro"]

    # Read content from source files
    file_ids = read_file_lines(file_ids_path)
    api_key = read_file_lines(api_key_path)
    original_content = read_file_lines(source_file_path)
    voucher_amounts = read_file_lines(voucher_amt_path)

    # Check if all source files exist
    if not (file_ids and api_key and original_content and voucher_amounts):
        messagebox.showwarning("Error", "One or more source files do not exist!")
    else:
        modified_content = original_content[0]

        # Replace placeholders with actual content for file IDs
        for file_id in file_ids:
            modified_content = modified_content.replace("PASTE_FILE_ID_HERE", file_id, 1)

        # Replace each occurrence of PASTE_API_KEY_HERE with the API key
        for i in range(len(file_ids)): 
            api_key_to_use = api_key[i % len(api_key)]  # Use modulo to cycle through the available API keys
            modified_content = modified_content.replace("PASTE_API_KEY_HERE", api_key_to_use, 1)

        duration_string = '","variable":{"textValue":"0 minutes'
        type_string = '","variable":{"textValue":"0'
        replace_string = '","variable":{"textValue":"'
        s_rcvamt_string = '","variable":{"textValue":"received PHP 0'
        r_rcvamt_string = '","variable":{"textValue":"received PHP '
        s_rcvmya_string = '","variable":{"textValue":"received ₱0'
        r_rcvmya_string = '","variable":{"textValue":"received ₱'        
        s_vamtx_string = '","variable":{"textValue":"Here is your '

        key_string = '{"key":"PHP0'
        vcodkey_string = '{"key":"VCOD_0'
        rcvamt_string = '","variable":{"textValue":"received PHP 0.00","variableType":2,"type":"StringValue"},"variableType":11,"type":"DictionaryEntry"}'
        rcvmya_string = '","variable":{"textValue":"received ₱0.00","variableType":2,"type":"StringValue"},"variableType":11,"type":"DictionaryEntry"}'
        vamtx_string = r'","variable":{"textValue":"Here is your PHP voucher\nCode :","variableType":2,"type":"StringValue"},"variableType":11,"type":"DictionaryEntry"}'
        vchcd_string = '","variable":{"textValue":"","variableType":2,"type":"StringValue"},"variableType":11,"type":"DictionaryEntry"}'
        vdrt_string = '","variable":{"textValue":"0 minutes","variableType":2,"type":"StringValue"},"variableType":11,"type":"DictionaryEntry"}'
        vusr_string = '","variable":{"textValue":"0 device","variableType":2,"type":"StringValue"},"variableType":11,"type":"DictionaryEntry"}'

        macro_action1_path = os.path.join(FILE_PATHS["macro_mod"], 'action_1')
        macro_action2_path = os.path.join(FILE_PATHS["macro_mod"], 'action_2')

        replacements = {}  # Initialize the replacements dictionary
        amount_ids = []  # Initialize list to collect price IDs

        with open(voucher_amt_path, "r", encoding="utf-8") as amount_file:
            for i, line in enumerate(amount_file, start=1):
                price, duration, type = line.strip().split(',')  # Assuming the tuple is Price, Duration, Type

                amount_ids.append(price)  # Collect price (1st column)

                replacements.update({
                    f"VCOD_0{i}": f"VCOD_{price}" if i <= len(voucher_amounts) else f"VCOD_0{i}",
                    f"0{i}PHP": f"{price}PHP" if i <= len(voucher_amounts) else f"0{i}PHP",
                    f"{key_string}{i}{s_rcvamt_string}": f"{key_string}{i}{r_rcvamt_string}{price}" if i <= len(voucher_amounts) else f"{key_string}{i}{s_rcvamt_string}",
                    f"{key_string}{i}{s_rcvmya_string}": f"{key_string}{i}{r_rcvmya_string}{price}" if i <= len(voucher_amounts) else f"{key_string}{i}{s_rcvmya_string}",
                    f"{key_string}{i}{s_vamtx_string}": f"{key_string}{i}{s_vamtx_string}{price}" if i <= len(voucher_amounts) else f"{key_string}{i}{s_vamtx_string}",
                    f"PHP0{i}{duration_string}": f"PHP{price}{replace_string}{duration}" if i <= len(voucher_amounts) else f"PHP0{i}",
                    f"PHP0{i}{type_string}": f"PHP{price}{replace_string}{type}" if i <= len(voucher_amounts) else f"PHP0{i}",
                    f"PHP0{i}": f"PHP{price}" if i <= len(voucher_amounts) else f"PHP0{i}"
                })
            loop_stopped = i + 1    

            # Perform the final regex replacement after collecting all amount_ids and finishing all content replacements
            if amount_ids:
                new_group = f"({'|'.join(amount_ids)})"
                modified_content = re.sub(r"\((?:\d+\|?)+\)", new_group, modified_content)


            def replace_content_in_file(search_path, main_content):
                if os.path.exists(search_path):
                    with open(search_path, 'r', encoding="utf-8") as search_file:
                        search_str = search_file.read()

                    # Perform the replacement in the main content
                    modified_content = main_content.replace(search_str, "")
                    return modified_content

                return None

            modified_content_temp = modified_content  # Use a separate variable

            while loop_stopped < 10:
                # Generate replacement paths for action_1
                search_path_action1 = os.path.join(macro_action1_path, f"e_php_{loop_stopped}.macro")
                # Generate replacement paths for action_2
                search_path_action2 = os.path.join(macro_action2_path, f"e_vcod_{loop_stopped}.macro")

                # Perform replacements
                modified_content_temp = replace_content_in_file(search_path_action1, modified_content_temp)
                modified_content_temp = replace_content_in_file(search_path_action2, modified_content_temp)

                if loop_stopped == 9:
                    # Replace unused strings with empty string directly in modified_content_temp without the comma (end part)
                    modified_content_temp = modified_content_temp.replace(f",{key_string}{str(loop_stopped)}{rcvamt_string}", "")
                    modified_content_temp = modified_content_temp.replace(f",{key_string}{str(loop_stopped)}{rcvmya_string}", "")
                    modified_content_temp = modified_content_temp.replace(f",{key_string}{str(loop_stopped)}{vamtx_string}", "")
                    modified_content_temp = modified_content_temp.replace(f",{vcodkey_string}{str(loop_stopped)}{vchcd_string}", "")
                    modified_content_temp = modified_content_temp.replace(f",{key_string}{str(loop_stopped)}{vchcd_string}", "")               
                    modified_content_temp = modified_content_temp.replace(f",{key_string}{str(loop_stopped)}{vdrt_string}", "")
                    modified_content_temp = modified_content_temp.replace(f",{key_string}{str(loop_stopped)}{vusr_string}", "")
                else:
                    # Replace unused strings with empty string directly in modified_content_temp with the comma ","
                    modified_content_temp = modified_content_temp.replace(f"{key_string}{str(loop_stopped)}{rcvamt_string},", "")
                    modified_content_temp = modified_content_temp.replace(f"{key_string}{str(loop_stopped)}{rcvmya_string},", "")
                    modified_content_temp = modified_content_temp.replace(f"{key_string}{str(loop_stopped)}{vamtx_string},", "")            
                    modified_content_temp = modified_content_temp.replace(f"{vcodkey_string}{str(loop_stopped)}{vchcd_string},", "")
                    modified_content_temp = modified_content_temp.replace(f"{key_string}{str(loop_stopped)}{vchcd_string},", "")                    
                    modified_content_temp = modified_content_temp.replace(f"{key_string}{str(loop_stopped)}{vdrt_string},", "")
                    modified_content_temp = modified_content_temp.replace(f"{key_string}{str(loop_stopped)}{vusr_string},", "")

                loop_stopped += 1

            # After the loop, assign the modified content back to the original variable
            modified_content = modified_content_temp

        print("\nConfiguring your macro, please wait...")
        time.sleep(1)

        # Perform all replacements in a single pass
        for placeholder, replacement in replacements.items():
            modified_content = modified_content.replace(placeholder, replacement)

        # Save the modified content to the destination file
        with open(modified_macro_file_path, "w", encoding="utf-8") as modified_file:
            modified_file.write(modified_content)

        # Check voucher code length from the CSV file
        check_csv_file()

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

        # Call backup function
        manage_backup_folder()  

        print("\nOpening macro download folder...")
        time.sleep(3)

        with open(FILE_PATHS["main_folder_id"], 'r') as file:
            folder_id = file.read().strip()
            url = f"https://drive.google.com/drive/u/0/folders/{folder_id}"

        webbrowser.open(url)