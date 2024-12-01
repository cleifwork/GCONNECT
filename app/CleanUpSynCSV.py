import os
import csv
import sys
import glob
import time
import requests
from tkinter import messagebox
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from utils import exe_dir, FILE_PATHS, check_file_exists, check_non_empty, open_in_notepad, execute_actions

# List to store error messages and actions to take
error_messages = []
actions_to_take = []

# Check if "service_account.json" is present
error = check_file_exists(FILE_PATHS["service_account"], "Please execute 'RUN INITIAL CONFIG' first.")
if error:
    error_messages.append(error)

# Check if "put_folder_id_here.txt" is not empty
folder_id = check_non_empty(FILE_PATHS["sub_folder_id"], "No folder ID found!")

# Check if "put_md_url_here.txt" is valid
md_url = check_non_empty(
    FILE_PATHS["md_url"],
    "Please check 'put_md_url_here.txt' for a valid URL.",
    additional_action=lambda: open_in_notepad(FILE_PATHS["md_url"])
)
if md_url and not md_url.startswith("http"):
    error_messages.append("Please check 'put_md_url_here.txt' for a valid URL.")

# Check if "put_voucher_amt_here.txt" is not empty
amounts = check_non_empty(
    FILE_PATHS["voucher_amt"],
    "The input file is empty. \nPlease provide voucher amounts in 'put_voucher_amt_here.txt'.",
    additional_action=lambda: open_in_notepad("put_voucher_amt_here.txt")
)
if amounts:
    amounts = [line.strip().split(',')[0] for line in amounts.splitlines()]

# Display all error messages
if error_messages:
    messagebox.showerror("Error", "\n".join(error_messages))
    execute_actions(actions_to_take)
    sys.exit()

print("All initial checks passed. Proceeding...\n")
time.sleep(1)

# Replace 'credentials.json' with the path to your service account key JSON file
credentials_file = FILE_PATHS["service_account"]

# Open the text file and read the content
with open(FILE_PATHS["sub_folder_id"], 'r') as file:
    # Read the content and remove any leading or trailing whitespace
    destination_folder_id = file.read().strip()


# Define the function to authenticate and create a Drive service
def create_drive_service():
    credentials = service_account.Credentials.from_service_account_file(credentials_file, scopes=["https://www.googleapis.com/auth/drive"])
    return build("drive", "v3", credentials=credentials)

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
# Rename the first CSV file found
if csv_files:
    current_filename = csv_files[0]
    new_filename = FILE_PATHS["voucher_list"]

    # Check if the new filename already exists
    if os.path.exists(new_filename):
        os.remove(new_filename)  # Remove the existing file

    os.rename(current_filename, new_filename)
else:
    messagebox.showerror("No CSV File Found", "No CSV file found in the directory.")
    sys.exit()

# Define the output file names dynamically based on the amounts
output_files = [os.path.join(exe_dir, f"{amount}php_vouchers.txt") for amount in amounts]

# Define the code arrays dynamically based on the amounts
code_arrays = {amount: [] for amount in amounts}

csv_file = FILE_PATHS["voucher_list"]
output_expired = FILE_PATHS["expired_vouchers"]
vcode_length = FILE_PATHS["vcodlen"]

# Read the voucher code length from "put_vcodlen_here.txt"
with open(vcode_length, 'r') as vcode_len_file:
    vcode_length = int(vcode_len_file.read().strip())

# Initialize lists to store voucher codes based on duration and type
codes_expired = []

# Open the CSV file for reading
with open(csv_file, "r") as file:
    # Create a CSV reader
    reader = csv.DictReader(file)

    # Iterate over each row in the CSV file
    for row in reader:
        # Extract relevant information from the row
        code = row["Code"]
        price = row["Price"]
        notes = row["Notes"]
        duration = row["Duration"]
        type = row["Type"]

        # Add leading zeroes based on the value in put_vcodlen_here.txt
        if len(code) < vcode_length:
            code = code.zfill(vcode_length)        

        # Categorize voucher codes based on duration and type
        for amount in amounts: 
            if type != "Expired" and notes != "PRINT VOUCHER" and price[3:] == amount:
                code_arrays[amount].append(code)
        
        if type == "Expired":
            codes_expired.append(code)

# Write voucher codes to separate output files based on amounts
for amount, output_file in zip(amounts, output_files):
    with open(output_file, "w") as file:
        for code in code_arrays[amount]:
            file.write(code + "\n")
        print(f"Voucher Codes for {amount} saved to {output_file}")
        time.sleep(1)

# Write expired voucher codes to a separate output file
with open(output_expired, "w") as file:
    for code in codes_expired:
        file.write(code + "\n")
print(f"Expired Voucher Codes saved to {output_expired} \n")


def main():
    """
    Main function to upload voucher files to Google Drive.
    """
    service = create_drive_service()

    # Read the destination folder ID
    with open(FILE_PATHS["sub_folder_id"], 'r') as file:
        destination_folder_id = file.read().strip()

    try:
        # Read voucher filenames from voucher_logger.txt
        with open(FILE_PATHS["voucher_log"], 'r') as file:
            voucher_files = [os.path.join(exe_dir, line.strip()) for line in file]

        # Upload each file and log the result
        for file_path in voucher_files:
            if os.path.isfile(file_path):
                message = upload_file(service, file_path, destination_folder_id)
                print(message)  # Log only the message returned by upload_file
            else:
                print(f"File not found: {file_path}")
    except FileNotFoundError:
        print(f"Error: {FILE_PATHS['voucher_log']} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def upload_file(service, file_path, folder_id):
    file_name = os.path.basename(file_path)
    existing_file_id = get_file_id(service, file_name, folder_id)

    if existing_file_id:
        # Update the existing file
        media = MediaFileUpload(file_path, resumable=True)
        file = service.files().update(fileId=existing_file_id, media_body=media).execute()
        result_message = f"Updated '{file_name}' in GDrive with ID: {file['id']}"
    else:
        # Upload a new file
        file_metadata = {"name": file_name, "parents": [folder_id]}
        media = MediaFileUpload(file_path, resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        result_message = f"Uploaded '{file_name}' to GDrive with ID: {file['id']}"

    # Set the permission to anyone with the link
    service.permissions().create(
        fileId=file["id"],
        body={"role": "reader", "type": "anyone", "withLink": True},
        fields="id"
    ).execute()

    return result_message  # Return the status message


def get_file_id(service, file_name, folder_id):
    # Retrieve the file ID by name in the specified folder
    results = service.files().list(q=f"'{folder_id}' in parents and name = '{file_name}'", fields="files(id)").execute()
    items = results.get('files', [])
    return items[0]['id'] if items else None

if __name__ == "__main__":
    main()

print("\nDone...")
time.sleep(1)

# Open the text file and read the content
with open(FILE_PATHS["md_url"], 'r') as file:
    # Read the content and remove any leading or trailing whitespace
    webhook_url = file.read().strip()

try:
    response = requests.get(webhook_url)
    response.raise_for_status()  # Will raise an HTTPError for bad responses
    print("Webhook triggered successfully!")
except requests.exceptions.RequestException as e:
    print(f"Error triggering webhook: {e}")
