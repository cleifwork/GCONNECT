import csv
import glob
import os
import time
from tkinter import messagebox

# Specify the voucher wifi app folder name
wifi_name = 'GCONNECT'

# Specify the directory where the CSV file is located
directory = os.path.join(os.environ['USERPROFILE'], 'Desktop', wifi_name, 'raw_csv')

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
    messagebox.showwarning("No CSV File Found", "No CSV file found in the directory.")
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
    time.sleep(1)

    with open(output_file10, "w") as file:
        for code in codes_10:
            file.write(code + "\n")
    print("Voucher Codes saved to", output_file10)
    time.sleep(1)

    with open(output_file15, "w") as file:
        for code in codes_15:
            file.write(code + "\n")
    print("Voucher Codes saved to", output_file15)
    time.sleep(1)

    with open(output_file20, "w") as file:
        for code in codes_20:
            file.write(code + "\n")
    print("Voucher Codes saved to", output_file20)
    time.sleep(1)

    with open(output_file30, "w") as file:
        for code in codes_30:
            file.write(code + "\n")
    print("Voucher Codes saved to", output_file30)
    time.sleep(1)

    with open(output_file50, "w") as file:
        for code in codes_50:
            file.write(code + "\n")
    print("Voucher Codes saved to", output_file50)
    time.sleep(1)

    with open(output_file99, "w") as file:
        for code in codes_99:
            file.write(code + "\n")
    print("Voucher Codes saved to", output_file99)
    time.sleep(1)

    with open(output_expired, "w") as file:
        for code in codes_expired:
            file.write(code + "\n")
    print("Voucher Codes saved to", output_expired)
    time.sleep(1)

    print("\nDone...")
    time.sleep(1)

    print("Exiting process...")
    time.sleep(1)
    