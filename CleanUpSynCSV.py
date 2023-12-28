import csv
import glob
import os
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
    error_messages.append("Please execute RUN INITIAL CONFIG first.")

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
print("All initial checks passed. Proceeding...")
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

# Specify the voucher wifi app folder name
app_name = 'GCONNECT'

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

csv_file = "VoucherList.csv"
output_file5 = "5php_vouchers.txt"
output_file10 = "10php_vouchers.txt"
output_file15 = "15php_vouchers.txt"
output_file20 = "20php_vouchers.txt"
output_file30 = "30php_vouchers.txt"
output_file50 = "50php_vouchers.txt"
output_file99 = "99php_vouchers.txt"
output_expired = "expired_vouchers.txt"

with open(csv_file, "r") as file:
    reader = csv.DictReader(file)

    codes_5 = []
    codes_10 = []
    codes_15 = []
    codes_20 = []
    codes_30 = []
    codes_50 = []
    codes_99 = []
    codes_expired = []

    for row in reader:
        duration = row["Duration"]
        type = row["Type"]
        code = row["Code"]
        notes = row["Notes"]

        # Add leading zeroes if code length is not 10
        if len(code) != 10:
            code = code.zfill(10)

        if type != "Expired" and notes != "PRINT VOUCHER":
            if duration == "30.0Minutes":
                codes_5.append(code)
            elif duration == "60.0Minutes":
                codes_10.append(code)
            elif duration == "3.0Hours":
                codes_15.append(code)
            elif duration == "6.0Hours":
                codes_20.append(code)
            elif duration == "12.0Hours":
                codes_30.append(code)
            elif duration == "72.0Hours":
                codes_50.append(code)
            elif duration == "168.0Hours":
                codes_99.append(code)
        elif type == "Expired":
            codes_expired.append(code)

    with open(output_file5, "w") as file:
        for code in codes_5:
            file.write(code + "\n")
    print("Voucher Codes saved to", output_file5)

    with open(output_file10, "w") as file:
        for code in codes_10:
            file.write(code + "\n")
    print("Voucher Codes saved to", output_file10)

    with open(output_file15, "w") as file:
        for code in codes_15:
            file.write(code + "\n")
    print("Voucher Codes saved to", output_file15)

    with open(output_file20, "w") as file:
        for code in codes_20:
            file.write(code + "\n")
    print("Voucher Codes saved to", output_file20)

    with open(output_file30, "w") as file:
        for code in codes_30:
            file.write(code + "\n")
    print("Voucher Codes saved to", output_file30)

    with open(output_file50, "w") as file:
        for code in codes_50:
            file.write(code + "\n")
    print("Voucher Codes saved to", output_file50)

    with open(output_file99, "w") as file:
        for code in codes_99:
            file.write(code + "\n")
    print("Voucher Codes saved to", output_file99)

    with open(output_expired, "w") as file:
        for code in codes_expired:
            file.write(code + "\n")
    print("Voucher Codes saved to", output_expired)

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

print("Launch browser to sync...")
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

