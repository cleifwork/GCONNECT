import os
import csv
import glob
import time
import subprocess
import webbrowser
from tkinter import messagebox
import win32com.client as win32
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# List to store error messages
error_messages = []
actions_to_take = []

# Check 1: Check if "service_account.json" is present
if not os.path.isfile("service_account.json"):
    error_messages.append("Please execute 'RUN INITIAL CONFIG' first.")

# Check 2: Check if "put_folder_id_here.txt" is not empty
with open("put_folder_id_here.txt", "r") as folder_id_file:
    folder_id = folder_id_file.read().strip()

    if not folder_id:
        error_messages.append("No folder ID found!")

# Check 3: Check if "put_md_url_here.txt" is not empty and contains a valid URL
with open("put_md_url_here.txt", "r") as md_url_file:
    md_url = md_url_file.read().strip()

    if not md_url or not md_url.startswith("http"):
        error_messages.append("Please check 'put_md_url_here.txt' for a valid URL.")
        text_file_path = "put_md_url_here.txt"
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
# Rename the first CSV file found
if csv_files:
    current_filename = csv_files[0]
    new_filename = 'VoucherList.csv'

    # Check if the new filename already exists
    if os.path.exists(new_filename):
        os.remove(new_filename)  # Remove the existing file

    os.rename(current_filename, new_filename)
else:
    messagebox.showerror("No CSV File Found", "No CSV file found in the directory.")
    exit()

# Read the amounts from the input file
with open("put_voucher_amt_here.txt", "r") as input_file:
    amounts = [line.strip() for line in input_file]

# Check if the amounts list is empty
if not amounts:
    error_message = "The input file is empty. \nPlease provide voucher amounts in 'put_voucher_amt_here.txt'."
    messagebox.showerror("Error", error_message)

    # Open the file for editing
    file_path = "put_voucher_amt_here.txt"
    os.system(f"notepad.exe {file_path}")

    exit()

# Define the output file names dynamically based on the amounts
output_files = [f"{amount}php_vouchers.txt" for amount in amounts]

# Define the code arrays dynamically based on the amounts
code_arrays = {amount: [] for amount in amounts}

csv_file = "VoucherList.csv"
output_expired = "expired_vouchers.txt"

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

        # Add leading zeroes if code length is not 10 (DISABLED)
        # if len(code) != 10:
        #     code = code.zfill(10)

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
print(f"Expired Vouchers Codes saved to {output_expired} \n")

def main():
    service = create_drive_service()

    # Read voucher filenames from voucher_logger.txt
    voucher_filenames_file = 'voucher_logger.txt'
    with open(voucher_filenames_file, 'r') as file:
        voucher_files = [line.strip() for line in file]

    for upload_file_path in voucher_files:
        upload_file(service, upload_file_path, destination_folder_id)

def upload_file(service, file_path, folder_id):
    file_name = os.path.basename(file_path)
    existing_file_id = get_file_id(service, file_name, folder_id)
    
    if existing_file_id:
        # If the file exists, update its content
        media = MediaFileUpload(file_path, resumable=True)
        file = service.files().update(fileId=existing_file_id, media_body=media).execute()
        print(f"Updated '{file_name}' in GDrive with ID: {file['id']}")
    else:
        # If the file does not exist, create a new one
        file_metadata = {
            "name": file_name,
            "parents": [folder_id]
        }
        media = MediaFileUpload(file_path, resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        print(f"Uploaded '{file_name}' to GDrive with ID: {file['id']}")

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

print("\nDone...")
time.sleep(1)

print("Launching browser to sync...")
time.sleep(2)      

# Open the text file and read the content
with open('put_md_url_here.txt', 'r') as file:
    # Read the content and remove any leading or trailing whitespace
    url = file.read().strip()
    webbrowser.open(url)   

# Create WScript Shell Object to access filesystem.
WshShell = win32.Dispatch("WScript.Shell")

# Allocate 5 seconds loading time before closing the tab
time.sleep(5)
WshShell.SendKeys("^w")    

