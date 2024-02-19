import csv
import glob
import os
import time
from tkinter import messagebox

# Check if "put_voucher_amt_here.txt" is empty
with open("put_voucher_amt_here.txt", "r") as input_file:
    amounts = [line.strip() for line in input_file]

# Check if the amounts list is empty
if not amounts:
    print("The input file is empty. Proceed getting prices from the CSV file...")
    time.sleep(1)
    
    # Specify the voucher wifi app folder name
    wifi_name = 'GCONNECT'

    # Specify the directory where the CSV file is located
    directory = os.path.join(os.environ['USERPROFILE'], 'Desktop', wifi_name, 'raw_csv')

    # Search for CSV files in the directory
    csv_files = glob.glob(os.path.join(directory, '*.csv'))

    # Check if there are CSV files in the directory
    if not csv_files:
        messagebox.showerror("Error", "No CSV files found in the directory.\nPlease provide voucher amounts in 'put_voucher_amt_here.txt'.")
    else:
        # Take the first CSV file found
        csv_file = csv_files[0]

        # Read the unique prices from the CSV file
        unique_prices = set()
        with open(csv_file, "r") as file:
            # Create a CSV reader
            reader = csv.DictReader(file)

            # Iterate over each row in the CSV file
            for row in reader:
                # Extract the price from the row and strip non-numeric values
                price = ''.join(char for char in row["Price"] if char.isdigit())
                if price:
                    unique_prices.add(price)

        # Check if unique prices set is empty
        if not unique_prices:
            messagebox.showerror("Error", f"No valid prices found in the CSV file: {csv_file}.")
        else:
            with open("put_voucher_amt_here.txt", "w") as output_file:
                output_file.write("\n".join(map(str, sorted(unique_prices, key=int))))
                print("Successfully added voucher prices from the CSV file...")
                time.sleep(1)
else:
    # Check if all elements in the amounts list are numbers
    if not all(amount.isdigit() for amount in amounts):
        messagebox.showerror("Error", "Please provide valid voucher amounts.")
